from dbstore import store

def registerDevice(token,jdata):
    """
    register a device to server-side

    @type token:string
    @param token:the access token return by auth
    @type jdata:JSON
    @param jdata:the info of device pass to server-side
                 {'deviceid':(string)value,'product':(string)value,'buildversion':(string)value,'height':(int)value,'width':(int)value}
    @rtype: JSON
    @return: ok-{'results':{'deviceid':(string)value}}
             error-{'errors':{'code':0,'msg':(string)info}} 
    """   
    pass

def unregisterDevice(token,deviceId):
    """
    unregister a device by id from server-side

    @type token:string
    @param token:the access token return by auth
    @type deviceId:JSON
    @param deviceId:the id of device
    @rtype: JSON
    @return: ok-{'results':{'did':(string)value}}
             error-{'errors':{'code':0,'msg':(string)info}} 
    """   
    pass

def remoteDeviceList(token):
    """ 
    Get list of devices accessiable in server-side

    @type token:string
    @param token:the access token return by auth
    @rtype: JSON
    @return: ok-{'results':[{dev1Info},{dev2Info},...]}
             error-{'errors':{'code':0,'msg':(string)info}} 
    """   
    pass

def remoteDeviceScreenStream(deviceId):
    """
    Maintain a websocket connection  for live-time screen stream
    This method invoked by browser-side

    @type deviceId:string
    @param deviceId:the deviceid
    """
    pass

def remoteDeviceConsoleStream(deviceId):
    """
    Maintain a websocket connection for live-time console stream
    This method invoked by browser-side

    @type deviceId:string
    @param deviceId:the deviceid
    """
    pass

def remoteDeviceLaunchTest(token,deviceId):
    """
    Lauch a test session in remote device
    This method invoked by browser-side

    @type token:string
    @param token:the access token return by auth
    @type deviceId:string
    @param deviceId:the deviceid
    @rtype: JSON
    @return: ok-{'results':1}
             error-{'errors':{'code':value,'msg':(string)info}}
    """
    pass
