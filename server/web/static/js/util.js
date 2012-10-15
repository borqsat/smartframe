var WebServerURL = 'http://192.168.7.212:8080';

function invokeWebApi(cmd, jdata, call){
    $.getJSON(WebServerURL+cmd+"?callback=?", jdata, call);
}
