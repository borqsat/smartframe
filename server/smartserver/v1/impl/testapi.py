
import requests
import json

def showResult():
    url = 'http://127.0.0.1:8081/smartapi/account'
    payload = {
             'action':'forgotpasswd', 
             'data':{'email':'rui.huang@borqs.com'}
            }
    headers = {'content-type' : 'application/json'}
    r = requests.post(url, data=json.dumps(payload), headers=headers)

#     print r.url

    print r.content
    
if __name__ == "__main__":
    showResult()