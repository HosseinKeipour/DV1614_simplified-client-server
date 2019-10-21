import os
import asyncio
import json
import sys

class User:
    def __init__(self, name, password, privilege):
        self.name = name
        self.__password = password
        self.privilege = privilege

        self._index = 0

        self.user_list = []
        self.each_user = {'name': self.name, 'password': self.__password, 'privilege': self.privilege} # folder=[]
        self.user_list.append(self.each_user)
        

    def change_folder(self, name):
        pass

    def print_list(self):
        pass

    def read_file(self, name):
        pass

    def write_file(self, name, input):
        pass

    def create_folder(self, name, privilege, folder, reader, writer):
        # with open('root/Server/created_folder.json', 'r') as file:
        #     created_folder = json.load(file)

        parent_dir = f"root/{privilege}/{name}"
        path = os.path.join(parent_dir, folder)
        # path = f"root/{privilege}/{name}/{folder}"
        try:
            os.mkdir(path)
            writer.write("The folder has been made successfully\n\r".encode(encoding='UTF-8'))
        except OSError as error:
            print(error)
            writer.write("Error:Folder with this name exist. Try again\n\r".encode(encoding='UTF-8'))
        
        # for i in range(len(created_folder[name])):
            # if path == created_folder[name][i]:
            #     writer.write("Error: the created file had been made.Please make another file with new name".encode(encoding='UTF-8'))
            # else:                
            #     os.mkdir(path)
            #     created_folder[name].append(path)
            #     with open('root/Server/created_folder.json', 'w') as file:
            #         json.dump(created_folder, file)
            #     writer.write("The folder has been made successfully\n\r".encode(encoding='UTF-8'))

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

    def delete(self, username, password):
        pass
