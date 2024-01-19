##
## test_delegated_sharing.py - Some tests for delegated sharing (CS1620/2660)
##

import unittest
import string

import support.crypto as crypto
import support.util as util

from support.dataserver import dataserver, memloc
from support.keyserver import keyserver

# Import your client
#from client import create_user, authenticate_user

# Use this in place of the above line to test using the reference client
from dropbox_client_reference import create_user, authenticate_user


class DelegatedSharingTests(unittest.TestCase):
    def setUp(self):
        """
        This function is automatically called before every test is run. It
        clears the dataserver and keyserver to a clean state for each test case.
        """
        dataserver.Clear()
        keyserver.Clear()

    def test_chain(self):
        """Test sharing chain 1 -> 2 -> 3"""

        create_user("usr1", "pswd")
        create_user("usr2", "pswd")
        create_user("usr3", "pswd")
        
        u1 = authenticate_user("usr1", "pswd")
        u2 = authenticate_user("usr2", "pswd")
        u3 = authenticate_user("usr3", "pswd")

        u1.upload_file("shared_file", b'shared data')
        u1.share_file("shared_file", "usr2")
        u2.receive_file("shared_file", "usr1")
        u2.share_file("shared_file", "usr3")
        u3.receive_file("shared_file", "usr2")
        
        u1_file = u1.download_file("shared_file")
        u2_file = u2.download_file("shared_file")
        u3_file = u3.download_file("shared_file")

        self.assertEqual(u1_file, b'shared data')
        self.assertEqual(u2_file, b'shared data')
        self.assertEqual(u3_file, b'shared data')
    
    def test_chain_revoke(self):
        """Test sharing chain 1 -> 2 -> 3, both 2 & 3 lose access after 1 revokes file from 2"""
        
        create_user("usr1", "pswd")
        create_user("usr2", "pswd")
        create_user("usr3", "pswd")
        
        u1 = authenticate_user("usr1", "pswd")
        u2 = authenticate_user("usr2", "pswd")
        u3 = authenticate_user("usr3", "pswd")

        u1.upload_file("shared_file", b'shared data')
        u1.share_file("shared_file", "usr2")
        u2.receive_file("shared_file", "usr1")
        u2.share_file("shared_file", "usr3")
        u3.receive_file("shared_file", "usr2")
        
        u1.revoke_file("shared_file", "usr2")
        
        try:
            u2.download_file("shared_file")
            self.fail("Test Failed: User 2 should not be able to download file")
        except util.DropboxError:
            pass
        
        try:
            u3.download_file("shared_file")
            self.fail("Test Failed: User 3 should not be able to download file")
        except util.DropboxError:
            pass
        
    def test_tree(self):
        """Test sharing tree 1 => 2, 3; 2 => 4, 5; 3 => 6, 7"""
        
        create_user("usr1", "pswd")
        create_user("usr2", "pswd")
        create_user("usr3", "pswd")
        create_user("usr4", "pswd")
        create_user("usr5", "pswd")
        create_user("usr6", "pswd")
        create_user("usr7", "pswd")
        
        u1 = authenticate_user("usr1", "pswd")
        u2 = authenticate_user("usr2", "pswd")
        u3 = authenticate_user("usr3", "pswd")
        u4 = authenticate_user("usr4", "pswd")
        u5 = authenticate_user("usr5", "pswd")
        u6 = authenticate_user("usr6", "pswd")
        u7 = authenticate_user("usr7", "pswd")
        
        u1.upload_file("shared_file", b'shared data')
        


# Start the REPL if this file is launched as the main program
if __name__ == '__main__':
    util.start_repl(locals())