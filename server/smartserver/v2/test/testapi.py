import requests
import json

def testAccountWithOutUidAPI():
    url = 'http://127.0.0.1:8081/smartapi/account'
    register= {
             'subc':'register', 
             'data':{'username': 'tttt', 'password': '1234', 'appid': '01', 'info': {'email': 'spritegzq@gmail.com'}}
            }
    forgotpasswd = {
             'subc':'forgotpasswd', 
             'data':{'email':'rui.huang@borqs.com'}
            }
    login = {
             'subc':'login', 
             'data':{'appid': '02', 'username': 'b260', 'password': 'e10adc3949ba59abbe56e057f20f883e'}
            }     
    headers = {'content-type' : 'application/json'}
    r = requests.post(url, data=json.dumps(register), headers=headers)
    print 'testAPI with sub---->register'
    print r.content
    r = requests.post(url, data=json.dumps(forgotpasswd), headers=headers)
    print 'testAPI with sub---->forgotpassword'
    print r.content
    r = requests.post(url, data=json.dumps(login), headers=headers)
    print 'testAPI with sub---->login'
    print r.content

def testAccountWithUidAPI():
    url = 'http://127.0.0.1:8081/smartapi/user/351f021bc0e143bf71b17e33c1547f70'
    changepasswd = {
             'subc':'changepasswd', 
             'data':{'token':'98166813da6fb15c8e201e34e9dfc65c','oldpassword':'123','newpassword':'1234'}
            }
    headers = {'content-type' : 'application/json'}
    r = requests.post(url, data=json.dumps(changepasswd), headers=headers)
    print 'testAPI with sub---->changepasswd'
    print r.content


if __name__ == "__main__":
	testAccountWithOutUidAPI()
    testAccountWithUidAPI()
