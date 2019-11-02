import asyncio
import random
from service import User
from service import Admin
import os
import json
import socket
import signal
import string

signal.signal(signal.SIGINT, signal.SIG_DFL)

name_list = [""]   # report3- we should define some unacceptable or restrict chararcter
registered = {'client_name': [], 'client_password': [], 'client_privilege': []}
signedin = []
addr_port = []

created_folder = {}
path = str(os.getcwd())
with open(f'{path}/root/Server/signed-info.json', 'w') as file:
    json.dump(signedin, file)
async def send_back(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    global path 
    # 'peername' is remote address connected to
    addr = writer.get_extra_info('peername')
    message = f'{addr!r} is connected !!!!' # !r calls the __repr__ method
    print(message)
    pre_file_name = ""
    with open(f'{path}/root/Server/client-info.json', 'r') as file:
                registered = json.load(file)
    with open(f'{path}/root/Server/signed-info.json', 'r') as file:
                signedin = json.load(file)
    # try:
  
    writer.write('\n\rYou are conected to Pytonista Server'.encode(encoding='UTF-8'))
    writer.write('\n\rPlease select login or register (login/register)'.encode(encoding='UTF-8'))
    writer.write('>>'.encode(encoding='UTF-8'))
    await writer.drain()
    
    while True:
        data = await reader.read(1000)
        msg = data.decode().strip()
        message = msg.split()
        # await asyncio.sleep(random.randint(0, 10))

        if message[0] == 'register':
            reg_Flag = False
            while True:
                if len(message) == 4:
                    name = message[1]
                    password = message[2]
                    privilege = message[3]
                    restricted_char = string.punctuation
                    for char in restricted_char:
                        if char in name:
                            writer.write('\n\rError:The username characters is not acceptable. Try again!!!!.'.encode(encoding='UTF-8'))
                            await writer.drain()
                            reg_Flag = True
                            break
                    if reg_Flag == True:
                        break
                else:
                    writer.write('\n\rError: Wrong command format'.encode(encoding='UTF-8'))
                    writer.write('\n\rUse: register <username> <password> <privilege>'.encode(encoding='UTF-8'))
                    await writer.drain()
                    break
                
                if username_check(name, registered['client_name']) == False and password != "" and (privilege == "user" or privilege == "admin"):
                    registered['client_name'].append(name)
                    registered['client_password'].append(password)
                    registered['client_privilege'].append(privilege)
                    if privilege == "user":
                        user_path = f"{path}/root/user/{name}"
                        os.mkdir(user_path)

                    elif privilege == "admin":
                        admin_path = f"{path}/root/admin/{name}"
                        os.mkdir(admin_path)

                    with open(f'{path}/root/Server/client-info.json', 'w') as file:
                        json.dump(registered, file)
                    break
                else:
                    if username_check(name, registered['client_name']) == True:
                        writer.write('\n\rError:The username has been already selected.'.encode(encoding='UTF-8'))
                        await writer.drain()
                        break
                    else:
                        writer.write('\n\rError: The selected username, password or privilege is not correct.'.encode(encoding='UTF-8'))
                        await writer.drain()
                        break
        
        elif message[0] == 'login':
            while True:
                if len(message) == 3:
                        name = message[1]
                        password = message[2]
                else:
                    writer.write('\n\rError: Wrong command format'.encode(encoding='UTF-8'))
                    writer.write('\n\rUse: login <username> <password>'.encode(encoding='UTF-8'))
                    await writer.drain()
                    break

                if (username_check(name, registered['client_name']) and name not in signedin):
                    index = registered['client_name'].index(name)

                    if password == registered['client_password'][index]:
                        with open(f'{path}/root/Server/signed-info.json', 'r') as file:
                            signedin = json.load(file)
                        signedin.append(name)
                        with open(f'{path}/root/Server/signed-info.json', 'w') as file:
                            json.dump(signedin, file)
                    else:
                        writer.write('\n\rError:The password is incorrect. Please try again.'.encode(encoding='UTF-8'))
                        await writer.drain()
                        break
                    
                    index = registered['client_name'].index(name)
                    privilege = registered['client_privilege'][index]

                    if privilege == "user":
                        client = User(name, password, privilege)
                    else:
                        client = Admin(name, password, privilege)
                    break
                else:
                    writer.write('\n\rError: This username is not exist or already logged in.'.encode(encoding='UTF-8'))
                    await writer.drain()
                    break

        elif message[0] == 'commands':
            writer.write('\n\rmkdir--------create a new folder'.encode(encoding='UTF-8'))
            writer.write('\n\rcd-----------change folder'.encode(encoding='UTF-8'))
            writer.write('\n\rls-----------list directory contents'.encode(encoding='UTF-8'))
            writer.write('\n\rreadfile-----read data from the file'.encode(encoding='UTF-8'))
            writer.write('\n\rwritefile----write the data to the end of the file'.encode(encoding='UTF-8'))
            writer.write('\n\rlogin--------log in the user'.encode(encoding='UTF-8'))
            writer.write('\n\rregister-----register a new user'.encode(encoding='UTF-8'))
            writer.write('\n\rdel----------delete a user from the server'.encode(encoding='UTF-8'))
            writer.write('\n\rquit---------log out the user, close the connection, close the application'.encode(encoding='UTF-8'))
            writer.write('\n\rcommands-----print information about all available commands'.encode(encoding='UTF-8'))
            await writer.drain()

        elif message[0] == 'mkdir':
            while True:
                if len(message) == 2:
                    folder = message[1]
                else:
                    writer.write('\n\rError: Wrong command format'.encode(encoding='UTF-8'))
                    writer.write('\n\rUse: mkdir <folder_name>'.encode(encoding='UTF-8'))
                    await writer.drain()
                    break
                if username_check(name, signedin):
                    client.create_folder(name, privilege, folder, reader, writer)
                    break
                else:
                    writer.write('\n\rYou should sign in first'.encode(encoding='UTF-8'))
                    await writer.drain()
                    break

        elif message[0] == 'cd':
            while True:
                if len(message) == 2:
                    folder = message[1]
                    restricted_char = string.punctuation
                    print(restricted_char)
                    
                else:
                    writer.write('\n\rError: Wrong command format'.encode(encoding='UTF-8'))
                    writer.write('\n\rUse: cd <folder_name> or cd .. to go back'.encode(encoding='UTF-8'))
                    await writer.drain()
                    break

                if folder == '..':
                    if username_check(name, signedin):
                        client.back_folder(name, privilege, reader, writer)
                        break

                for char in restricted_char:
                    cd_flag = False
                    if char in folder:
                        writer.write('\n\rError:The folder does not exist. Try again!!!!.'.encode(encoding='UTF-8'))
                        await writer.drain()
                        cd_flag = True
                        break
                if cd_flag == False:
                    client.change_folder(name, privilege, folder, reader, writer)         
                    break
                break

        elif message[0] == 'ls':
            while True:
                if len(message) == 1:
                    if username_check(name, signedin):
                        client.print_list(name, reader, writer)
                        break
                else:
                    writer.write('\n\rError: Wrong command format'.encode(encoding='UTF-8'))
                    writer.write('\n\rUse: ls'.encode(encoding='UTF-8'))
                    await writer.drain()
                    break
            
        elif message[0] == 'write':
            while True:
                if len(message) >= 2:
                    file_name = message[1]
                    user_input = ' '.join(message[2:])
                else:
                    writer.write('\n\rError: Wrong command format'.encode(encoding='UTF-8'))
                    writer.write('\n\rUse: write <filename> <input>'.encode(encoding='UTF-8'))
                    await writer.drain()
                    break
                if username_check(name, signedin):
                    client.write_file(name, file_name, user_input, reader, writer)
                    break
        
        elif message[0] == 'read':
            read_flag = False
            while True:
                if len(message) == 1:
                    file_name = ""
                elif len(message) == 2:
                    file_name = message[1]
                else:
                    writer.write('\n\rError: Wrong command format'.encode(encoding='UTF-8'))
                    writer.write('\n\rUse: read <filename>'.encode(encoding='UTF-8'))
                    await writer.drain()
                    break
                if username_check(name, signedin):
                    if pre_file_name == file_name: 
                        read_flag = True
                    client.read_file(file_name, read_flag, reader, writer)
                    pre_file_name = str(file_name)
                    break

        elif message[0] == 'del':
            while True:
                if len(message) == 3:
                    user_name = message[1]
                    input_password = message[2]
                else:
                    writer.write('\n\rError: Wrong command format'.encode(encoding='UTF-8'))
                    writer.write('\n\rUse: del <username> <admin_password>'.encode(encoding='UTF-8'))
                    await writer.drain()
                    break
                if username_check(name, signedin):
                    client.delete(name, password, privilege, user_name, input_password, signedin, reader, writer)
                    break
                
        elif message[0] == 'quit':
            with open(f'{path}/root/Server/signed-info.json', 'r') as file:
                signedin = json.load(file)            
            
            signedin.remove(name)
            
            with open(f'{path}/root/Server/signed-info.json', 'w') as file:
                json.dump(signedin, file)

            close_msg = f'{addr!r} wants to close the connection.'
            print(close_msg)
            break
        else:
            writer.write('\n\rThe implemented command is wrong.Please type "commands"'.encode(encoding='UTF-8'))
            await writer.drain()

        writer.write('\n\r>>'.encode(encoding='UTF-8'))
        await writer.drain()
    writer.close()

    # except:
    #     print("CONNECTION LOST")
    #     signedin.remove(name)
    #     with open(f'{path}/root/Server/signed-info.json', 'w') as file:
    #         json.dump(signedin, file)
    #     close_msg = f'{addr!r} wants to close the connection.'
    #     print(close_msg)
    #     writer.close()
    
    
async def main():
    server = await asyncio.start_server(send_back, '127.0.0.1', 8080)
    addr = server.sockets[0].getsockname()
    # try:
    #     addr = server.sockets[0].getsockname()
    # except socket.error:
    #     addr = None
    # try:
    #     addr.bind(('127.0.0.1', 8080))
    # except socket.error:
    #     addr.close()
    
    print(f'Serving on {addr}')
    async with server:
        await server.serve_forever()

def username_check(name1, name2):
    for i in range(0, len(name2)):   
        if name1 == name2[i]:
            return True
    return False

# def get_first_path():
#     if path_flag == 1:
#         path = str(os.getcwd())
#         path_flag = 2   
#     return path

asyncio.run(main())

