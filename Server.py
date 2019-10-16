import asyncio
import random
async def send_back(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    # 'peername' is remote address connected to
    addr = writer.get_extra_info('peername')
    message = f'{addr!r} is connected !!!!' # !r calls the __repr__ method
    print(message)
    while message != 'exit':
        data = await reader.readline()
        # Transfer format is bytes, decode() makes it a string
        message = data.decode().strip()
        await asyncio.sleep(random.randint(0, 10))
        # The Streamwriter.write() is just a regular function
        writer.write('\n[From server]: '.encode(encoding='UTF-8')+data[::-1])
        await writer.drain()
        if message == 'exit':
            close_msg = f'{addr!r} wants to close the connection.'
            print(close_msg)
            break
    writer.close()

async def main():
    server = await asyncio.start_server(send_back, '127.0.0.1', 8888)

    addr = server.sockets[0].getsockname()
    print(f'Serving on {addr}')
    async with server:
        await server.serve_forever()
asyncio.run(main())