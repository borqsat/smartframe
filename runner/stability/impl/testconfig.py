'''
EpyDoc
@version: $id$
@author: U{borqsat<www.borqs.com>}
@see: null
'''
class Account(object):
    '''
    A class for present user account info.
    '''
    def __init__(self):
        self.data = {}

    def add(self,properties):
        '''
        Add user info.
        '''
        key = properties[0]
        value = properties[1]
        self.data[key] = value

    def remove(self,property):
        pass

    def __getattribute__(self, name):
        try:
            v = object.__getattribute__(self, name)
        except AttributeError:
            d = self.data
            if d.has_key(name):
                v = d[name]
            else:
                raise
        return v

class SystemConfig(object):
    '''
    A class for present user account info.
    '''
    def __init__(self):
        self.data = {}

    def add(self,properties):
        '''
        Add user info.
        '''
        key = properties[0]
        value = properties[1]
        self.data[key] = value

    def remove(self,property):
        pass

    def __getattribute__(self, name):
        try:
            v = object.__getattribute__(self, name)
        except AttributeError:
            d = self.data
            if d.has_key(name):
                v = d[name]
            else:
                raise
        return v