"""
This module containing two functions.
One for sending input commands from terminal to server.
One for connecting to server in given IP address and port. It gives data from service with await 
and print it in terminal for user if there was a data.
Call another function with await to get input messages from user. If the message was exit, 
the loop will be stopped and the connection will be closed.
"""
import asyncio
async def get_message(reader, writer):
    """
    Getting input from terminal and send it to server, also return it to tcp_echo_client
    """
    user_input = input("user input:")
    
    writer.write(user_input.encode(encoding='UTF-8'))
    return user_input

async def tcp_echo_client():
    """
    making connection with server, getting data from server to show the user in terminal, 
    call the get_message function, if the returned message is not exit, the loop will be repeated, 
    else the connection will be closed
    """
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
