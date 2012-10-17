var WebServerURL = 'http://192.168.7.212:8080';
var SocketURL = "ws://192.168.7.212:8082";

function invokeWebApi(cmd, jdata, call){
    $.getJSON(WebServerURL+cmd+"?callback=?", jdata, call);
}

function getWebsocket(subcmd){
    return new WebSocket(SocketURL+subcmd);
}

function logout(){
     $.cookie('ticket', '', { expires: -1 });
     $.cookie('loginname', '', { expires: -1 });
     window.location = "login.html"
}

function getRequestParam(src,name){
    var params=src;
    var paramList=[];
    var param=null;
    var parami;
    if(params.length>0) {
        if(params.indexOf("&") >=0) {  // >=2 parameters
                paramList=params.split( "&" );
        } else {                       // 1 parameter
                paramList[0] = params;
        }
        for(var i=0,listLength = paramList.length;i<listLength;i++) {
            parami = paramList[i].indexOf(name+"=" );
            if(parami>=0) {
                param =paramList[i].substr(parami+(name+"=").length); //get value
                break;
            }
        }
    }
    return param;
}