import os
import asyncio
import json
import sys
import time

class User:
    def __init__(self, name, password, privilege):
        self.name = name
        self.__password = password
        self.privilege = privilege

        self._index = 0

        self.user_list = []
        self.each_user = {'name': self.name, 'password': self.__password, 'privilege': self.privilege} # folder=[]
        self.user_list.append(self.each_user)
        self.login_directory = f"root\{privilege}\{name}"
        self.init_cwd = os.getcwd()
        self.fd = os.path.join(os.getcwd(), self.login_directory)
        self.read_command_count = 0

        with open('root/Server/client-info.json', 'r') as file:
            self.registered = json.load(file)        
    
        os.chdir(self.fd)
        
    def change_folder(self, name, privilege, folder, reader, writer):
        
        # some non existing directory 
        path = os.path.join(self.fd, folder)
        cwd = os.getcwd()
        print(f'cwd = {cwd}')
        print(f'path = {path}')
        
        # trying to insert to flase directory 
        try: 
            os.chdir(path) 
            writer.write(name.encode(encoding='UTF-8'))
            writer.write(">>".encode(encoding='UTF-8'))
            writer.write(path.encode(encoding='UTF-8'))
            self.fd = os.path.join(self.fd, folder)
            print(self.fd)
            cwd = os.getcwd()
            print(f'try cwd = {cwd}')
        # Caching the exception     
        except: 
            writer.write("Error:The folder does not exist. Try again\n\r".encode(encoding='UTF-8'))
            print("Something wrong with specified Exception- ")     
        # handling with finally           
        # finally: 
        #     print("Restoring the path") 
        #     os.chdir(cwd) 
        #     print("Current directory is-", os.getcwd()) 
    
    def back_folder(self,name, privilege, folder, reader, writer):
        if self.fd != f"{self.init_cwd}/root":
            pathX = self.fd  
            self.fd = os.path.dirname(pathX)
            writer.write(name.encode(encoding='UTF-8'))
            writer.write(">>".encode(encoding='UTF-8'))
            writer.write(self.fd.encode(encoding='UTF-8'))
        else:
            writer.write("Error:You are in root directory\n\r".encode(encoding='UTF-8'))
            writer.write(name.encode(encoding='UTF-8'))
            writer.write(">>".encode(encoding='UTF-8'))
            writer.write(self.fd.encode(encoding='UTF-8'))
    
    def create_folder(self, name, privilege, folder, reader, writer):
        
        path = os.path.join(self.fd, folder)
        # path2 = os.path.dirname(os.path.abspath(folder))
        # print(path2)
        try:
            os.makedirs(path)
            writer.write("The folder has been made successfully\n\r".encode(encoding='UTF-8'))
            
        except OSError:
            writer.write(f"Error: Cannot create a folder when folder {folder} already exists\n\r".encode(encoding='UTF-8'))

    def print_list(self, name, reader, writer):
        dir_file_list = os.listdir(self.fd)
        for i in range(len(dir_file_list)):
            path = os.path.join(self.fd, dir_file_list[i])
            size = 0
            date = 0
            if os.path.isfile(path):
                size = os.path.getsize(path)  
                date = os.path.getctime(path)

                writer.write(f'{dir_file_list[i]}'.encode(encoding='UTF-8'))
                writer.write(f'\tsize:{str(size)}'.encode(encoding='UTF-8'))
                writer.write(f'\tdate:{time.ctime(date)}'.encode(encoding='UTF-8'))

            elif os.path.isdir(path):
                total_size = 0
                start_path = os.path.join(self.fd, dir_file_list[i]) # To get size of current directory
                date = os.path.getctime(path)

                for path, dirs, files in os.walk(start_path):
                    for f in files:
                        fp = os.path.join(path, f)
                        total_size += os.path.getsize(fp)
                writer.write(f'{dir_file_list[i]}'.encode(encoding='UTF-8'))
                writer.write(f'\tsize:{str(total_size)}'.encode(encoding='UTF-8'))
                writer.write(f'\tdate:{time.ctime(date)}'.encode(encoding='UTF-8'))

            writer.write('\n'.encode(encoding='UTF-8'))

    def read_file(self, name, file_name, reader, writer):
        if file_name == "":
            self.read_command_count = 0 
        else:
            try:
                first = self.read_command_count*100
                with open(f"{file_name}.txt") as file:
                    text_file = "".join(line.rstrip() for line in file)
                    charr = text_file[first:first+100]
                    writer.write('\n\r'.encode(encoding='UTF-8'))
                    writer.write(f'{charr}\n\r'.encode(encoding='UTF-8'))
                    first += 100
                    self.read_command_count += 1         
            except FileNotFoundError as error:
                writer.write(f"{error}.\n\r".encode(encoding='UTF-8'))   

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

    # def __repr__(self):
    #     return

    # def __str__(self):
        # return
 
class Admin(User):

    def delete(self, name, password, privilege, user_name, input_password, reader, writer):
   
        if user_name in self.registered['client_name']:
            index = self.registered['client_name'].index(name)
            admin_password = self.registered['client_password'][index]
            
            if admin_password ==  input_password:
                user_name_index = self.registered['client_name'].index(user_name)
                del self.registered['client_name'][user_name_index]
                del self.registered['client_password'][user_name_index]
                del self.registered['client_privilege'][user_name_index]
                writer.write(f'\n\rThe {user_name} successfuly has been deleted.\n\r'.encode(encoding='UTF-8'))
               
                with open(f'{self.init_cwd}/root/Server/client-info.json', 'w') as file:
                    json.dump(self.registered, file)    
            else:
                writer.write(f'\n\rThe password is wrong.\n\r'.encode(encoding='UTF-8'))

        else:
            writer.write(f'\n\rThe username does not exist.\n\r'.encode(encoding='UTF-8'))

        # if username_check(name, self.registered['client_name']) == True:
        #     index = self.registered['client_name'].index(name)
        #     signedin.append(name)
        #     break
        # else:
        #     writer.write('\n\rError: This username is not exist. Please try again.'.encode(encoding='UTF-8'))

# def username_check(name1, name2):
#     for i in range(0, len(name2)):   
#         if name1 == name2[i]:
#             return True
#     return False