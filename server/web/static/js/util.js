var WebServerURL = "http://" + window.location.host + "/smartquery";
var SocketURL = "ws://ats.borqs.com:81";

var ajaxstart=function() {
     var winWidth=0;
     var winHeight=0;

     //获取窗口宽度	
     if(window.innerWidth) winWidth = window.innerWidth;	
     else if((document.body) && (document.body.clientWidth))	winWidth = document.body.clientWidth;
	 
     //获取窗口高度
     if(window.innerHeight) winHeight = window.innerHeight;	
     else if((document.body) && (document.body.clientHeight)) winHeight = document.body.clientHeight;
	
     //通过深入Document内部对body进行检测，获取窗口大小
     if(document.documentElement && document.documentElement.clientHeight && document.documentElement.clientWidth) {
         winHeight = document.documentElement.clientHeight;
         winWidth = document.documentElement.clientWidth;
     }

     if(document.getElementById('img') !== undefined && document.getElementById('img') !== null ) {
	 document.getElementById('img').style.left=""+(winWidth/2-70)+"px";
	 document.getElementById('img').style.top=""+(winHeight/2)+"px";
	 document.getElementById('img').innerHTML = "<a><img style='BORDER:none' src='static/img/loading.gif'></a>";   	
     }	    		    
}; 

var ajaxend = function(){
    if(document.getElementById('img') !== undefined && document.getElementById('img') !== null )
        document.getElementById('img').innerHTML = '';
};

/*
 * Http Get Request by Jquery Ajax
 */
var invokeWebApi = function(apiUrl,dataj,render) {
    var options = {}; 
    var funok=function(data) {
        if(data['results'] === undefined) {
           if(data['errors'] !== undefined) {
              alert(data['errors']['msg']);
              if(data['errors']['code'] === '01') window.location = "login.html";
           } else alert("Web server occurr unexpected error!");
           ajaxend();
        } else {
           render(data);
           ajaxend();          
        }
    };
    var funerror=function() {
        alert("Server Internal error!");
        ajaxend();
    };
    dataj['token'] = $.cookie('ticket');
    options['beforeSend'] = ajaxstart;
    options['url'] = WebServerURL + apiUrl;
    options['async'] = true;
    options['type'] = 'GET';
    options['data'] = dataj;
    options['dataType'] = 'jsonp';
    options['timeout'] = 15000;
    options['success'] = funok;
    options['error'] = funerror;
			
    $.ajax(options);
}

/*
 * Http POST Request by Jquery Ajax
 */
var invokeWebApiEx = function(apiUrl,datap,render) {
 
    var funok=function(data) {
        if(data['results'] === undefined) {
           if(data['errors'] !== undefined){
              alert(data['errors']['msg']);
              if(data['errors']['code'] === '01') window.location = "login.html";
           } else alert("Web server Internal error!");
           ajaxend();
        } else {
           render(data);
           ajaxend();          
        }
    };
    var funerror=function() {
        alert("Server Internal error!");
        ajaxend();
    };
    var options = {};
    options['beforeSend'] = ajaxstart;
    options['url'] = WebServerURL + apiUrl;
    options['type'] = 'POST';
    options['data'] = JSON.stringify(datap);
    options['contentType']= "application/json; charset=utf-8";
    options['dataType'] = 'json';
    options['timeout'] = 15000;
    options['success'] = funok;
    options['error'] = funerror;
      
    $.ajax(options);
}

function getWebsocket(subcmd){
    try {
        var ws = new WebSocket(SocketURL+subcmd);
        return ws;
    } catch (ex) {
        return null;
    }
}

function logout(){
     //invokeWebApi('/user/logout',
     //             {},
     //             function (data){
                      $.cookie('ticket', '', { expires: -1 });
                      $.cookie('loginname', '', { expires: -1 });
                      window.location = "login.html";
     //             }
     //            )
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
