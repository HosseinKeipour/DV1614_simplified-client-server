"""
This file contains the classes User, Admin, UserClassTestingStepOne which in order
handling the request from server which is sent by a user, the request from server
which is sent by a admin and tests chosen for testing service functions
"""
import os
import json
import time
import shutil
import unittest
init_cwd = str(os.getcwd())

class User:
    """
    A services for all users, a user or an admin.

    Attributes:
    ------------------------
        name: string
            The user name

        password: string
            The user password

        privilege: string
            The user privilege

    Methods:
    ------------------------
        change_folder(name, privilege, folder):
            Move the current working directory for the current user to the specified folder
            residing in the current folder

        back_folder(name, privilege):
            walk back the previous folder

        create_folder(name, privilege, folder):
            Create a new folder with the specified <name> in the current working
            directory for the user issuing the request

        print_list(name):
            Print all files and folders in the current working directory for the
            user issuing the request

        read_file(file_name, read_flag):
            Read data from the file <name> in the current working directory for
            the user issuing the request and return the first hundred characters in it

        Write_file(name, file_name, user_input):
            Write the data in <input> to the end of the file <name> in the current
            working directory for the user issuing the request, starting on a new line.
            If no file exists with the given name_file, a new file will be created in the
            current working directory for the user
    """

    def __init__(self, name, password, privilege):
        """
        Initialize the user.

        Parameters:
        ------------------------------------------
        name: string
            The user name

        password: string
            The user password

        privilege: string
            The user privilege
        """
        self.name = name
        self.__password = password
        self.privilege = privilege
        self._index = 0
        self.user_list = []
        self.each_user = {'name': self.name, 'password': self.__password,
                          'privilege': self.privilege}
        self.user_list.append(self.each_user)
        self.login_directory = f"root/{privilege}/{name}"
        self.fd = os.path.join(init_cwd, self.login_directory)
        self.read_command_count = 0
        with open(f'{init_cwd}/root/Server/client-info.json', 'r') as file:
            self.registered = json.load(file)
        os.chdir(self.fd)

    def change_folder(self, name, privilege, folder):
        """
        Move the current working directory for the current user to the specified folder
        residing in the current folder
        """
        path = os.path.join(self.fd, folder)
        if self.fd == f"{init_cwd}\\root":
            if privilege == "admin" or "User" == folder:
                try:
                    os.chdir(path)
                    self.fd = os.path.join(self.fd, folder)
                    cwd = str(os.getcwd())
                    return path
                except:
                    error = "Error:The folder does not exist. Try again\n\r"
                    return error
            else:
                error = "Error: Your are not allowed to enter this folder.\n\r"
                return error

        elif self.fd == f"{init_cwd}\\root\\User":
            if name == folder or privilege == "admin":
                try:
                    os.chdir(path)
                    self.fd = os.path.join(self.fd, folder)
                    return path
                except:
                    error = "Error:The folder does not exist. Try again\n\r"
                    return error
            else:
                error = "Error: Your are not allowed to enter this folder.\n\r"
                return error
        else:
            try:
                os.chdir(path)
                self.fd = os.path.join(self.fd, folder)
                cwd = str(os.getcwd())
                return path
            except:
                error = "Error:The folder does not exist. Try again\n\r"
                return error

    def back_folder(self, name, privilege):
        """walk back the previous folder"""
        if self.fd != f"{init_cwd}\\root":
            pathX = self.fd
            self.fd = os.path.dirname(pathX)
            msg = self.fd
            return msg
        else:
            msg = f"Error:You are in root directory\n\r{self.fd}"
            return msg

    def create_folder(self, name, privilege, folder):
        """
        Create a new folder with the specified <name> in the current working directory
        for the user issuing the request
        """
        is_path = self.fd.find(f'{init_cwd}\\root/user/{name}')
        if is_path >= 0 or privilege == "admin":
            path = os.path.join(self.fd, folder)
            try:
                os.makedirs(path)
            except OSError:
                return "Error: Folder with this name exist.\n\r"
            else:
                return "The folder has been made successfully\n\r"
        else:
            return "Error: Your are not allowed to create folder here.\n\r"

    def print_list(self, name):
        """
        Print all files and folders in the current working directory for the user
        issuing the request
        """
        return_msg = ''
        dir_file_list = os.listdir(self.fd)
        for i in range(len(dir_file_list)):
            path = os.path.join(self.fd, dir_file_list[i])
            size = 0
            date = 0
            if os.path.isfile(path):
                size = os.path.getsize(path)
                date = os.path.getctime(path)
                info_msg = (f'{dir_file_list[i]}\t\tsize:{str(size)}\tdate:{time.ctime(date)}\n\r')
                return_msg += str(info_msg)
            elif os.path.isdir(path):
                total_size = 0
                start_path = os.path.join(self.fd, dir_file_list[i])
                date = os.path.getctime(path)
                for path, dirs, files in os.walk(start_path):
                    for f in files:
                        fp = os.path.join(path, f)
                        total_size += os.path.getsize(fp)
                info_msg = (f'{dir_file_list[i]}\t\tsize:{str(total_size)}\tdate:{time.ctime(date)}\n\r')
                return_msg += str(info_msg)
        return return_msg

    def read_file(self, file_name, read_flag):
        """
        Read data from the file <name> in the current working directory for the
        user issuing the request and return the first hundred characters in it
        """
        if file_name == "":
            self.read_command_count = 0
            return "Current file is closed"
        if self.read_command_count == 0 and not read_flag:
            try:
                first = self.read_command_count*100
                with open(f"{self.fd}/{file_name}.txt") as file:
                    text_file = "".join(line.rstrip() for line in file)
                    charr = text_file[first:first+100]
                    first += 100
            except FileNotFoundError as error:
                msg = f'{error}.\n\r'
                return msg
            else:
                msg = f'\n\r{charr}\n\r'
                self.read_command_count += 1
                return msg
        if read_flag:
            try:
                first = self.read_command_count*100
                with open(f"{self.fd}/{file_name}.txt") as file:
                    text_file = "".join(line.rstrip() for line in file)
                    charr = text_file[first:first+100]
                    first += 100
            except FileNotFoundError as error:
                msg = f"{error}.\n\r"
                return msg
            else:
                msg = f'\n\r{charr}\n\r'
                self.read_command_count += 1
                return msg
        if self.read_command_count != 0 and not read_flag:
            self.read_command_count = 0
            try:
                first = self.read_command_count*100
                with open(f"{self.fd}/{file_name}.txt") as file:
                    text_file = "".join(line.rstrip() for line in file)
                    charr = text_file[first:first+100]
                    first += 100
            except FileNotFoundError as error:
                msg = f'{error}.\n\r'
                return msg
            else:
                msg = f'\n\r{charr}\n\r'
                self.read_command_count += 1
                return msg

    def write_file(self, name, file_name, user_input):
        """
        Write the data in <input> to the end of the file <name> in the current
        working directory for the user issuing the request, starting on a new line.
        If no file exists with the given name_file, a new file will be created in the
        current working directory for the user
        """
        if user_input == '':
            with open(f'{file_name}.txt', 'w') as writefile:
                writefile.writelines(f'{user_input}')
        else:
            with open(f'{file_name}.txt', 'a') as writefile:
                writefile.writelines(f'{user_input}\n')

class Admin(User):
    """
    A service for users just with admin privilege. This class inherit from user class,
    so it uses from all of its methods,including its constructor. So the attributes of
    admin class is the same as user class.

    Methods:
    ------------------------
    delete(name, user_name, input_password, signedin):
        Delete the user conforming with <username> from the server
    """

    def delete(self, name, user_name, input_password, signedin):
        """Delete the user conforming with <username> from the server"""
        os.chdir(init_cwd)
        with open(f'{init_cwd}/root/Server/client-info.json', 'r') as file:
            self.registered = json.load(file)

        index = self.registered['client_name'].index(name)
        admin_password = self.registered['client_password'][index]

        if user_name in self.registered['client_name']:
            if admin_password == input_password:
                user_name_index = self.registered['client_name'].index(user_name)
                user_name_privilege = self.registered['client_privilege'][user_name_index]

                with open(f'{init_cwd}/root/Server/client-info.json', 'r') as file:
                    self.registered = json.load(file) 
                del self.registered['client_name'][user_name_index]
                del self.registered['client_password'][user_name_index]
                del self.registered['client_privilege'][user_name_index]
                with open(f'{init_cwd}/root/Server/client-info.json', 'w') as file:
                    json.dump(self.registered, file)

                with open(f'{init_cwd}/root/Server/signed-info.json', 'r') as file:
                    signedin = json.load(file)
                try:
                    signedin.remove(user_name)
                except ValueError:
                    pass
                with open(f'{init_cwd}/root/Server/signed-info.json', 'w') as file:
                    json.dump(signedin, file)

                del_path = os.path.join(init_cwd, f"root/{user_name_privilege}/{user_name}")
                try:
                    shutil.rmtree(del_path, ignore_errors=True, onerror=None)
                except:
                    shutil.rmtree(del_path, ignore_errors=True, onerror=None)
                    msg = f'\n\rError : Error while deleting.\n\r'
                    return msg, user_name_index
                else:
                    msg = f'\n\rThe {user_name} successfuly has been deleted.\n\r'
                    return msg, user_name_index
                # finally:
                #     os.rmdir(del_path)
                # msg = f'\n\rThe {user_name} successfuly has been deleted.\n\r'
                # return msg           
                with open(f'{init_cwd}/root/Server/client-info.json', 'w') as file:
                    json.dump(self.registered, file)
            else:
                msg = f'\n\rThe request is denied.The password is wrong.\n\r'
                return msg
        else:
            msg = f'\n\rThe request is denied.The username does not exist.\n\r'
            return msg


class UserClassTestingStepOne(unittest.TestCase):
    """Handles the first part of tests"""

    def test_create_folder(self):
        """This is a test for create_folder functions"""
        name = "user1"
        password = "pass1"
        privilege = "admin"
        self.login_directory = f"root/{privilege}/{name}"
        self.fd = os.path.join(init_cwd, self.login_directory)
        path = os.path.join(self.fd, name)
        os.makedirs(path)

        client = Admin(name, password, privilege)

        expected_result = "The folder has been made successfully\n\r"
        result = client.create_folder("user1", "admin", "folder1")

        self.assertEqual(result,
                         expected_result,
                         f'Expected the answer to be : {expected_result}')

        chdir_path = os.path.join(init_cwd, f"root/{privilege}")
        os.chdir(chdir_path)
        del_path = os.path.join(init_cwd, f"root/{privilege}/{name}")
        shutil.rmtree(del_path)

    def test_change_folder(self):
        """This is a test for change_folder functions"""
        name = "user1"
        password = "pass1"
        privilege = "admin"
        folder = "testfolder1"
        self.login_directory = f"root/{privilege}/{name}"
        self.fd = os.path.join(init_cwd, self.login_directory)
        path = os.path.join(self.fd, folder) #init_cwd+f"root/{privilege}/{name}"+
        os.makedirs(path)

        client = Admin(name, password, privilege)

        expected_result = os.path.join(init_cwd, f"root/{privilege}/{name}\\{folder}")
        result = client.change_folder(name, privilege, folder)

        self.assertEqual(result,
                         expected_result,
                         f'Expected the answer to be : {expected_result}')

        chdir_path = os.path.join(init_cwd, f"root/{privilege}")
        os.chdir(chdir_path)
        del_path = os.path.join(init_cwd, f"root/{privilege}/{name}")
        shutil.rmtree(del_path)

    def test_back_folder(self):
        """This is a test for back_folder functions"""
        name = "user1"
        password = "pass1"
        privilege = "admin"
        self.login_directory = f"root/{privilege}/{name}"
        self.fd = os.path.join(init_cwd, self.login_directory)
        os.makedirs(self.fd)

        client = Admin(name, password, privilege)

        self.fd = f"{init_cwd}\\root"
        expected_result = f"{init_cwd}\\root/{privilege}"
        result = client.back_folder(name, privilege)

        self.assertEqual(result,
                        expected_result,
                        f'Expected the answer to be : {expected_result}')

        chdir_path = os.path.join(init_cwd, f"root/{privilege}")
        os.chdir(chdir_path)
        del_path = os.path.join(init_cwd, f"root/{privilege}/{name}")
        shutil.rmtree(del_path)

    def test_print_list(self):
        """This is a test for print_list functions"""
        name = "user1"
        password = "pass1"
        privilege = "admin"
        folder = "testfolder1"
        self.login_directory = f"root/{privilege}/{name}"
        self.fd = os.path.join(init_cwd, self.login_directory)
        path = os.path.join(self.fd, folder)

        os.makedirs(path)
        os.chdir(self.fd)
        with open('testfile1.txt', 'w') as writefile:    #Find proper command
                writefile.writelines("""It was the White Rabbit, trotting slowly back again, and looking
                                     anxiously about as it went, as if it had lost something; and she 
                                     heard it muttering to itself `The Duchess! The Duchess! Oh my dear
                                     paws! Oh my fur and whiskers! She'll get me executed, as sure as 
                                     ferrets are ferrets! Where CAN I have dropped them, I wonder?""")

        client = Admin(name, password, privilege)

        expected_results = ["testfile1.txt", "testfolder1"]
        result = client.print_list(name)

        for expected_result in expected_results:
            self.assertIn(expected_result,
                            result,
                            f'Expected the answer contains the following files : {expected_result}')

        chdir_path = os.path.join(init_cwd, f"root/{privilege}")
        os.chdir(chdir_path)
        del_path = os.path.join(init_cwd, f"root/{privilege}/{name}")
        shutil.rmtree(del_path)

    def test_write_file(self):
        """This is a test for write_file functions"""
        name = "user1"
        password = "pass1"
        privilege = "admin"
        file_name = "testfile1"
        user_input = "This is a test file."
        self.login_directory = f"root/{privilege}/{name}"
        self.fd = os.path.join(init_cwd, self.login_directory)
        path = os.path.join(self.fd, name)
        
        os.makedirs(path)
        os.chdir(self.fd)
        

        client = Admin(name, password, privilege)
        client.write_file(name, file_name, user_input)

        expected_result = user_input

        with open(f"{self.fd}/{file_name}.txt") as file:
            text_file = "".join(line.rstrip() for line in file)
            result = text_file[:]

        self.assertEqual(result,
                        expected_result,
                        f'Expected the answer to be : {expected_result}')

        chdir_path = os.path.join(init_cwd, f"root/{privilege}")
        os.chdir(chdir_path)
        del_path = os.path.join(init_cwd, f"root/{privilege}/{name}")
        shutil.rmtree(del_path)      

    def test_delete_as_an_admin(self):
        """
        This is a test for delete functions
        """
        name = "user1"
        password = "pass1"
        input_password = "pass1"
        privilege = "admin"

        user_name = "user2"
        user_pass = "pass2"
        user_privelege = "admin"

        file_name = "testfile2"
        user_input = "This is a test file."
        self.login_directory = f"root/{privilege}/{name}"
        self.fd = os.path.join(init_cwd, self.login_directory)

        signedin = ["user1", "user2"]
        with open(f'{init_cwd}/root/Server/signed-info.json', 'w') as file:
            json.dump(signedin, file)
        
        with open(f'{init_cwd}/root/Server/client-info.json', 'r') as file:
            registered = json.load(file)

        registered['client_name'].append(name)
        registered['client_password'].append(password)
        registered['client_privilege'].append(privilege)

        registered['client_name'].append(user_name)
        registered['client_password'].append(user_pass)
        registered['client_privilege'].append(user_privelege)

        with open(f'{init_cwd}/root/Server/client-info.json', 'w') as file:
            json.dump(registered, file)

        user1_path = os.path.join(init_cwd, f"root/{privilege}/{name}")
        os.makedirs(user1_path)
        user2_path = os.path.join(init_cwd, f"root/{privilege}/{user_name}")
        os.makedirs(user2_path)

        os.chdir(os.path.join(init_cwd, f"root/{privilege}/user2"))

        with open(f'{file_name}.txt', 'w') as writefile:
                writefile.writelines(user_input)
        client = Admin(name, password, privilege)


        expected_result = f'\n\rThe {user_name} successfuly has been deleted.\n\r'
        print(f'expected_result:{expected_result}')
        result = client.delete(name, user_name, input_password, signedin)
        print(result)
        print(expected_result)
        self.assertEqual(result,
            expected_result,
            f'Expected the answer to be : {expected_result}')
        
        with open(f'{init_cwd}/root/Server/client-info.json', 'r') as file:
            registered = json.load(file)
        user_name_index = registered['client_name'].index(name)
        del registered['client_name'][user_name_index]
        del registered['client_password'][user_name_index]
        del registered['client_privilege'][user_name_index]
        with open(f'{init_cwd}/root/Server/client-info.json', 'w') as file:
            json.dump(registered, file)

        with open(f'{init_cwd}/root/Server/signed-info.json', 'r') as file:
            signedin = json.load(file)
        signedin.remove(name)
        with open(f'{init_cwd}/root/Server/signed-info.json', 'w') as file:
            json.dump(signedin, file)

        chdir_path = os.path.join(init_cwd, f"root/{privilege}")
        os.chdir(chdir_path)
        del_path = os.path.join(init_cwd, f"root/{privilege}/{name}")
        shutil.rmtree(del_path) 

    # def test_read_files_first_100_char(self):
    #     """This is a test for read_files functions"""
    #     name = "user1"
    #     password = "pass1"
    #     privilege = "admin"
    #     # folder = "testfolder1"
    #     file_name = "testfile1"
    #     read_flag = False           #'False' means it is first time to read a file and 'True' means it is second or more times
    #     self.login_directory = f"root/{privilege}/{name}"
    #     self.fd = os.path.join(init_cwd, self.login_directory)
    #     path = os.path.join(self.fd, name)

    #     os.makedirs(path)
    #     os.chdir(self.fd)

    #     with open(f'{file_name}.txt', 'w') as writefile:
    #             writefile.writelines("""It was the White Rabbit, trotting slowly back again, and looking
    #                                  anxiously about as it went, as if it had lost something; and she 
    #                                  heard it muttering to itself `The Duchess! The Duchess! Oh my dear
    #                                  paws! Oh my fur and whiskers! She'll get me executed, as sure as 
    #                                  ferrets are ferrets! Where CAN I have dropped them, I wonder?""")

    #     client = Admin(name, password, privilege)

    #     expected_result = "\n\rIt was the White Rabbit, trotting slowly back again, and looking\n\r"
    #     print(f'expected_result:{expected_result}')
    #     result = client.read_file(file_name, read_flag)
    #     print(f'command  result:{result}')

    #     self.assertEqual(result,
    #                     expected_result,
    #                     f'Expected the answer to be : {expected_result}')

    #     chdir_path = os.path.join(init_cwd, f"root/{privilege}")
    #     os.chdir(chdir_path)
    #     del_path = os.path.join(init_cwd, f"root/{privilege}/{name}")
    #     shutil.rmtree(del_path)

    # assert 

if __name__ == "__main__":
    unittest.main()

