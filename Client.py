import asyncio
async def get_message(reader, writer):
    user_input = input("user input:")
    
    writer.write(user_input.encode(encoding='UTF-8'))
    return user_input

async def tcp_echo_client():
    reader, writer = await asyncio.open_connection('127.0.0.1', 8080)

    while True:
        data = await reader.read(1000)
        print(f"{data.decode()}")

        message = await get_message(reader, writer)
        
        if message == 'exit':
            break

    print('Close the connection')
    writer.close()

asyncio.run(tcp_echo_client())
