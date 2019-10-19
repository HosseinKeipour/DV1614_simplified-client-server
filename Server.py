import asyncio
import random
from Client import User

# def funcname(self, parameter_list):
#     pass
async def send_back(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    # 'peername' is remote address connected to
    addr = writer.get_extra_info('peername')
    message = f'{addr!r} is connected !!!!' # !r calls the __repr__ method
    print(message)
    flag = False
    name_list = [""]   # report3- we should define some unacceptable or restrict chararcter
    while message != 'quit':

        if flag == False:
            writer.write('\n\rYou are conected to Pytonista Server'.encode(encoding='UTF-8'))
            writer.write('\n\rEnter S to Sign in or R to Register(S/R):'.encode(encoding='UTF-8'))
            flag = True
        
        data = await reader.readline()

        message = data.decode().strip()             # Transfer format is bytes, decode() makes it a string

        if message == 'R':
            while True:
                writer.write('\n\rPlease enter your username:'.encode(encoding='UTF-8'))
                data = await reader.readline()
                # Transfer format is bytes, decode() makes it a string
                name = data.decode().strip()
                # for i in range(0, len(name_list)-1):   
                #     if name == name_list[i]:
                #         writer.write('\n\rError: The username has been selected'.encode(encoding='UTF-8'))
                #         # name_list.remove(name)
                #         # continue
                # name_list.append(name)
                # break
                if username_check(name, name_list) == False:
                    name_list.append(name)
                    
                    break
                writer.write('\n\rError: The username has been selected'.encode(encoding='UTF-8'))

                        
                
            while True:
                writer.write('\n\rPlease enter your password:'.encode(encoding='UTF-8'))
                data = await reader.readline()
                # Transfer format is bytes, decode() makes it a string
                password = data.decode().strip()
                if password != "":
                    break
                else:
                    writer.write('\n\rError:The password pattern is incorrect.'.encode(encoding='UTF-8'))

            while True:
                writer.write('\n\rPlease define your privilege (user/admin):'.encode(encoding='UTF-8'))
                data = await reader.readline()
                # Transfer format is bytes, decode() makes it a string
                privilege = data.decode().strip()                    
                if privilege == "user" or privilege == "admin":
                    break
                else:
                    writer.write('\n\rError:The selected privilge is incorrect.'.encode(encoding='UTF-8'))

            print(f'{name, password, privilege}\n')
            # client = User(name, password, privilege) 
            #     for user in client:
            #         pass 
            writer.write('\n\rR Username:\n\r>>'.encode(encoding='UTF-8'))
            await writer.drain()
        elif message == 'S':
            writer.write('\n\rUsername:'.encode(encoding='UTF-8'))
            await writer.drain()
        else:
            writer.write('\n\rError: input error!!!\n\r[Enter S to Sign in or R to Register(S/R)]>>'.encode(encoding='UTF-8'))
            await writer.drain()
        
        # await asyncio.sleep(random.randint(0, 10))

        if message == 'quit':
            close_msg = f'{addr!r} wants to close the connection.'
            print(close_msg)
            break
    writer.close()

async def main():
    server = await asyncio.start_server(send_back, '127.0.0.1', 8080)

    addr = server.sockets[0].getsockname()
    print(f'Serving on {addr}')
    async with server:
        await server.serve_forever()

def username_check(name, name_list):
    for i in range(0, len(name_list)):   
        if name == name_list[i]:
            return True
    return False

        

asyncio.run(main())