import os
import asyncio
import json
import sys
import time
import shutil
import unittest
init_cwd = str(os.getcwd())


class User:
    def __init__(self, name,  password, privilege):
        self.name = name
        self.__password = password
        self.privilege = privilege
        
        
        self._index = 0
        self.user_list = []
        self.each_user = {'name': self.name, 'password': self.__password, 'privilege': self.privilege} 
        self.user_list.append(self.each_user)

        self.login_directory = f"root/{privilege}/{name}"
        
        self.fd = os.path.join(init_cwd, self.login_directory)

        self.read_command_count = 0

        with open(f'{init_cwd}/root/Server/client-info.json', 'r') as file:
            self.registered = json.load(file)     
    
        os.chdir(self.fd)

    def change_folder(self, name, privilege, folder):
        # some non existing directory 
        path = os.path.join(self.fd, folder)
        # cwd = str(os.getcwd())
        # trying to insert to flase directory 
        if self.fd == f"{init_cwd}\\root":
            if privilege == "admin" or "User" == folder :
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
                    # cwd = str(os.getcwd())
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
    
    def back_folder(self,name, privilege):

        if self.fd != f"{init_cwd}\\root":
            pathX = self.fd
            self.fd = os.path.dirname(pathX)
            # writer.write(name.encode(encoding='UTF-8'))
            # writer.write(">>".encode(encoding='UTF-8'))
            # writer.write(self.fd.encode(encoding='UTF-8'))
            msg = self.fd
            return msg

        else:
            # writer.write("Error:You are in root directory\n\r".encode(encoding='UTF-8'))
            # writer.write(name.encode(encoding='UTF-8'))
            # writer.write(">>".encode(encoding='UTF-8'))
            # writer.write(self.fd.encode(encoding='UTF-8'))
            msg = f"Error:You are in root directory\n\r{self.fd}"
            return msg
    
    def create_folder(self, name, privilege, folder):
        
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
                start_path = os.path.join(self.fd, dir_file_list[i]) # To get size of current directory
                date = os.path.getctime(path)

                for path, dirs, files in os.walk(start_path):
                    for f in files:
                        fp = os.path.join(path, f)
                        total_size += os.path.getsize(fp)

                info_msg = (f'{dir_file_list[i]}\t\tsize:{str(total_size)}\tdate:{time.ctime(date)}\n\r')
                return_msg += str(info_msg)

        return return_msg

    def read_file(self, file_name, read_flag):
        if file_name == "": # input is: read ""
            # writer.write('file_name == ""'.encode(encoding='UTF-8'))
            self.read_command_count = 0
            return "Current file is closed"

        if self.read_command_count == 0 and not read_flag: # run 1: read alice
            # writer.write('if self.read_command_count == 0 and not read_flag:'.encode(encoding='UTF-8'))
            try:
                first = self.read_command_count*100
                # print(f"{self.fd}/{file_name}")
                with open(f"{self.fd}/{file_name}.txt") as file:
                    text_file = "".join(line.rstrip() for line in file)
                    charr = text_file[first:first+100]
                    # writer.write('\n\r'.encode(encoding='UTF-8'))
                    # writer.write(f'{charr}\n\r'.encode(encoding='UTF-8'))
                    first += 100   
            except FileNotFoundError as error:
                # writer.write(f"{error}.\n\r".encode(encoding='UTF-8'))
                msg = f'{error}.\n\r'
                return msg
            else:
                msg = f'\n\r{charr}\n\r'
                self.read_command_count += 1
                return msg

        if read_flag: # input is: read ""
            # writer.write('read_flag:'.encode(encoding='UTF-8'))
            try:
                first = self.read_command_count*100
                # print(f"{self.fd}/{file_name}")
                with open(f"{self.fd}/{file_name}.txt") as file:
                    text_file = "".join(line.rstrip() for line in file)
                    charr = text_file[first:first+100]
                    # writer.write('\n\r'.encode(encoding='UTF-8'))
                    # writer.write(f'{charr}\n\r'.encode(encoding='UTF-8'))
                    first += 100
            except FileNotFoundError as error:
                # writer.write(f"{error}.\n\r".encode(encoding='UTF-8'))
                msg = f"{error}.\n\r"
                return msg                
            else:
                msg = f'\n\r{charr}\n\r'
                self.read_command_count += 1
                return msg

        if self.read_command_count != 0 and not read_flag: # run 1 another file : read bob
            # writer.write('self.read_command_count != 0 and not read_flag:'.encode(encoding='UTF-8'))
            self.read_command_count = 0
            try:
                first = self.read_command_count*100
                # print(f"{self.fd}/{file_name}")
                with open(f"{self.fd}/{file_name}.txt") as file:
                    text_file = "".join(line.rstrip() for line in file)
                    charr = text_file[first:first+100]
                    # writer.write('\n\r'.encode(encoding='UTF-8'))
                    # writer.write(f'{charr}\n\r'.encode(encoding='UTF-8'))
                    first += 100  
            except FileNotFoundError as error:
                # writer.write(f"{error}.\n\r".encode(encoding='UTF-8'))
                msg = f'{error}.\n\r'
                return msg
            else:
                msg = f'\n\r{charr}\n\r'
                self.read_command_count += 1
                return msg

        # self.read_command_count += 1 
        # if file_name == "": # input is: read ""
        #     # writer.write('file_name == ""'.encode(encoding='UTF-8'))
        #     self.read_command_count = 0
        #     return ""

    def write_file(self, name, file_name, user_input):
        if user_input == '':
            with open(f'{file_name}.txt', 'w') as writefile:    #Find proper command
                writefile.writelines(f'{user_input}')
        else:
            with open(f'{file_name}.txt', 'a') as writefile:
                writefile.writelines(f'{user_input}\n')

    def register(self, username, password, privileges):
        pass

    def login(self, username, password):
        pass
    
    def __iter__(self):
        return self

    def __len__(self):
        return len(self.user_list)

    def __next__(self):
        if len(self) == self._index:
            self._index = 0
            raise StopIteration
        self._index += 1
        return self.user_list[self._index-1]

class Admin(User):

    def delete(self, name, password, privilege, user_name, input_password, signedin):
   
        if user_name in self.registered['client_name']:
            index = self.registered['client_name'].index(name)
            admin_password = self.registered['client_password'][index]
            
            if admin_password ==  input_password:
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
                    signedin.remove(f'{user_name}')
                except ValueError:
                    pass
                with open(f'{init_cwd}/root/Server/signed-info.json', 'w') as file:
                    json.dump(signedin, file)

                del_path = os.path.join(init_cwd, f"root/{user_name_privilege}/{user_name}")
                try:
                    shutil.rmtree(del_path)
                    # writer.write(f'\n\rThe {user_name} successfuly has been deleted.\n\r'.encode(encoding='UTF-8'))
                except:
                    # writer.write(f'\n\rError : Error while deleting.\n\r'.encode(encoding='UTF-8'))
                    msg = f'\n\rError : Error while deleting.\n\r'
                    return msg
                else:
                    msg = f'\n\rThe {user_name} successfuly has been deleted.\n\r'
                    return msg
                               
                with open(f'{init_cwd}/root/Server/client-info.json', 'w') as file:
                    json.dump(self.registered, file)    
            else:
                # writer.write(f'\n\rThe password is wrong.\n\r'.encode(encoding='UTF-8'))
                msg = f'\n\rThe password is wrong.\n\r'
                return msg
        else:
            # writer.write(f'\n\rThe username does not exist.\n\r'.encode(encoding='UTF-8'))
            msg = f'\n\rThe username does not exist.\n\r'
            return msg

class UserClassTestingStepOne(unittest.TestCase):
    """Handles the first part of tests"""
    # registered = {'client_name': ["soheil", "vahid"], 'client_password': ["soheil", "vahid"], 'client_privilege': ["admin", "user"]}

    def test_create_folder(self):
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
        # print(result)

        self.assertEqual(result,
                        expected_result,
                        'Expected the answer to be : "The folder has been made successfully\n\r"')
        
        chdir_path = os.path.join(init_cwd, f"root/{privilege}")
        os.chdir(chdir_path)
        del_path = os.path.join(init_cwd, f"root/{privilege}/{name}")
        shutil.rmtree(del_path)

    # def test_change_folder(self):
    #     name = "user1"
    #     password = "pass1"
    #     privilege = "admin"
    #     self.login_directory = f"root/{privilege}/{name}"
    #     self.fd = os.path.join(init_cwd, self.login_directory)
    #     path = os.path.join(self.fd, name)
    #     os.makedirs(path)

    #     client = Admin(name, password, privilege)

    #     expected_result = os.path.join(init_cwd, f"root/{privilege}/folder1")
    #     result = client.change_folder("user1", "admin", "folder1")
        
        
    #     self.assertEqual(result,
    #                     expected_result,
    #                     f'Expected the answer to be : {os.path.join(self.fd, folder)}')

    #     chdir_path = os.path.join(init_cwd, f"root/{privilege}")
    #     os.chdir(chdir_path)
    #     del_path = os.path.join(init_cwd, f"root/{privilege}/{name}")
    #     shutil.rmtree(del_path)

if __name__ == "__main__":
    unittest.main()
