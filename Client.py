import asyncio

async def tcp_echo_client():
    reader, writer = await asyncio.open_connection('127.0.0.1', 8080, loop=loop)

    while True:        
        data = await reader.read(1000)
        print(data.decode())
        message = input()
        
        if message == 'exit':
            break

        writer.write(message.encode(encoding='UTF-8'))
        
        data = await reader.readline()
        print(data.decode())
    print('Close the connection')
    writer.close()

message = "Hello world"
loop = asyncio.get_event_loop()
loop.run_until_complete(tcp_echo_client(message, loop))
loop.close()
asyncio.run(tcp_echo_client())
