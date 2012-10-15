$(document).ready(function(){
    createSessionList();
});

function createSessionList(){
    invokeWebApi("/test/session", {}, createSessionTable);
}

function createCaseSnaps(sid, tid){
    invokeWebApi('/test/caseresult/'+sid+'/'+tid+'/snapshot',
                {},
                function(data){
                    if(data.results === undefined) return;
                    for(var d in data.results.snaps) {
                        var ig = new Image();
                        ig.src = 'data:image/png;base64,' + d;
                        ig.width = '120px';
                        ig.height = '200px';
                        $('#snapsDiv').append(ig);
                }
    }); 
}

function createDetailTable(ids){

    var $div_detail = $("#detail_table");
    var $tb = $('<table>').attr('id', ids).attr('class','table table-striped');
    var $th = '<thead>'+
              '<tr>'+
              '<th align="left">StartTime</th>'+
              '<th align="left">TestCase</th>'+
              '<th align="left">Result</th>'+
              '<th align="left">Traceinfo</th>'+
              '<th align="left">Log</th>'+
              '<th align="left">Snapshot</th>'+
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
function showSnapDiv() {
    if(curSid !== "") createSnapshotDiv(curSid);
}

function showTestDiv() {
    if(curSid !== "") createCaseResultDiv(curSid);
}

function createSnapshotDiv(sid) {
    curSid = sid;

    $("#status_tab").removeClass('active');
    $("#snap_tab").addClass('active'); 

    $("#status_div").hide()
    $("#snap_div").show()

    if(ws !== undefined) ws.close();

    //screen snap channel
    ws = new WebSocket("ws://192.168.7.212:8082/test/session/"+sid+"/screen");
    var c=document.getElementById("myCanvas");
    var cxt=c.getContext("2d");

    //var imgdata=cxt.createImageData(480, 800);
    ws.onopen = function() {
        ws.send('sync:ok');
    };

    ws.onmessage = function (evt) {
        var data = evt.data;
        if (data.indexOf('snapsize:') >= 0 ) {
            data = data.substr('snapsize:'.length);
            data = JSON.parse(data);
            c.setAttribute('width',data['width']);
            c.setAttribute('height',data['height']);      
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

function createCaseResultDiv(sid) {
    curSid = sid;

    $("#status_tab").addClass('active');
    $("#snap_tab").removeClass('active');    
    $("#status_div").show()
    $("#snap_div1").hide()

    if(ws !== undefined) ws.close();
    //screen snap channel
    ws = new WebSocket("ws://192.168.7.212:8082/test/session/"+sid+"/terminal");

    ws.onopen = function() {
        ws.send('sync:ok');
    };

    ws.onmessage = function (evt) {
        var data = evt.data;
        if (data.indexOf('caseupdate:') >= 0 ) {  
            data = data.substr('caseupdate:'.length);
            doRender(data);
        } 
        ws.send('sync:ok');
    };

    function doRender(data) {
        $("#myTerminal").append(data+"\r\n");
    }
}


function fillDetailTable(data, ids, tag){

    var detail_table = $("#"+ids+" > tbody");

    if($("#"+ids).length>0){ //table exist?

        $("#"+ids+ " tr:gt(0)").remove(); //delete table content

        for (var i in data.results.cases){

            var ctime,cname,cresult,ctraceinfo,ctid,csid, trId;
            ctid=data.results.cases[i]['tid'];
            csid=data.results.cases[i]['sid'];           
            ctime=data.results.cases[i]['starttime'];
            cname=data.results.cases[i]['casename'];
            cresult=data.results.cases[i]['result'];
            ctraceinfo = 'N/A';

            if(tag !== 'all' && tag !== cresult) continue;
            if(cresult=='') cresult='running';
            if(cname=='') cname='missed';
            if(ctime=='') ctime='missed';
            casename = cname;
            trId="#"+ids+"_"+i;

            if(cresult=='fail'){

                detail_table.append("<tr id=\""+trId+"\">"+
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
                                        "<td><a href=\"http://192.168.7.212:8080/test/caseresult/"+csid+"/"+ctid+"/log\">log</a> </td>"+
                                        "<td><a id=\"f_"+ctid+"_"+i+"\" data-toggle=\"modal\" href=\"#myModal\" onclick=\"createCaseSnaps('"+csid+"','"+ctid+"');\">snapshot</a></td>"+
                                        "</tr>");

         }else if(cresult=='error') {

             detail_table.append("<tr id=\""+trId+"\">"+
                                     "<td>"+ctime+"</td>"+
                                     "<td>"+casename+"</td>"+
                                     "<td><font color=\"red\">"+cresult+"<font></td>"+
                                     "<td><a class=\"popup_link\" onfocus=\"this.blur();\" href=\"javascript:showTestDetail('div_"+ids+"_"+i+"')\">"+"detail"+"</a>"+
                                     "<div id='div_"+ids+"_"+i+"'class=\"popup_window\">"+
                                     "<div style=\"text-align: right; color:red;cursor:pointer\">"+
                                     "<a onfocus=\"this.blur();\" onclick=\"document.getElementById('div_"+ids+"_"+i+"').style.display ='none' \"> [x] </a>"+"</div>"+
                                     "<pre><h5>"+ctraceinfo+"</h5></pre> </div>"+"</td>"+
                                     "<td><a href=\"http://192.168.7.212:8080/test/caseresult/"+csid+"/"+ctid+"/log\">log</a> </td>"+
                                     "<td></td>"+
                                     "</tr>");

         }else if (cresult == 'running' || cresult == 'pass'){
             if (cresult == 'running'){
                detail_table.append("<tr id=\""+trId+"\">"+
                                     "<td>"+ctime+"</td>"+
                                     "<td>"+casename+"</td>"+
                                     "<td> <img src=\"static/img/running1.gif\" alt=\"running\" /> </td>"+
                                     "<td>"+ctraceinfo+"</td>"+
                                     "<td> </td>"+
                                     "<td> </td>"+
                                     "</tr>");     
             }else{    
                 detail_table.append("<tr id=\""+trId+"\">"+
                                     "<td>"+ctime+"</td>"+
                                     "<td>"+casename+"</td>"+
                                     "<td>"+cresult+"</td>"+
                                     "<td>"+ctraceinfo+"</td>"+
                                     "<td> </td>"+
                                     "<td> </td>"+
                                     "</tr>");
                 }    
             } }
    }
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

      //get target cycle fail list
      invokeWebApi('/test/caseresult/'+key,
                     {},
                    function(data){
                        createDetailTable(allTableId);
                        fillDetailTable(data,allTableId,'all');
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
            var $th = '<thead><tr><th>product</th><th>planname</th><th>revision</th><th>statrtime</th><th>runtime</th></tr></thead>';
            var $tbody = '<tbody></tbody>';
            $product_table.append($th);
            $product_table.append($tbody);
            //$product_div.append($product_label);
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
                      "<td><a href=\"javascript:createCaseResultDiv('"+key+"');javascript:createAllTestList('"+key+"')\">"+value+"</a></td>"+      
                      "<td>"+product_cycle_planname[key]+"</td>"+                        
                      "<td>"+product_cycle_revision[key]+"</td>"+                     
                      "<td>"+product_cycle_starttime[key]+"</td>"+
                      //"<td>"+"<a id="+allId+" href=\"javascript:void(0);\">"+product_cycle_result[key]['total']+"</a></td>"+
                      //"<td>"+"<a id="+passId+" href=\"javascript:void(0);\">"+product_cycle_result[key]['pass']+"</td>"+
                      //"<td>"+"<a id="+failId+" href=\"javascript:void(0);\">"+product_cycle_result[key]['fail']+"</td>"+
                      //"<td>"+"<a id="+errorId+" href=\"javascript:void(0);\">"+product_cycle_result[key]['error']+"</td>"+
                      "<td>"+setRunTime(product_cycle_runtime[key])+"s</td>"+
                      "</tr>";

                $product_table.append($tr);


                /*jQuery("#"+allId).click(function(){
                    var allTableId = 'alltable_'+key.replace('cycle:','');

                    //get target cycle fail list
                    invokeWebApi('/test/caseresult/'+key,
                                  {},
                                  function(data){
                                      createDetailTable(allTableId);
                                      fillDetailTable(data,allTableId,'all');
                                });
                });       

                jQuery("#"+failId).click(function(){
                    var failTableId = 'failtable_'+key.replace('cycle:','');

                    //get target cycle fail list
                    invokeWebApi('/test/caseresult/'+key,
                                {},
                                function(data){
                                    createDetailTable(failTableId);
                                    fillDetailTable(data,failTableId,'fail');
                                });

                });
               

                jQuery("#"+passId).click(function(){
                    var passTableId = 'passtable_'+key.replace('cycle:','');
                    
                    invokeWebApi('/test/caseresult/'+key,
                                  {},
                                  function(data){
                                    createDetailTable(passTableId);
                                    fillDetailTable(data,passTableId,'pass');
                                });
                });
               

                jQuery("#"+errorId).click(function(){
                    var errorTableId = 'errortable_'+key.replace('cycle:','');
                    invokeWebApi('/test/caseresult/'+key,
                                  {},
                                  function(data){
                                      fillDetailTable(data,errorTableId,'error');
                                });
                });*/
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
        var cycleimei = '0';
        var cycleruntime = item.runtime;
        var cycleendtime = ''

        if (cycleendtime==''){
            product_run_list[idx] = product;
            product_run_cycle_product[cycleid] = product;
            product_run_cycle_plan[cycleid] = planname;
            product_run_cycle_starttime[cycleid] = starttime;
            product_run_cycle_revision[cycleid] = revision;
            product_run_cycle_result[cycleid] = cycleresult;
            product_run_cycle_runtime[cycleid] = cycleruntime;
            product_run_cycle_userid[cycleid] = cycleuserid;
        } else {
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
        }
    });

    createRunningSessionDiv(arrayUnique(product_run_list),
                            product_run_cycle_product,
                            product_run_cycle_plan,                            
                            product_run_cycle_starttime,
                            product_run_cycle_runtime,
                            product_run_cycle_revision);
}
