import os
import asyncio
import json
import sys
import time
import shutil
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
                    # # writer.write(name.encode(encoding='UTF-8'))
                    # # writer.write(">>".encode(encoding='UTF-8'))
                    # writer.write(path.encode(encoding='UTF-8'))
                    
                    self.fd = os.path.join(self.fd, folder)
                    print('if self.fd', self.fd)
                    cwd = str(os.getcwd())
                    return path
                # Caching the exception     
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
                    # writer.write(name.encode(encoding='UTF-8'))
                    # writer.write(">>".encode(encoding='UTF-8'))
                    # writer.write(path.encode(encoding='UTF-8'))
                    
                    self.fd = os.path.join(self.fd, folder)
                    print('self.fd:',self.fd)
                    # cwd = str(os.getcwd())
                    return path
                # Caching the exception     
                except: 
                    error = "Error:The folder does not exist. Try again\n\r"  
                    return error
            else:
                error = "Error: Your are not allowed to enter this folder.\n\r"  
                return error
        else:
            try:
                os.chdir(path) 
                # writer.write(name.encode(encoding='UTF-8'))
                # writer.write(">>".encode(encoding='UTF-8'))
                # writer.write(path.encode(encoding='UTF-8'))
                
                self.fd = os.path.join(self.fd, folder)
                cwd = str(os.getcwd())
                return path
            # Caching the exception     
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

        else:
            # writer.write("Error:You are in root directory\n\r".encode(encoding='UTF-8'))
            # writer.write(name.encode(encoding='UTF-8'))
            # writer.write(">>".encode(encoding='UTF-8'))
            # writer.write(self.fd.encode(encoding='UTF-8')) 
            pass
    
    def create_folder(self, name, privilege, folder, reader, writer):
        
        is_path = self.fd.find(f'{init_cwd}\\root/user/{name}')
        print(is_path)

        #if f'{init_cwd}\\root/User/{name}' in self.fd or privilege == "admin":
        if is_path >= 0 or privilege == "admin":
            path = os.path.join(self.fd, folder)
            try:
                os.makedirs(path)
                writer.write("The folder has been made successfully\n\r".encode(encoding='UTF-8'))
            except OSError:
                writer.write("Error: Folder with this name exist.\n\r".encode(encoding='UTF-8'))
        else:
            writer.write("Error: Your are not allowed to create folder here.\n\r".encode(encoding='UTF-8'))

    def print_list(self, name):
        return_msg = ''
        dir_file_list = os.listdir(self.fd)
        print('self.fd:',self.fd)
        print('dir_file_list:', dir_file_list)
        for i in range(len(dir_file_list)):
            path = os.path.join(self.fd, dir_file_list[i])
            size = 0
            date = 0
            if os.path.isfile(path):
                size = os.path.getsize(path)  
                date = os.path.getctime(path)

                info_msg = (f'{dir_file_list[i]}\tsize:{str(size)}\tdate:{time.ctime(date)}\n\r')
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

    def read_file(self, file_name, read_flag, reader, writer):
        if self.read_command_count == 0 and not read_flag:
            writer.write('if self.read_command_count == 0 and not read_flag:'.encode(encoding='UTF-8'))
            try:
                first = self.read_command_count*100
                print(f"{self.fd}/{file_name}")
                with open(f"{self.fd}/{file_name}.txt") as file:
                    text_file = "".join(line.rstrip() for line in file)
                    charr = text_file[first:first+100]
                    writer.write('\n\r'.encode(encoding='UTF-8'))
                    writer.write(f'{charr}\n\r'.encode(encoding='UTF-8'))
                    first += 100     
            except FileNotFoundError as error:
                writer.write(f"{error}.\n\r".encode(encoding='UTF-8'))


        if read_flag:
            writer.write('read_flag:'.encode(encoding='UTF-8'))
            try:
                first = self.read_command_count*100
                print(f"{self.fd}/{file_name}")
                with open(f"{self.fd}/{file_name}.txt") as file:
                    text_file = "".join(line.rstrip() for line in file)
                    charr = text_file[first:first+100]
                    writer.write('\n\r'.encode(encoding='UTF-8'))
                    writer.write(f'{charr}\n\r'.encode(encoding='UTF-8'))
                    first += 100     
            except FileNotFoundError as error:
                writer.write(f"{error}.\n\r".encode(encoding='UTF-8'))  
        if self.read_command_count != 0 and not read_flag:
            writer.write('self.read_command_count != 0 and not read_flag:'.encode(encoding='UTF-8'))
            self.read_command_count = 0
            try:
                first = self.read_command_count*100
                print(f"{self.fd}/{file_name}")
                with open(f"{self.fd}/{file_name}.txt") as file:
                    text_file = "".join(line.rstrip() for line in file)
                    charr = text_file[first:first+100]
                    writer.write('\n\r'.encode(encoding='UTF-8'))
                    writer.write(f'{charr}\n\r'.encode(encoding='UTF-8'))
                    first += 100    
            except FileNotFoundError as error:
                writer.write(f"{error}.\n\r".encode(encoding='UTF-8'))
        self.read_command_count += 1 
        if file_name == "":
            writer.write('file_name == ""'.encode(encoding='UTF-8'))
            self.read_command_count = 0

    def write_file(self, name, file_name, user_input, reader, writer):
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

    def delete(self, name, password, privilege, user_name, input_password, signedin, reader, writer):
   
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
                    writer.write(f'\n\rThe {user_name} successfuly has been deleted.\n\r'.encode(encoding='UTF-8'))
                except:
                    writer.write(f'\n\rError : Error while deleting.\n\r'.encode(encoding='UTF-8'))
                               
                with open(f'{init_cwd}/root/Server/client-info.json', 'w') as file:
                    json.dump(self.registered, file)    
            else:
                writer.write(f'\n\rThe password is wrong.\n\r'.encode(encoding='UTF-8'))

        else:
            writer.write(f'\n\rThe username does not exist.\n\r'.encode(encoding='UTF-8'))
