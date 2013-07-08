import getpass
import hashlib
import base64
from ps import Topics,emit

class Authentication(object):
    @staticmethod
    def auth():
    	print '\nwhen enable --upload there requires accountname/password.\n'
        account = raw_input('Enter account name:\n')
        #password = hashlib.sha224(getpass.getpass('Enter password:\n')).hexdigest()
        password = base64.b64encode(getpass.getpass('Enter password:\n'))
        emit(Topics.AUTH, data={'account':account,'password':password})