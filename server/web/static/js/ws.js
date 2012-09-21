//screen snap channel
var ws = new WebSocket("ws://192.168.7.212:8080/device/id/screenstream");
var c=document.getElementById("myCanvas");
var cxt=c.getContext("2d");

//var imgdata=cxt.createImageData(480, 800);
ws.onopen = function() {
    $("#timeline").append("Connect screensnap ok!\r\n");
    c.setAttribute('width','480px');
    c.setAttribute('height','800px');
    ws.send('sync');
};

ws.onmessage = function (evt) {
    if(evt.data !== 'null')
        doRenderImg(evt.data);
    else
        ws.send('sync');
};

function doRenderImg(data) {
    var img=new Image();
    img.onload = function () //确保图片已经加载完毕
    {
        cxt.drawImage(img,0,0);
        ws.send('sync');
    }
    img.src=data;
}
    
//adb channel
var wsd = new WebSocket("ws://192.168.7.212:8080/device/id/consolestream");
wsd.onopen = function() {
    $("#timeline").append("Connect adb shell ok!\r\n");
};

wsd.onmessage = function (evt) {
    $("#timeline").append(evt.data+"\r\n");
};

function doSend() {
    wsd.send($("#textmsg").val());
}