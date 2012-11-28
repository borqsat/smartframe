
var _appglobal = function () {};

$(function(){
    if($.cookie('loginname') !== undefined && $.cookie('loginname') !== null) {
        $('#logname').html($.cookie('loginname'));
    }
});

function createSessionList(){
    invokeWebApi("/test/session", {}, createSessionTable);
}


function initMainPage(){
    createSessionList();
    setTimeout(initMainPage, 20000);
}

function viewRun(){
    $('#tabrun').addClass('active');
    $('#tabstop').removeClass('active');
    $('#run_cycle_panel').show();
    $('#stop_cycle_panel').hide();    
}

function viewStop(){
    $('#tabrun').removeClass('active');
    $('#tabstop').addClass('active');
    $('#run_cycle_panel').hide();
    $('#stop_cycle_panel').show();    
}

function createCaseSnaps(sid, tid){
    var $snaplist = $('#img_list'); 
    $snaplist.html('');

    var zoom = 1;
    var wd = parseInt(_appglobal.deviceinfo['width']) >> zoom;
    var ht = parseInt(_appglobal.deviceinfo['height']) >> zoom;
    $('#history_div').dialog({title:"case snapshots",
                              height: ht + 160,
                              width: 2*wd + 80,
                              resizable:false,
                              modal: true});

    invokeWebApi('/test/caseresult/'+sid+'/'+tid+'/snapshot',
                {},
                function(data){
                    if(data.results === undefined) {
                        $snaplist.html('None');
                        return;
                    } else if(data.results.snaps.length === 0) {
                        $snaplist.html('None');
                        return;
                    }
                    var idx = 0;
                    var total = data.results.snaps.length;
                    for(var d in data.results.snaps) {
                        ++idx;
                        var $snapli = $('<div>');
                        var $igdiv = $('<div>');
                        var $icgdiv = $('<div>');                                
                        var $ig = new Image();
                        var $icg = new Image();
                        var title = '';
                        var rect = '';
                        $ig.src = 'data:image/png;base64,' + data.results.snaps[d]['data'];
                        $ig.setAttribute("id","snap"+idx);                        
                        $ig.setAttribute("width",wd+"px");
                        $ig.setAttribute("height",ht+"px");
                        if((idx === total) && (data.results.checksnap !== undefined)) {
                            $icg.src = 'data:image/png;base64,' + data.results.checksnap['data'];
                            $icg.setAttribute("width", wd + "px");
                            $icg.setAttribute("height", ht + "px");
                            $ig.setAttribute('class','thumbnail thumbnailr');
                            $icg.setAttribute('class','thumbnail thumbnaile'); 
                            title = data.results.checksnap['title']
                            rect = title.substring(title.indexOf('(')+1, title.indexOf(')'));
                            title = title.substring(0, title.indexOf('('))
                            var x = parseInt(rect.substring(rect.indexOf('x')+1, rect.indexOf('y'))) >> zoom;
                            var y = parseInt(rect.substring(rect.indexOf('y')+1, rect.indexOf('w'))) >> zoom;
                            var w = parseInt(rect.substring(rect.indexOf('w')+1, rect.indexOf('h'))) >> zoom;
                            var h = parseInt(rect.substring(rect.indexOf('h')+1)) >> zoom;
                            $igdiv.append($ig);
                            $icgdiv.append($icg);   
                            var $pdiv = $('<div>').attr('style','border:3px solid green; position:absolute; top:'+y+'px; left:'+x+'px; width:' +w+'px; height:'+h+'px');
                            $icgdiv.append($pdiv);
                            $snapli.append($icgdiv); 
                            $snapli.append($igdiv);
                            $icgdiv.attr('style','float:left');
                            $igdiv.attr('style','float:left');
                            $snapli.attr('class','active item');                                                 
                        } else {
                            $ig.setAttribute('class','thumbnail');
                            title = data.results.snaps[d]['title']
                            rect = title.substring(title.indexOf('(')+1, title.indexOf(')'));
                            title = title.substring(0, title.indexOf('('))
                            var x = parseInt(rect.substring(rect.indexOf('x')+1, rect.indexOf('y'))) >> zoom;
                            var y = parseInt(rect.substring(rect.indexOf('y')+1, rect.indexOf('w'))) >> zoom;
                            var w = parseInt(rect.substring(rect.indexOf('w')+1, rect.indexOf('h'))) >> zoom;
                            var h = parseInt(rect.substring(rect.indexOf('h')+1)) >> zoom;
                            $igdiv.append($ig);
                            var $pdiv = $('<div>').attr('style','border:3px solid green; position:absolute; top:'+y+'px; left:'+x+'px; width:' +w+'px; height:'+h+'px');
                            $igdiv.append($pdiv).attr('style','float:left'); 
                            $snapli.append($igdiv); 
                            $snapli.attr('class','item');                                     
                        }
                         $snaptitle = $('<div>');
                         $snaptitle.html('<h3>('+idx+'/'+total+')'+ title +'</h3>');
                         //$snapli.append($snaptitle); 
                         $snaplist.append($snapli);                              
                    }
                    $('#history_div').carousel({"interval":100000,"pause":"hover"});
                }
            );


}

function createDetailTable(ids){

    var $div_detail = $("#cases_div");
    var $tb = $('<table>').attr('id', ids).attr('class','table table-striped table-hover');
    var $th = '<thead>'+
              '<tr>'+
              '<th align="left">id</th>'+
              '<th align="left">StartTime</th>'+
              '<th align="left">TestCase</th>'+
              '<th align="left">Result</th>'+
              '<th align="left">Traceinfo</th>'+
              '<th align="left">Log</th>'+
              '<th align="left">snaps</th>'+
              '</tr>'+
              '</thead>';
    var $tbody = '<tbody></tbody>';
    $tb.append($th);
    $tb.append($tbody);
    $div_detail.html($tb);
}

//for fail and error popup link
function showTestDetail(div_id){

    var details_div = document.getElementById(div_id)
    var displayState = details_div.style.display

    if (displayState != 'block' ) {
        displayState = 'block'
        details_div.style.display = 'block'
    }

    else {
        details_div.style.display = 'none'
    }
}

var curSid = "";
var ws = undefined;

function showSnapDiv(sid) {
    $("#history_div").hide();
    $("#snap_div").show();
    createSnapshotDiv(sid);
}

function showHistoryDiv(sid, tid) { 
    $("#history_div").show();
    $("#snap_div").hide();
    createCaseSnaps(sid, tid);
}

function createSnapshotDiv(sid) {

    if(ws !== undefined)  ws.close();
    var wd = parseInt(_appglobal.deviceinfo['width'])/2;
    var ht = parseInt(_appglobal.deviceinfo['height'])/2;
    $('#snap_div').dialog({
                            title:"case real-time snap",
                            height: ht+120,
                            width: wd+40,
                            resizable:false,
                            modal: true});
    ws = getWebsocket("/test/session/"+sid+"/screen");
    var c=document.getElementById("snapCanvas");
    var cxt=c.getContext("2d");

    ws.onopen = function() {
        ws.send('sync:ok');
    };

    ws.onmessage = function (evt) {
        var data = evt.data;
        if (data.indexOf('snapsize:') >= 0 ) {
            data = data.substr('snapsize:'.length);
            data = JSON.parse(data);
            c.setAttribute('width', wd + 'px');
            c.setAttribute('height', ht + 'px');      
        } else if (data.indexOf('snapshot:') >= 0 ) {
            data = data.substr('snapshot:'.length);
            doRenderImg(data);
        } 
        ws.send('sync:ok');
    };

    function doRenderImg(data) {
        var img = new Image();
        img.src = 'data:image/png;base64,' + data;
        cxt.drawImage(img,0,0,wd,ht);
    }
}

function processCasesData(data) {
    var datacases = data.results.cases;
    if(datacases !== undefined) {
        datacases.sort(function(a,b){ 
           return parseInt(b['tid']) - parseInt(a['tid']) ; 
        });
    }
    return datacases;
  
}

function fillDetailTable(data, ids, tag){

    var detail_table = $("#"+ids+" > tbody");

    data = processCasesData(data);

    if($("#"+ids).length > 0){ 
        $("#"+ids+ " tr:gt(0)").remove(); //delete table content
        for (var i in data){
            var cname,cresult,ctraceinfo,ctid,csid, trId;
            var citem = data[i];
            ctid = citem['tid'];
            csid = citem['sid'];
            ctime = citem['starttime'];
            cname = citem['casename'];
            cresult = citem['result'];
            ctraceinfo = citem['traceinfo'];

            if(cresult=='') cresult='running';
            if(cname=='') cname='missed';
            if(ctime=='') ctime='missed';

            if(tag !== 'all' && tag !== cresult) continue;
            casename = cname;
            trId="#"+ids+"_"+i;
            if(cresult=='fail'){
                detail_table.append("<tr id=\""+trId+"\">"+
                                        "<td>"+ctid+"</td>"+                  
                                        "<td>"+ctime+"</td>"+
                                        "<td>"+casename+"</td>"+
                                        "<td><font color=\"red\">"+cresult+"<font></td>"+
                                        "<td><a onfocus=\"this.blur();\" href=\"javascript:showTestDetail('div_"+ids+"_"+i+"')\">"+"detail"+"</a>"+
                                        "<div id='div_"+ids+"_"+i+"'class=\"popup_window\">" + 
                                        "<div style=\"text-align: right; color:red;cursor:pointer\">"+
                                        "<a onfocus=\"this.blur();\" onclick=\"document.getElementById('div_"+ids+"_"+i+"').style.display ='none' \"> [x] </a>"+
                                        "</div>" +
                                        "<pre><h5>"+ctraceinfo+"</h5></pre></div>"+
                                        "</td>"+
                                        "<td><a href=\""+WebServerURL+"/test/caseresult/"+csid+"/"+ctid+"/log\">log</a> </td>"+
                                        "<td><a id=\"f_"+ctid+"_"+i+"\" href=\"javascript:showHistoryDiv('"+csid+"','"+ctid+"');\">snapshot</a></td>"+
                                        "</tr>");

            } else if(cresult=='error') {

                detail_table.append("<tr id=\""+trId+"\">"+
                                     "<td>"+ctid+"</td>"+
                                     "<td>"+ctime+"</td>"+
                                     "<td>"+casename+"</td>"+
                                     "<td><font color=\"red\">"+cresult+"<font></td>"+
                                     "<td><a onfocus=\"this.blur();\" href=\"javascript:showTestDetail('div_"+ids+"_"+i+"')\">"+"detail"+"</a>"+
                                     "<div id='div_"+ids+"_"+i+"'class=\"popup_window\">"+
                                     "<div style=\"text-align: right; color:red;cursor:pointer\">"+
                                     "<a onfocus=\"this.blur();\" onclick=\"document.getElementById('div_"+ids+"_"+i+"').style.display ='none' \"> [x] </a>"+"</div>"+
                                     "<pre><h5>"+ctraceinfo+"</h5></pre> </div>"+"</td>"+
                                     "<td></td>"+
                                     "<td></td>"+
                                     //"<td><a href=\""+WebServerURL+"/test/caseresult/"+csid+"/"+ctid+"/log\">log</a> </td>"+
                                     //"<td><a id=\"f_"+ctid+"_"+i+"\" href=\"javascript:showHistoryDiv('"+csid+"','"+ctid+"');\">snapshot</a></td>"+
                                     "</tr>");

           } else if (cresult == 'running' || cresult == 'pass'){
                 if (cresult == 'running'){
                    detail_table.append("<tr id=\""+trId+"\">"+
                                        "<td>"+ctid+"</td>"+
                                        "<td>"+ctime+"</td>"+
                                        "<td>"+casename+"</td>"+
                                        "<td> <img src=\"static/img/running1.gif\" alt=\"running\" /> </td>"+
                                        "<td>"+ctraceinfo+"</td>"+
                                        "<td> </td>"+
                                        "<td> </td>"+
                                        "</tr>");     
                 } else {    
                    detail_table.append("<tr id=\""+trId+"\">"+
                                        "<td>"+ctid+"</td>"+
                                        "<td>"+ctime+"</td>"+
                                        "<td>"+casename+"</td>"+
                                        "<td>"+cresult+"</td>"+
                                        "<td>"+ctraceinfo+"</td>"+
                                        "<td> </td>"+
                                        "<td> </td>"+
                                        "</tr>");
                 }    
            } 
        }
    }

    TablePage('#'+ids, 20, 20);
}


//resort array
function arrayUnique__back(arr){
    var n = [];
    for(var i = 0; i < arr.length; i++){
        if(n.indexOf(arr[i]) == -1) n.push(arr[i]);
	  }
	  return n;
}

function arrayUnique(data){  
    data = data || [];  
    var a = {};  
    for (var i=0; i<data.length; i++) {  
        var v = data[i];  
        if (typeof(a[v]) == 'undefined'){  
            a[v] = 1;  
        }  
    }

    data.length=0;  
    for (var i in a){  
           data[data.length] = i;  
    }
    return data;  
}  

function createAllTestList(key) {
      var allTableId = 'alltable_' + key;
      invokeWebApi('/test/caseresult/'+key,
                   {},
                   function(data){
                       createDeviceInfo(data);
                       if(data['results'] !== undefined && data['results']['endtime'] !== 'N/A') {
                           createHistoryCaseSummary(data);
                           createDetailTable(allTableId);
                           fillDetailTable(data,allTableId,'all');                
                       } else {
                           createLiveCaseSummary(data);
                           createDetailTable(allTableId);
                           fillDetailTable(data,allTableId,'all');           
                           setTimeout("createAllTestList(\""+key+"\")",20000);
                       }

                  });
}

function createDeviceInfo(data) {

    data = data['results']['deviceinfo'];
    _appglobal.deviceinfo = data;
    
    var key = data['sid'];
    var allId = "o_"+key;
    var failId = 'fail_'+key;
    var passId = 'pass_'+key;
    var errorId = 'error_'+key;

    $('#device_div').html('');
    var $dev_table = $('<table>').attr('class','table table-bordered').attr('id','dtable'+key);
    var $th = '<thead><tr><th>product</th><th>build</th><th>width</th><th>height</th></tr></thead>';
    var $tbody = '<tbody></tbody>';
    $('#device_div').append($dev_table);
    $dev_table.append($th);
    $dev_table.append($tbody);

    $tr = "<tr>"+     
          "<td>"+data['product']+"</td>"+    
          "<td>"+data['revision']+"</td>"+
          "<td>"+data['width']+"</td>"+
          "<td>"+data['height']+"</td>"+          
          "</tr>";

    $dev_table.append($tr);
}

function createLiveCaseSummary(data) {
    data = data['results'];
    var key = data['sid'];
    var allId = "o_"+key;

    $('#summary_div').html('');
    var $summary_table = $('<table>').attr('class','table table-bordered').attr('id','stable'+key);
    var $th = '<thead><tr><th>planname</th><th>owner</th><th>statrtime</th><th>runtime</th><th></th></tr></thead>';
    var $tbody = '<tbody></tbody>';
    $('#summary_div').append($summary_table);
    $summary_table.append($th);
    $summary_table.append($tbody);

    $tr = "<tr>"+     
          "<td>"+data['planname']+"</td>"+    
          "<td>"+data['user']+"</td>"+
          "<td>"+data['starttime']+"</td>"+
          "<td>"+setRunTime(data['runtime'])+"</td>"+
          "<td>"+"<a id="+allId+" href=\"javascript:showSnapDiv(\'"+key+"\');\">livesnaps</a></td>"+
          "</tr>";

    $summary_table.append($tr); 
}

function createHistoryCaseSummary(data) {

    data = data['results'];
    var key = data['sid'];
    var allId = "o_"+key;
    var failId = 'fail_'+key;
    var passId = 'pass_'+key;
    var errorId = 'error_'+key;
    $('#summary_div').html('');
    var $summary_table = $('<table>').attr('class','table table-bordered').attr('id','stable'+key);
    var $th = '<thead><tr><th>planname</th><th>owner</th><th>statrtime</th><th>runtime</th><th>all</th><th>pass</th><th>fail</th><th>error</th></tr></thead>';
    var $tbody = '<tbody></tbody>';
    $('#summary_div').append($summary_table);
    $summary_table.append($th);
    $summary_table.append($tbody);

    $tr = "<tr>"+     
          "<td>"+data['planname']+"</td>"+    
          "<td>"+data['user']+"</td>"+
          "<td>"+data['starttime']+"</td>"+
          "<td>"+setRunTime(data['runtime'])+"</td>"+
          "<td>"+"<a id="+allId+" href=\"javascript:void(0);\">"+data['result']['total']+"</a></td>"+
          "<td>"+"<a id="+passId+" href=\"javascript:void(0);\">"+data['result']['pass']+"</a></td>"+
          "<td>"+"<a id="+failId+" href=\"javascript:void(0);\">"+data['result']['fail']+"</a></td>"+
          "<td>"+"<a id="+errorId+" href=\"javascript:void(0);\">"+data['result']['error']+"</a></td>"+
          "</tr>";

    $summary_table.append($tr);

    $("#"+allId).click(function(){
        var allTableId = 'alltable_'+key.replace('cycle:','');

        //get target cycle fail list
        invokeWebApi('/test/caseresult/'+key,
                    {},
                     function(data){
                        createDetailTable(allTableId);
                        fillDetailTable(data,allTableId,'all');
                    });
    });       

    $("#"+failId).click(function(){
        var failTableId = 'failtable_'+key.replace('cycle:','');

                    //get target cycle fail list
        invokeWebApi('/test/caseresult/'+key,
                      {},
                      function(data){
                          createDetailTable(failTableId);
                          fillDetailTable(data,failTableId,'fail');
                    });

    });

    $("#"+passId).click(function(){
          var passTableId = 'passtable_'+key.replace('cycle:','');
                    
          invokeWebApi('/test/caseresult/'+key,
                        {},
                        function(data){
                            createDetailTable(passTableId);
                            fillDetailTable(data,passTableId,'pass');
                      });
    });

    $("#"+errorId).click(function(){
          var errorTableId = 'errortable_'+key.replace('cycle:','');
          invokeWebApi('/test/caseresult/'+key,
                        {},
                        function(data){
                            createDetailTable(errorTableId);
                            fillDetailTable(data,errorTableId,'error');
                      });
    });
}

//create html data content
function createRunningSessionDiv(product_list,product_cycle_id,product_cycle_product,product_cycle_planname,product_cycle_owner,product_cycle_starttime,product_cycle_runtime,product_cycle_revision){

    var plist = product_list;
    var $cycle_panel = $("#run_cycle_panel");
    $cycle_panel.html('');
    for(var i = 0; i < plist.length; i++) {
        if(plist[i] === 'undefined') continue;
        if($("#ongoing"+plist[i]).length <=0 ){
            var $product_div = $('<div>').attr('id','ongoing'+plist[i]);
            //var $product_label = "<span class=\"label label-info\">"+plist[i]+"</span><span align=right>";
            var $product_table = $('<table>').attr('class','table table-bordered table-striped table-hover').attr('id','otable'+plist[i]);
            var $th = '<thead><tr><th width=\'50px\'>id</th><th width=\'50px\'>product</th><th width=\'250px\'>build</th><th width=\'50px\'>planname</th><th>owner</th><th>statrtime</th><th>runtime</th></tr></thead>';
            var $tbody = '<tbody></tbody>';
            $product_table.append($th);
            $product_table.append($tbody);
            $product_div.append($product_table);
            $cycle_panel.append($product_div);
        }

        $.each(product_cycle_product, function(key, value){

        if(value == plist[i]){
            var ids = key;
            var allId = "o_"+ids;
            var failId = 'fail_'+ids;
            var passId = 'pass_'+ids;
            var errorId = 'error_'+ids;

            if($("#"+allId).length<=0){
                $tr = "<tr>"+
                      "<td><a href=\"view.html?sid="+key+"\" target=\"_blank\">"+product_cycle_id[key]+"</a></td>"+ 
                      "<td>"+value+"</td>"+
                      "<td>"+product_cycle_revision[key]+"</td>"+  
                      "<td>"+product_cycle_planname[key]+"</td>"+
                      "<td>"+product_cycle_owner[key]+"</td>"+                        
                      "<td>"+product_cycle_starttime[key]+"</td>"+
                      "<td>"+setRunTime(product_cycle_runtime[key])+"</td>"+
                      "</tr>";

                $product_table.append($tr);
            }
          }
       })
   }
}

function deleteSessionById(sid) {
          
    if(confirm('Confirm to delete this session?')) {
       invokeWebApi('/test/session/'+sid+'/delete',
                    {},
                    function(data){ 
                       createSessionList();
                   });
   }

}

//create html data content
function createFinishedSessionDiv(product_list,product_cycle_id,product_cycle_product,product_cycle_planname,product_cycle_owner,product_cycle_result,product_cycle_starttime,product_cycle_runtime,product_cycle_revision){

    var plist = product_list;
    var $cycle_panel = $("#stop_cycle_panel");
    $cycle_panel.html('');
    for(var i = 0; i < plist.length; i++) {
        if(plist[i] === 'undefined') continue;

        if($("#stoprun"+plist[i]).length <=0 ){
            var $product_div = $('<div>').attr('id','stoprun'+plist[i]);
            var $product_table = $('<table>').attr('class','table table-bordered table-striped table-hover').attr('id','otable'+plist[i]);
            var $th = '<thead><tr><th width=\'50px\'>id</th><th width=\'50px\'>product</th><th width=\'150px\'>build</th><th width=\'50px\'>planname</th><th>owner</th><th>statrtime</th><th>runtime</th><th>all</th><th>pass</th><th>fail</th><th>error</th><th></th></tr></thead>';
            var $tbody = '<tbody></tbody>';
            $product_table.append($th);
            $product_table.append($tbody);
            $product_div.append($product_table);
            $cycle_panel.append($product_div);
        }

        $.each(product_cycle_product, function(key, value){

        if(value == plist[i]){
            var ids = key;
            var allId = "o_"+ids;
            var failId = 'fail_'+ids;
            var passId = 'pass_'+ids;
            var errorId = 'error_'+ids;

            if($("#"+allId).length<=0){
                $tr = "<tr>"+
                      "<td><a href=\"view.html?sid="+key+"\" target=\"_blank\">"+product_cycle_id[key]+"</a></td>"+
                      "<td>"+value+"</td>"+      
                      "<td>"+product_cycle_revision[key]+"</td>"+
                      "<td>"+product_cycle_planname[key]+"</td>"+                               
                      "<td>"+product_cycle_owner[key]+"</td>"+
                      "<td>"+product_cycle_starttime[key]+"</td>"+
                      "<td>"+setRunTime(product_cycle_runtime[key])+"</td>"+
                      "<td>"+product_cycle_result[key]['total']+"</td>"+
                      "<td>"+product_cycle_result[key]['pass']+"</td>"+
                      "<td>"+product_cycle_result[key]['fail']+"</td>"+
                      "<td>"+product_cycle_result[key]['error']+"</td>"+
                      "<td><a href=\"javascript:deleteSessionById('"+key+"')\">[X]</a></td>"+
                      "</tr>";
                $product_table.append($tr);
            }
          }
       })
   }
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

function createSessionTable(data){

    //step1: search data for 'productList'
    var product_run_list = new Array();
    var product_stop_list = new Array();
    var product_run_cycle_product = {};
    var product_stop_cycle_product = {};
    var product_stop_cycle_plan = {};
    var product_run_cycle_plan = {};
    var product_run_cycle_result = {};
    var product_stop_cycle_result = {};
    var product_run_cycle_runtime = {};
    var product_stop_cycle_runtime = {};
    var product_run_cycle_userid = {};
    var product_stop_cycle_userid = {};
    var product_stop_cycle_endtime = {};
    var product_run_cycle_revision = {};
    var product_stop_cycle_revision = {};
    var product_stop_cycle_imei = {};
    var product_stop_cycle_cyclestarttime = {};
    var product_run_cycle_starttime = {};
    var product_stop_cycle_starttime = {};
    var product_run_cycle_owner = {};
    var product_stop_cycle_owner = {};
    var product_run_cycle_id = {};
    var product_stop_cycle_id = {};

    $.each(data.results.sessions,function(idx,item){

        var cycleid = item.sid;       
        var cycleuserid = item.deviceid;
        var planname = item.planname;
        var product = item.deviceinfo['product'];
        var revision = item.deviceinfo['revision'];
        var starttime = item.starttime;
        var cycleresult = item.result;
        var cycleimei = 'N/A';
        var cyclestarttime = item.starttime;
        var cycleruntime = item.runtime;
        var cycleendtime = item.endtime;
        var cycleowner = item.user; 
        var cyclevid = item._id;

        if (cycleendtime !== '' && cycleendtime !== 'N/A'){
            product_stop_list[idx] = product;
            product_stop_cycle_product[cycleid] = product;
            product_stop_cycle_plan[cycleid] = planname;
            product_stop_cycle_starttime[cycleid] = starttime;            
            product_stop_cycle_result[cycleid] = cycleresult;
            product_stop_cycle_runtime[cycleid] = cycleruntime;
            product_stop_cycle_userid[cycleid] = cycleuserid;
            product_stop_cycle_endtime[cycleid] = cycleendtime;
            product_stop_cycle_revision[cycleid] = revision;
            product_stop_cycle_imei[cycleid] = cycleimei;
            product_stop_cycle_cyclestarttime[cycleid] = cyclestarttime;
            product_stop_cycle_owner[cycleid] = cycleowner;
            product_stop_cycle_id[cycleid] = cyclevid;
        } else {
            product_run_list[idx] = product;
            product_run_cycle_product[cycleid] = product;
            product_run_cycle_plan[cycleid] = planname;
            product_run_cycle_starttime[cycleid] = starttime;
            product_run_cycle_revision[cycleid] = revision;
            product_run_cycle_result[cycleid] = cycleresult;
            product_run_cycle_runtime[cycleid] = cycleruntime;
            product_run_cycle_userid[cycleid] = cycleuserid;
            product_run_cycle_owner[cycleid] = cycleowner;
            product_run_cycle_id[cycleid] = cyclevid;
        }
    });

    createRunningSessionDiv(arrayUnique(product_run_list),
                            product_run_cycle_id,
                            product_run_cycle_product,
                            product_run_cycle_plan, 
                            product_run_cycle_owner,                           
                            product_run_cycle_starttime,
                            product_run_cycle_runtime,
                            product_run_cycle_revision);

    createFinishedSessionDiv(arrayUnique(product_stop_list),
                            product_stop_cycle_id,
                            product_stop_cycle_product,
                            product_stop_cycle_plan,
                            product_stop_cycle_owner,    
                            product_stop_cycle_result,                    
                            product_stop_cycle_starttime,
                            product_stop_cycle_runtime,
                            product_stop_cycle_revision);

}
