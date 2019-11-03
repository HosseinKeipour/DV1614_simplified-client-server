import unittest
from service import User
from service import Admin
import service

class UserClassTestingStepOne(unittest.TestCase):
    """Handles the first part of tests"""
    # registered = {'client_name': ["soheil", "vahid"], 'client_password': ["soheil", "vahid"], 'client_privilege': ["admin", "user"]}
    
    def test_create_folder(self):
        client = Admin("user1", "pass1", "admin")
        expected_result = "The folder has been made successfully\n\r"
        result = client.create_folder("user1", "admin", "folder1")
        print(result)

    def test_change_folder(self):

        client = User("user1", "pass1", "admin")

        client.change_folder("vahid", "admin", "vahidfolder")

        expected_result = True