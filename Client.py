"""
This module contains two functions. One for sending input commands from its terminal to the server.
Another for connecting to server in given IP address and port number. if there was a data, It sends
data from service with await command and print it in terminal for user. When started up, it should
present the user with the option to either login or register to the server. These options are to
result in requests to the server, and a login is only to be allowed if the username and password
matches with the information on the server The user should be able to input any command described
for the server. Whenever a command is issued, the client is to send a request to the server and
present the result to the user if applicable. The client is also required to save down all commands
issued by each user. If the message was quit, the loop will be stopped and the connection will be
closed.
"""
import asyncio
commands_issued = list()
valid_commands = ['register', 'login', 'create_folder', 'change_folder', 'list', 'write_file',
                  'read_file', 'delete', 'quit', 'commands']
async def get_message(reader, writer):
    """
    The function gets input from terminal and send it to server, also return it to
    tcp_echo_client On the other step Whenever a command is issued, the client is to
    send a request to the server and present the result to the user if applicable.
    The client is also save down all commands issued by each user. If the message was
    quit, the loop will be stopped and the connection will be closed.
    """
    user_input = input("user input:") 
    commands_issued.append(user_input)
    msg = user_input.strip()
    message = msg.split()

    # assert-statement for valid commands
    try:
        assert message[0] in valid_commands, "The implemented command is wrong"
    except AssertionError as error:
        print(error)

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
            # return()
        elif len(message) == 2:
            if message[1] == "issued":
                print(commands_issued)
                # return()
            elif message[1] == "clear":
                commands_issued.clear()
            else:
                print("The implemented command is wrong")
        else:
            print("The implemented command is wrong")
    return user_input

async def tcp_echo_client():
    """
    The function makes connection with server, It gets data from server to show the user
    connection in the server terminal, then it calls the get_message function, if the
    returned message is not quit, the while will be repeated, otherwise the connection
    will be closed
    """
    reader, writer = await asyncio.open_connection('127.0.0.1', 8080)

    while True:
        data = await reader.read(1000)
        print(f"{data.decode()}")

        message = await get_message(reader, writer)

        writer.write(message.encode(encoding='UTF-8'))
        await writer.drain()

        if message == 'quit':
            break

    print('Close the connection')
    writer.close()

asyncio.run(tcp_echo_client())
