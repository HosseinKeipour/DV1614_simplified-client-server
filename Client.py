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

    def create_folder(self, name):
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
 
class Admin(User):

    def delete(self, username, password):
        pass
