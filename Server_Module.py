import asyncio
import random

def funcname(self, parameter_list):
    pass
async def send_back(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    # 'peername' is remote address connected to
    addr = writer.get_extra_info('peername')
    message = f'{addr!r} is connected !!!!' # !r calls the __repr__ method
    print(message)
    flag = False
    while message != 'quit':

        if flag == False:
            writer.write('\n\r[You are conected to Pytonista Server]'.encode(encoding='UTF-8'))
            writer.write('\n\r[Enter S to Sign in or R to Register(S/R)]>> '.encode(encoding='UTF-8'))
            flag = True
        
        data = await reader.readline()

        message = data.decode().strip()             # Transfer format is bytes, decode() makes it a string

        if message == 'R':
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


asyncio.run(main())