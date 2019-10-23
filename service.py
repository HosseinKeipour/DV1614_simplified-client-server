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
        self.fd = os.path.join(os.getcwd(), self.login_directory)
        
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
        if self.fd != "C:\\Users\\EMKING\\ass3\\root":
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
            
        except OSError as error:
            print(error)
            writer.write("Error:Folder with this name exist. Try again\n\r".encode(encoding='UTF-8'))


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

    def read_file(self, name):
        pass

    def write_file(self, name, input):
        pass

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

    def delete(self, username, password):
        pass
