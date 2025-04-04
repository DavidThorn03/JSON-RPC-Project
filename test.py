import unittest, requests

from jsonrpcclient import request, parse, Ok

from c import getFunctionWithoutParam, getFunctionWithParam
import os

"""
-------------------------- RUN USING test_script.bat --------------------------------------------------------

"""

class MyTests(unittest.TestCase):
    def test_01_startup(self):
        self.assertEqual(getFunctionWithParam(5001, "startup", {"server_num": "2"}), "Server 2 started")
        self.assertEqual(getFunctionWithParam(5001, "startup", {"server_num": "3"}), "Server 3 started")

        self.assertEqual(getFunctionWithParam(5001, "startup", {"server_num": "2"}), "Server 2 already running")
        self.assertEqual(getFunctionWithParam(5001, "startup", {"server_num": "3"}), "Server 3 already running")

    def test_02_ping(self):
        # should return pong (work)
        self.assertEqual(getFunctionWithoutParam(5001, "ping"), "pong")
        self.assertEqual(getFunctionWithoutParam(5002, "ping"), "pong")
        self.assertEqual(getFunctionWithoutParam(5003, "ping"), "pong")
        
        # should return false (not work as servers arent up)
        self.assertFalse(getFunctionWithoutParam(5005, "ping"))
        self.assertFalse(getFunctionWithoutParam(3000, "ping"))

    def test_03_make_folder(self):
        # make folder
        # should return folder created (work)
        self.assertEqual(getFunctionWithParam(5001, "make_folder", {"folder_name": "test_folder1"}), "Folder test_folder1 created")
        self.assertEqual(getFunctionWithParam(5002, "make_folder", {"folder_name": "test_folder2"}), "Folder test_folder2 created")
        self.assertEqual(getFunctionWithParam(5003, "make_folder", {"folder_name": "test_folder3"}), "Folder test_folder3 created")

        # should return folder already exists (work)
        self.assertEqual(getFunctionWithParam(5001, "make_folder", {"folder_name": "test_folder1"}), "Folder test_folder1 already exists")
        self.assertEqual(getFunctionWithParam(5002, "make_folder", {"folder_name": "test_folder2"}), "Folder test_folder2 already exists")

        # should return false (not work as servers arent up)
        self.assertFalse(getFunctionWithParam(5005, "make_folder", {"folder_name": "test_folder"}))
        self.assertFalse(getFunctionWithParam(3000, "make_folder", {"folder_name": "test_folder"}))

    # DOESNT WORK??????
    def test_04_delete_folder(self):
        # delete folder
        # should return folder deleted (work)
        self.assertEqual(getFunctionWithParam(5001, "delete_folder", {"folder_name": "test_folder1"}), "Folder test_folder1 deleted")# says that access is denyed for folder
        self.assertEqual(getFunctionWithParam(5002, "delete_folder", {"folder_name": "test_folder2"}), "Folder test_folder2 deleted")
        self.assertEqual(getFunctionWithParam(5003, "delete_folder", {"folder_name": "test_folder3"}), "Folder test_folder3 deleted")

        # should return folder does not exist (work)
        self.assertEqual(getFunctionWithParam(5001, "delete_folder", {"folder_name": "test_folder1"}), "Folder test_folder1 does not exist")
        self.assertEqual(getFunctionWithParam(5002, "delete_folder", {"folder_name": "test_folder2"}), "Folder test_folder2 does not exist")

        # should return false (not work as servers arent up)
        self.assertFalse(getFunctionWithParam(5005, "delete_folder", {"folder_name": "test_folder"}))
        self.assertFalse(getFunctionWithParam(3000, "delete_folder", {"folder_name": "test_folder"}))

    def test_05_whoareyou(self):
        # should return server number and port number (work)
        self.assertEqual(getFunctionWithoutParam(5001, "whoareyou"), "Server Number: 1 Port Number: 5001")
        self.assertEqual(getFunctionWithoutParam(5002, "whoareyou"), "Server Number: 2 Port Number: 5002")
        self.assertEqual(getFunctionWithoutParam(5003, "whoareyou"), "Server Number: 3 Port Number: 5003")
        
        # should return false (not work as servers arent up)
        self.assertFalse(getFunctionWithoutParam(5005, "whoareyou"))
        self.assertFalse(getFunctionWithoutParam(3000, "whoareyou"))

    def test_06_get_version(self):
        # should return server version (work)
        self.assertTrue(getFunctionWithoutParam(5001, "get_version"))
        self.assertTrue(getFunctionWithoutParam(5002, "get_version"))
        self.assertTrue(getFunctionWithoutParam(5003, "get_version"))

        # should return false (not work as servers arent up)
        self.assertFalse(getFunctionWithoutParam(5005, "get_version"))
        self.assertFalse(getFunctionWithoutParam(3000, "get_version"))

    def test_07_search(self):
        # should return file found (work)
        self.assertEqual(getFunctionWithParam(5001, "search", {"file_name": "c.py"}), "File c.py exists")
        self.assertEqual(getFunctionWithParam(5002, "search", {"file_name": "s.py"}), "File s.py exists")
        self.assertEqual(getFunctionWithParam(5003, "search", {"file_name": "run_script.bat"}), "File run_script.bat exists")

        # should return file not found (work)
        self.assertEqual(getFunctionWithParam(5001, "search", {"file_name": "test_file1"}), "File test_file1 does not exist")
        self.assertEqual(getFunctionWithParam(5002, "search", {"file_name": "test_file2"}), "File test_file2 does not exist")

        # should return false (not work as servers arent up)
        self.assertFalse(getFunctionWithParam(5005, "search", {"file_name": "test_file"}))
        self.assertFalse(getFunctionWithParam(3000, "search", {"file_name": "test_file"}))
    
    
    def test_08_getFriends(self):
        # should return server number and friends (work)
        self.assertEqual(getFunctionWithoutParam(5001, "get_friends"), "Server 1 has friends: ['2', '3']")
        self.assertEqual(getFunctionWithoutParam(5002, "get_friends"), "Server 2 has friends: ['1', '3']")
        self.assertEqual(getFunctionWithoutParam(5003, "get_friends"), "Server 3 has friends: ['1', '2']")
        
        # should return false (not work as servers arent up)
        self.assertFalse(getFunctionWithoutParam(5005, "get_friends"))
        self.assertFalse(getFunctionWithoutParam(3000, "get_friends"))

    def test_09_heartbeat(self):
        # should return up servers (work)
        self.assertEqual(getFunctionWithoutParam(5001, "heart_beat"), "Sent from 1 Response from: ['2', '3']")
        self.assertEqual(getFunctionWithoutParam(5002, "heart_beat"), "Sent from 2 Response from: ['1', '3']")
        self.assertEqual(getFunctionWithoutParam(5003, "heart_beat"), "Sent from 3 Response from: ['1', '2']")
        
        # should return false (not work as servers arent up)
        self.assertFalse(getFunctionWithoutParam(5005, "heart_beat"))
        self.assertFalse(getFunctionWithoutParam(3000, "heart_beat"))

    def test_10_pass_msg(self):
        # should return message received (work)
        self.assertEqual(getFunctionWithParam(5001, "pass_msg", {"target": "1", "servers": ["1", "2", "3"]}), "Message received")
        self.assertEqual(getFunctionWithParam(5001, "pass_msg", {"target": "2", "servers": ["1", "2", "3"]}), "Message received")
        self.assertEqual(getFunctionWithParam(5001, "pass_msg", {"target": "3", "servers": ["1", "2", "3"]}), "Message received")
    
        # should return server not found (work)
        self.assertEqual(getFunctionWithParam(5001, "pass_msg", {"target": "4", "servers": ["1", "2", "3"]}), "Server not found")
        self.assertEqual(getFunctionWithParam(5001, "pass_msg", {"target": "5", "servers": ["1", "2", "3"]}), "Server not found")
        self.assertEqual(getFunctionWithParam(5001, "pass_msg", {"target": "3000", "servers": ["1", "2", "3"]}), "Server not found")

        # should return false (not work as servers arent up)
        self.assertFalse(getFunctionWithParam(5005, "pass_msg", {"target": "1", "servers": ["1", "2", "3"]}))
        self.assertFalse(getFunctionWithParam(3000, "pass_msg", {"target": "1", "servers": ["1", "2", "3"]}))

    def test_11_shutdown(self):
        # should return server shutdown (work)
        self.assertFalse(getFunctionWithoutParam(5001, "shutdown"))
        self.assertFalse(getFunctionWithoutParam(5002, "shutdown"))
        self.assertFalse(getFunctionWithoutParam(5003, "shutdown"))


if __name__ == '__main__':
    unittest.main()


    #current issues
    # delete folder doesnt work, says access is denied ONLY IN TEST CASE doing same i normal run works????
    # shutdown doesnt work, dont know how to shut down and send message