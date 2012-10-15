var WebServerURL = 'http://192.168.7.212:8080';
var SocketURL = "ws://192.168.7.212:8082";

function invokeWebApi(cmd, jdata, call){
    $.getJSON(WebServerURL+cmd+"?callback=?", jdata, call);
}

function getWebsocket(subcmd){
    return new WebSocket(SocketURL+subcmd);
}