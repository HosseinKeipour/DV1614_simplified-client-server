"""
This module containing two functions.
One for sending input commands from terminal to server.
One for connecting to server in given IP address and port. It gives data from service with await
and print it in terminal for user if there was a data.
Call another function with await to get input messages from user. If the message was exit,
the loop will be stopped and the connection will be closed.
"""
import asyncio
commands_issued = list()
async def get_message(reader, writer):
    """
    Getting input from terminal and send it to server, also return it to tcp_echo_client
    """
    user_input = input("user input:") 

    commands_issued.append(user_input)
    msg = user_input.strip()
    message = msg.split()
    if message[0] == 'commands':
        if len(message) == 1:
            help_message = """
            create_folder <name>---------------------------create a new folder
            change_folder <name>---------------------------change folder
            list-------------------------------------------list directory contents
            read_file <file_name>--------------------------read data from the file
            write_file <file_name> <input>-----------------write the data to the end of the file
            login <username> <password>--------------------log in the user
            register <username> <password> <privileges>----register a new user
            delete <del_username> <admin_password>---------delete a user from the server
            quit------------log out the user, close the connection, close the application
            commands--------------------------------------information about all available commands
            commands issued-------------------------------all commands issued are issued
            commands clear--------------------------------all commands issued are cleared
            """
            print(f'\n\r{help_message}')
            return()
        elif len(message) == 2:
            if message[1] == "issued":
                print(commands_issued)
            elif message[1] == "clear":
                commands_issued.clear()    
            else:
                print("The implemented command is wrong")
            return()  
        else:
            print("The implemented command is wrong")
        return()
    else:
        writer.write(user_input.encode(encoding='UTF-8'))
        return user_input

async def tcp_echo_client():
    """
    making connection with server, getting data from server to show the user in terminal,
    call the get_message function, if the returned message is not exit, the loop will be repeated,
    else the connection will be closed
    """
    reader, writer = await asyncio.open_connection('127.0.0.1', 8000)

    while True:
        data = await reader.read(1000)
        print(f"{data.decode()}")

        message = await get_message(reader, writer)
        if message == 'exit':
            break

    print('Close the connection')
    writer.close()

asyncio.run(tcp_echo_client())
