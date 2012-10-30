
var _appglobal = function () {};

$(function(){
    if($.cookie('loginname') !== undefined && $.cookie('loginname') !== null) {
        $('#logname').html($.cookie('loginname'));
    }
});

function createSessionList(){
    invokeWebApi("/test/session", {}, createSessionTable);
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

    $('#history_div').dialog({height: 640,
                              width:360,
                              resizable:false,
                              modal: true});

    var $snaplist = $('#img_list'); 
    $snaplist.html('');
    invokeWebApi('/test/caseresult/'+sid+'/'+tid+'/snapshot',
                {},
                function(data){
                    if(data.results === undefined) {
                        $snaplist.html('None');
                        return;
                    }
                    if(data.results.snaps.length === 0) {
                        $snaplist.html('None');
                        return;
                    }
                    for(var d in data.results.snaps) {
                        var $snapli = $('<li>');
                        var $ig = new Image();
                        $ig.src = 'data:image/png;base64,' + data.results.snaps[d];
                        $ig.setAttribute("width",parseInt(_appglobal.deviceinfo['width'])/2+"px");
                        $ig.setAttribute("height",parseInt(_appglobal.deviceinfo['height'])/2+"px");
                        $ig.setAttribute('class','thumbnail');
                        $snaplist.append($snapli);
                        $snapli.append($ig);
                    }
                    $("#history_div").jCarouselLite({
                        btnNext: ".next",
                        btnPrev: ".prev",
                        visible: 1
                    });
                });
}

function createDetailTable(ids){

    var $div_detail = $("#cases_div");
    var $tb = $('<table>').attr('id', ids).attr('class','table table-striped');
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

    $('#snap_div').dialog({height: 640,
                          width: 320,
                          resizable:false,
                          modal: true});

    if(ws !== undefined) {
        ws.close();
    }

    //screen snap channel
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
            c.setAttribute('width', parseInt(data['width'])/2 + 'px');
            c.setAttribute('height', parseInt(data['height'])/2 + 'px');      
        } else if (data.indexOf('snapshot:') >= 0 ) {
            data = data.substr('snapshot:'.length);
            doRenderImg(data);
        } 
        ws.send('sync:ok');
    };

    function doRenderImg(data) {
        var img = new Image();
        img.src = 'data:image/png;base64,' + data;
        cxt.drawImage(img,0,0,300,512);
    }
}

function fillDetailTable(data, ids, tag){

    var detail_table = $("#"+ids+" > tbody");

    if($("#"+ids).length > 0){ 
        $("#"+ids+ " tr:gt(0)").remove(); //delete table content
        for (var i in data.results.cases){
            var ctime,cname,cresult,ctraceinfo,ctid,csid, trId;
            var citem = data.results.cases[i];
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
                                        "<td><a class=\"popup_link\" onfocus=\"this.blur();\" href=\"javascript:showTestDetail('div_"+ids+"_"+i+"')\">"+"detail"+"</a>"+
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
                                     "<td><a class=\"popup_link\" onfocus=\"this.blur();\" href=\"javascript:showTestDetail('div_"+ids+"_"+i+"')\">"+"detail"+"</a>"+
                                     "<div id='div_"+ids+"_"+i+"'class=\"popup_window\">"+
                                     "<div style=\"text-align: right; color:red;cursor:pointer\">"+
                                     "<a onfocus=\"this.blur();\" onclick=\"document.getElementById('div_"+ids+"_"+i+"').style.display ='none' \"> [x] </a>"+"</div>"+
                                     "<pre><h5>"+ctraceinfo+"</h5></pre> </div>"+"</td>"+
                                     "<td><a href=\""+WebServerURL+"/test/caseresult/"+csid+"/"+ctid+"/log\">log</a> </td>"+
                                     "<td><a id=\"f_"+ctid+"_"+i+"\" href=\"javascript:showHistoryDiv('"+csid+"','"+ctid+"');\">snapshot</a></td>"+
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

    TablePage('#'+ids,30, 5);
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
    };  

    data.length=0;  
    for (var i in a){  
           data[data.length] = i;  
    }
    return data;  
}  

function createAllTestList(key) {
      var allTableId = 'alltable_'+key.replace('cycle:','');
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

    var $summary_table = $('<table>').attr('class','table table-bordered').attr('id','stable'+key);
    var $th = '<thead><tr><th>planname</th><th>statrtime</th><th>runtime</th></tr></thead>';
    var $tbody = '<tbody></tbody>';
    $('#summary_div').append($summary_table);
    $summary_table.append($th);
    $summary_table.append($tbody);

    $tr = "<tr>"+     
          "<td>"+data['planname']+"</td>"+    
          "<td>"+data['starttime']+"</td>"+
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

    var $summary_table = $('<table>').attr('class','table table-bordered').attr('id','stable'+key);
    var $th = '<thead><tr><th>planname</th><th>statrtime</th><th>runtime</th><th>all</th><th>pass</th><th>fail</th><th>error</th></tr></thead>';
    var $tbody = '<tbody></tbody>';
    $('#summary_div').append($summary_table);
    $summary_table.append($th);
    $summary_table.append($tbody);

    $tr = "<tr>"+     
          "<td>"+data['planname']+"</td>"+    
          "<td>"+data['starttime']+"</td>"+
          "<td>"+data['runtime']+"</td>"+
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
function createRunningSessionDiv(product_list,product_cycle_product,product_cycle_planname,product_cycle_starttime,product_cycle_runtime,product_cycle_revision){

    var plist = product_list;
    var $cycle_panel = $("#run_cycle_panel");
    for(var i = 0; i < plist.length; i++) {
        if(plist[i] === 'undefined') continue;
        if($("#ongoing"+plist[i]).length <=0 ){
            var $product_div = $('<div>').attr('id','ongoing'+plist[i]);
            //var $product_label = "<span class=\"label label-info\">"+plist[i]+"</span><span align=right>";
            var $product_table = $('<table>').attr('class','table table-bordered').attr('id','otable'+plist[i]);
            var $th = '<thead><tr><th width=\'50px\'>product</th><th width=\'250px\'>build</th><th width=\'50px\'>planname</th><th>statrtime</th></tr></thead>';
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
                      "<td><a href=\"view.html?sid="+key+"\" target=\"_blank\">"+value+"</a></td>"+      
                      "<td>"+product_cycle_revision[key]+"</td>"+  
                      "<td>"+product_cycle_planname[key]+"</td>"+                        
                      "<td>"+product_cycle_starttime[key]+"</td>"+
                      "</tr>";

                $product_table.append($tr);
            }
          }
       })
   }
}
//create html data content
function createFinishedSessionDiv(product_list,product_cycle_product,product_cycle_planname,product_cycle_result,product_cycle_starttime,product_cycle_endtime,product_cycle_revision){

    var plist = product_list;
    var $cycle_panel = $("#stop_cycle_panel");
    for(var i = 0; i < plist.length; i++) {
        if(plist[i] === 'undefined') continue;

        if($("#stoprun"+plist[i]).length <=0 ){
            var $product_div = $('<div>').attr('id','stoprun'+plist[i]);
            var $product_table = $('<table>').attr('class','table table-bordered').attr('id','otable'+plist[i]);
            var $th = '<thead><tr><th width=\'50px\'>product</th><th width=\'250px\'>build</th><th width=\'50px\'>planname</th><th>statrtime</th><th>all</th><th>pass</th><th>fail</th><th>error</th><th>endtime</th></tr></thead>';
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
                      "<td><a href=\"view.html?sid="+key+"\" target=\"_blank\">"+value+"</a></td>"+      
                      "<td>"+product_cycle_revision[key]+"</td>"+
                      "<td>"+product_cycle_planname[key]+"</td>"+                               
                      "<td>"+product_cycle_starttime[key]+"</td>"+
                      "<td>"+product_cycle_result[key]['total']+"</td>"+
                      "<td>"+product_cycle_result[key]['pass']+"</td>"+
                      "<td>"+product_cycle_result[key]['fail']+"</td>"+
                      "<td>"+product_cycle_result[key]['error']+"</td>"+
                      "<td>"+product_cycle_endtime[key]+"</td>"+
                      "</tr>";
                $product_table.append($tr);
            }
          }
       })
   }
}

function setRunTime(secs) {
    var minute = Math.floor((secs / 60) % 60);
    var hour = Math.floor((secs / 3600));
    if(hour>0) {
        return  hour+'h'+minute+'m';
    } else {
        return minute+'m';
    }        
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
        } else {
            product_run_list[idx] = product;
            product_run_cycle_product[cycleid] = product;
            product_run_cycle_plan[cycleid] = planname;
            product_run_cycle_starttime[cycleid] = starttime;
            product_run_cycle_revision[cycleid] = revision;
            product_run_cycle_result[cycleid] = cycleresult;
            product_run_cycle_runtime[cycleid] = cycleruntime;
            product_run_cycle_userid[cycleid] = cycleuserid;
        }
    });

    createRunningSessionDiv(arrayUnique(product_run_list),
                            product_run_cycle_product,
                            product_run_cycle_plan,                            
                            product_run_cycle_starttime,
                            product_run_cycle_runtime,
                            product_run_cycle_revision);

    createFinishedSessionDiv(arrayUnique(product_stop_list),
                            product_stop_cycle_product,
                            product_stop_cycle_plan,    
                            product_stop_cycle_result,                    
                            product_stop_cycle_starttime,
                            product_stop_cycle_endtime,
                            product_stop_cycle_revision);

}
