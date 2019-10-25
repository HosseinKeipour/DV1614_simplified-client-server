import asyncio
import random
from service import User
from service import Admin
import os
import json
import socket

name_list = [""]   # report3- we should define some unacceptable or restrict chararcter
registered = {'client_name': [], 'client_password': [], 'client_privilege': []}
signedin = []
created_folder = {}
path = os.getcwd()



async def send_back(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    global path 
    # 'peername' is remote address connected to
    addr = writer.get_extra_info('peername')
    message = f'{addr!r} is connected !!!!' # !r calls the __repr__ method
    print(message)
    flag = False
    with open(f'{path}/root/Server/client-info.json', 'r') as file:
                registered = json.load(file)
    with open(f'{path}/root/Server/signed-info.json', 'r') as file:
                signedin = json.load(file)
    # try:
    while message != 'quit':

        if flag == False:
            writer.write('\n\rYou are conected to Pytonista Server'.encode(encoding='UTF-8'))
            writer.write('\n\rPlease select login or register (login/register)'.encode(encoding='UTF-8'))
            writer.write('>>'.encode(encoding='UTF-8'))
            flag = True
        # try:
        #     data = await reader.readline()
        #     message = data.decode().strip()  
        # except ConnectionError:
        #     message = 'quit'
        data = await reader.readline()
        message = data.decode().strip()
            
                

        if message == 'register':
            while True:
                writer.write('\n\rPlease enter your username:'.encode(encoding='UTF-8'))
                data = await reader.readline()
                name = data.decode().strip()
                
                if username_check(name, registered['client_name']) == False:
                    registered['client_name'].append(name)
                    break
                writer.write('\n\rError: The username has been selected'.encode(encoding='UTF-8'))
                
            while True:
                writer.write('\n\rPlease enter your password:'.encode(encoding='UTF-8'))
                data = await reader.readline()
                password = data.decode().strip()
                if password != "":
                    registered['client_password'].append(password)
                    break
                else:
                    writer.write('\n\rError:The password pattern is incorrect.'.encode(encoding='UTF-8'))

            while True:
                writer.write('\n\rPlease define your privilege (user/admin):'.encode(encoding='UTF-8'))
                data = await reader.readline()
                privilege = data.decode().strip()                    
                if privilege == "user" or privilege == "admin":
                    registered['client_privilege'].append(privilege)
                    break
                else:
                    writer.write('\n\rError:The selected privilge is incorrect.'.encode(encoding='UTF-8'))

            if privilege == "user":
                user_path = f"{path}root/user/{name}"
                os.mkdir(user_path)
                
            elif privilege == "admin":
                admin_path = f"{path}root/admin/{name}"
                os.mkdir(admin_path)
            
            await writer.drain()

            with open(f'{path}/root/Server/client-info.json', 'w') as file:
                json.dump(registered, file)
            
            # created_folder[name] = []
            # created_folder[name].append(name)
            # with open('root/Server/created_folder.json', 'w') as file:
            #     json.dump(created_folder, file)


        elif message == 'login':
            while True:
                writer.write('\n\rPlease enter your username:'.encode(encoding='UTF-8'))
                data = await reader.readline()
                name = data.decode().strip()
                
                if username_check(name, registered['client_name']) and name not in signedin:
                    index = registered['client_name'].index(name)
                    signedin.append(name)
                    break
                else:
                    writer.write('\n\rError: This username is not exist or already logged in.'.encode(encoding='UTF-8'))
                
            while True:
                writer.write('\n\rPlease enter your password:'.encode(encoding='UTF-8'))
                data = await reader.readline()
                password = data.decode().strip()

                if password == registered['client_password'][index]:
                    # writer.write(name.encode(encoding='UTF-8'))
                    with open(f'{path}/root/Server/signed-info.json', 'w') as file:
                        json.dump(signedin, file)
                    break
                else:
                    writer.write('\n\rError:The password is incorrect. Please try again.'.encode(encoding='UTF-8'))
                    
            index = registered['client_name'].index(name)
            privilege = registered['client_privilege'][index]

            if privilege == "user":
                client = User(name, password, privilege)
            else:
                client = Admin(name, password, privilege)

        elif message == 'commands':
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

        elif message == 'mkdir':
            if username_check(name, signedin):
                writer.write('\n\rPlease enter folder name:'.encode(encoding='UTF-8'))
                data = await reader.readline()
                folder = data.decode().strip() 
                client.create_folder(name, privilege, folder, reader, writer)

        elif message == 'cd':
            if username_check(name, signedin):
                writer.write('\n\rPlease enter folder name:'.encode(encoding='UTF-8'))
                data = await reader.readline()
                folder = data.decode().strip() 
                client.change_folder(name, privilege, folder, reader, writer)

        elif message == 'cd ..':
            if username_check(name, signedin):
                client.back_folder(name, privilege, folder, reader, writer)

        elif message == 'ls':
            if username_check(name, signedin):
                client.print_list(name, reader, writer)

        elif message == 'write':
            if username_check(name, signedin):
                writer.write('\n\rPlease enter file name:'.encode(encoding='UTF-8'))
                data = await reader.readline()
                file_name = data.decode().strip()

                writer.write('\n\rPlease enter text:'.encode(encoding='UTF-8'))
                data = await reader.readline()
                user_input = data.decode().strip()

                client.write_file(name, file_name, user_input, reader, writer)
        
        elif message == 'read':
            if username_check(name, signedin):
                writer.write('\n\rPlease enter file name:'.encode(encoding='UTF-8'))
                data = await reader.readline()
                file_name = data.decode().strip()

                client.read_file(name, file_name, reader, writer)

        elif message == 'delete':
            if username_check(name, signedin):
                writer.write('\n\rPlease enter the username which should be deleted:'.encode(encoding='UTF-8'))
                data = await reader.readline()
                user_name = data.decode().strip()

                writer.write('\n\rPlease enter your password:'.encode(encoding='UTF-8'))
                data = await reader.readline()
                input_password = data.decode().strip()
                
                client.delete(name, password, privilege, user_name, input_password, reader, writer)
                
        elif message == 'quit':
            signedin.remove(name)
            with open(f'{path}/root/Server/signed-info.json', 'w') as file:
                json.dump(signedin, file)
            close_msg = f'{addr!r} wants to close the connection.'
            print(close_msg)
            break
        else:
            writer.write('\n\rThe implemented command is wrong.Please type "commands"'.encode(encoding='UTF-8'))

        writer.write('>>'.encode(encoding='UTF-8'))
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

def get_first_path():
    if path_flag == 1:
        path = os.getcwd()
        path_flag = 2   
    return path


# async def register_client(reader, writer):
#     while True:
#         writer.write('\n\rPlease enter your username:'.encode(encoding='UTF-8'))
#         data = await reader.readline()
#         # Transfer format is bytes, decode() makes it a string
#         name = data.decode().strip()
            
#         if username_check(name, name_list) == False:
#             name_list.append(name)
#             break
#             writer.write('\n\rError: The username has been selected'.encode(encoding='UTF-8'))

                        
                
#     while True:
#         writer.write('\n\rPlease enter your password:'.encode(encoding='UTF-8'))
#         data = await reader.readline()
#         # Transfer format is bytes, decode() makes it a string
#         password = data.decode().strip()
        
#         if password != "":
#             break
#         else:
#             writer.write('\n\rError:The password pattern is incorrect.'.encode(encoding='UTF-8'))

#     while True:
        # writer.write('\n\rPlease define your privilege (user/admin):'.encode(encoding='UTF-8'))
        # data = await reader.readline()
        # # Transfer format is bytes, decode() makes it a string
        # privilege = data.decode().strip()                    
        # if privilege == "user" or privilege == "admin":
        #     break
        # else:
        #     writer.write('\n\rError:The selected privilge is incorrect.'.encode(encoding='UTF-8'))


asyncio.run(main())

