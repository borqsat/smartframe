var apiBaseURL = window.location.protocol + "//" + window.location.hostname + (window.location.port ? ":" + window.location.port : "")+"/smartapi";
var storeBaseURL = apiBaseURL + "/fs";
var socketURL = apiBaseURL.replace(window.location.protocol, "ws:") + "/ws";

var _appglobal = function () {};

var _ajaxstart=function() {
    var winWidth=0;
    var winHeight=0;

    if(window.innerWidth) winWidth = window.innerWidth;	
    else if((document.body) && (document.body.clientWidth))  winWidth = document.body.clientWidth;

    if(window.innerHeight) winHeight = window.innerHeight;	
    else if((document.body) && (document.body.clientHeight)) winHeight = document.body.clientHeight;

    if(document.documentElement && document.documentElement.clientHeight && document.documentElement.clientWidth) {
        winHeight = document.documentElement.clientHeight;
        winWidth = document.documentElement.clientWidth;
    }

    if(document.getElementById('progress-img') !== undefined 
        && document.getElementById('progress-img') !== null ) {
	      document.getElementById('progress-img').style.left=""+(winWidth/2-70)+"px";
	      document.getElementById('progress-img').style.top=""+(winHeight/2)+"px";
	      document.getElementById('progress-img').innerHTML = "<a><img style='BORDER:none' src='static/img/loading.gif'></a>";   	
    }	    		    
};

var _ajaxend = function(){
    if(document.getElementById('progress-img') !== undefined && document.getElementById('progress-img') !== null )
        document.getElementById('progress-img').innerHTML = '';
};

var prepareData = function(data) {
    var dataj = data;
    dataj['token'] = $.cookie('ticket');
    dataj['appid'] = '02';
    return dataj;
}

/*
 * Http Get Request by Jquery Ajax
 */
var invokeWebApi = function(apiUrl,dataj,render,bprg) {
    var options = {}; 
    var funok = function(data) {
        if(data['results'] === undefined) {
           if(data['errors'] !== undefined) {
              alert(data['errors']['msg']);
              if(data['errors']['code'] === '01') window.location = "./login.html";
           } else alert("ERROR:Request failed, please retry!");
           _ajaxend();
        } else {
           render(data);
           _ajaxend();          
        }
    }
    var funerror = function(jqXHR, textStatus, errorThrown) {
        var err;
        if (textStatus !== "abort" && errorThrown === "Internal Server Error") {
            try {
                err = JSON.parse(jqXHR.responseText);
                alert(err.Message);
            } catch(e) {
                alert("ERROR: Request failed, please retry!");
            }
        }
    }
    if(bprg !== undefined) options['beforeSend'] = _ajaxstart;
    options['url'] = apiBaseURL + apiUrl;
    options['async'] = true;
    options['type'] = 'GET';
    options['data'] = dataj;
    options['dataType'] = 'json';
    options['timeout'] = 25000;
    options['success'] = funok;
    options['error'] = funerror;
			
    $.ajax(options);
}

/*
 * Http POST Request by Jquery Ajax
 */
var invokeWebApiEx = function(apiUrl,datap,render, formid) {
    var funok=function(data) {
        if(data['results'] === undefined) {
            if(data['errors'] !== undefined){
                alert(data['errors']['msg']);
            } else alert("ERROR:Request failed, please retry!");
        } else {
           render(data);
        }
    }
    var funerror = function(jqXHR, textStatus, errorThrown) {
        var err;
        if (textStatus !== "abort" && errorThrown === "Internal Server Error") {
            try {
                err = JSON.parse(jqXHR.responseText);
                alert(err.Message);
            } catch(e) {
                alert("ERROR:Request failed, please retry!");
            }
        }
    }
    var options = {};
    //options['beforeSend'] = _ajaxstart;
    options['url'] = apiBaseURL + apiUrl;
    options['async'] = false;
    options['type'] = 'POST';
    options['dataType'] = 'json';
    options['timeout'] = 15000;
    options['success'] = funok;
    options['error'] = funerror;
    if (formid === undefined) {
    	options['data'] = JSON.stringify(datap);
    	options['contentType']= "application/json;";
        $.ajax(options);
    }
    else{
    	options['data'] = datap;
    	options['contentType'] = "multipart/form-data;"
    	$('#'+formid).ajaxSubmit(options);
    }
}

function checkLogIn() {
    if($.cookie('ticket') === undefined || $.cookie('ticket') === null) {
        window.location = "./login.html";
    }
}

function logout(){
    invokeWebApi('/account/logout',
                  prepareData({}),
                  function (data){
                      $.cookie('ticket', '', { expires: -1 });
                      $.cookie('loginname', '', { expires: -1 });
                      window.location = "./login.html";
                  }
                )
}

function setRunTime(secs) {
    var seconds = Math.floor( secs % 60);
    var minute = Math.floor((secs / 60) % 60);
    var hour = Math.floor((secs / 3600));
    var result = '';
    if(hour>0) result += hour+'h';
    if(minute>0) result += minute+'m';
    if(seconds>=0) result += seconds+'s'; 
    return result; 
}

function getWebsocket(subcmd){
    try {
        var ws = new WebSocket(socketURL+subcmd);
        return ws;
    } catch (ex) {
        return null;
    }
}

function getRequestParam(src,name){
    var params = src;
    var paramList = [];
    var param = null;
    var parami;
    if(params.indexOf('#') >= 0)
       params = params.substr(0,params.indexOf('#'));
    if(params.length>0) {
        if(params.indexOf("&") >= 0) {  // >=2 parameters
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
