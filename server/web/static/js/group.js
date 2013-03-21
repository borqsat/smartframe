function showGroupInfo(id) {
      invokeWebApi('/group/'+id+'/info',
                   prepareData({}),
                   function(data){
                       data = data.results;
                       if(data === undefined) return;
                       $('#group-name').parent().attr('href','#/group/'+id);
                       $('#group-name').html(data['groupname']);         
                       var $groupprf = $('#group-members').html('');
                       var members = data['members'];
                       _appglobal.members = [];
                       $.each(members,function(i, o) {
                           _appglobal.members.push(o['username']);
                           $groupprf.append('<li>' + o['username'] + '('+ o['role'] + ')</li>')
                       })
                   })
      $('#dialog-user')
                      .dialog({
                          resizable:false,
                          autoOpen: false,
                          modal: true,
                          buttons:{
                            "Add":function(){
                                var uid = $('#dialog-user #name').val();
                                var role = $('#dialog-user #role').val();
                                invokeWebApiEx('/group/'+id+'/addmember',
                                              prepareData({'members':[{'uid':uid,'role':role}]}),
                                              function(data) {
                                                  showGroupInfo(id);
                                              }
                                            )
                                $(this).dialog("close");
                            },
                            "Cancel":function(){
                                $(this).dialog("close");
                            }
                          }
                      })

      $("#add-member")
            .button()
            .click(function() {
                invokeWebApi('/account/list',
                      prepareData({}),
                      function (data){
                        data = data.results;
                        $('#dialog-user #name').html('');
                        var users = data['users'];
                        var userlist = [];
                        $.each(users, function(i, o) {
                            if(_appglobal.members.indexOf(o['username']) < 0)
                                $('#dialog-user #name').append('<option value="'+o['uid']+'">' + o['username']+ '</option>')
                        })                        
                        $("#dialog-user").dialog("open");
                      })
            });
}

function showTestSummary(id) {
    $('#session-div').tab();
    invokeWebApi('/group/'+id+'/testsummary',
                 prepareData({}),
                 function(data) {
                     renderTestSessionView(data);
                     _appglobal.t2 = setTimeout("showTestSummary(\""+id+"\")",60000);
                 }
                );
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



function deleteSessionById(gid,sid) {
    if(confirm('Confirm to delete this session?')) {
        invokeWebApi('/group/'+gid+'/test/'+sid+'/delete',
                    prepareData({}),
                    function(data){
                       showSessionInfo(_appglobal.gid,_appglobal.sid); 
                    });
    }
}

function renderTestSessionDiv(div_id, test_session){
    var $cycle_panel = $("#"+div_id).html('');
    var $product_table = $('<table>').attr('class','table table-bordered table-striped table-hover');
    var $th =     '<thead><tr>'+
                      '<th width="5%">id</th>'+
                      '<th width="10%">product</th>'+
                      '<th width="5%">build</th>'+
                      '<th width="10%">device</th>'+
                      '<th width="7%">planname</th>'+
                      '<th width="8%">tester</th>'+ 
                      '<th width="15%">statrtime</th>'+
                      '<th width="15%">runtime</th>'+
                      '<th width="5%">all</th>'+
                      '<th width="5%">pass</th>'+
                      '<th width="5%">fail</th>'+
                      '<th width="5%">error</th>'+
                      '<th width="5%"></th>'+
                      '</tr></thead>';
    var $tbody = '<tbody></tbody>';
    $product_table.append($th);
    $product_table.append($tbody);
    $cycle_panel.append($product_table);

    test_session.sort(function(a,b){return b._id - a._id});
    for(var k = 0; k < test_session.length;k++){
            var value = test_session[k];
            var key = value.id;
            var allId = "all_"+key;
            var failId = 'fail_'+key;
            var passId = 'pass_'+key;
            var errorId = 'error_'+key;
            if($("#"+allId).length <= 0){
                    $tr = "<tr>"+
                      "<td><a href=\"#/group/"+value.gid+"/session/"+value.sid+"\">"+key+"</a></td>"+
                      "<td>"+value.deviceinfo.product+"</td>"+      
                      "<td>"+value.deviceinfo.revision+"</td>"+
                      "<td>"+value.deviceid+"</td>"+
                      "<td>"+value.planname+"</td>"+                    
                      "<td>"+value.tester+"</td>"+
                      "<td>"+value.starttime+"</td>"+
                      "<td>"+setRunTime(value.runtime)+"</td>"+
                      "<td>"+value.summary.total+"</td>"+
                      "<td>"+value.summary.pass+"</td>"+
                      "<td>"+value.summary.fail+"</td>"+
                      "<td>"+value.summary.error+"</td>"+
                      "<td><a href=\"javascript:deleteSessionById('"+value.gid+"','"+value.sid+"')\">[X]</a></td>"+
                      "</tr>";
               $product_table.append($tr);
           }
    }

}

function renderTestSessionView(data) {
    var run_session_data = [];
    var stop_session_data = [];
    var sdata = data.results;
    if(sdata === undefined) 
        return;
    else
        sdata = sdata.sessions;
    if(sdata === undefined) return;

    for(var k = 0; k < sdata.length; k = k+1){
         var item = sdata[k];
         var endtime = item.endtime;
         if (endtime !== '' && endtime !== 'N/A')
             stop_session_data.push(item);
         else 
             run_session_data.push(item);
    }

    renderTestSessionDiv('run_cycle_panel', run_session_data);
    renderTestSessionDiv('stop_cycle_panel', stop_session_data);
}
function renderCaseSnaps(gid, sid, tid){
    var zoom = 1;
    var $snaplist = $('#img_list').html('');
    var wd = parseInt(_appglobal.deviceinfo['width']) >> zoom;
    var ht = parseInt(_appglobal.deviceinfo['height']) >> zoom;
    $('#history_div').dialog({title:"case snapshots",
                              height: ht + 120,
                              width: 2*wd + 80,
                              resizable:false,
                              modal: true});

    invokeWebApi('/group/'+gid+'/test/'+sid+'/case/'+tid+'/snaps',
                prepareData({}),
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
                        var imgdata = data.results.snaps[d]['data'];
                        if(imgdata === "")
                            $ig.src = 'static/img/notFound.png';
                        else
                            $ig.src = 'data:image/png;base64,' + imgdata;
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
                            if(title !== undefined && title.indexOf('(') > 0){
                                rect = title.substring(title.indexOf('(')+1, title.indexOf(')'));
                                title = title.substring(0, title.indexOf('('))+'.png';
                            }
                            var x = parseInt(rect.substring(rect.indexOf('x')+1, rect.indexOf('y'))) >> zoom;
                            var y = parseInt(rect.substring(rect.indexOf('y')+1, rect.indexOf('w'))) >> zoom;
                            var w = parseInt(rect.substring(rect.indexOf('w')+1, rect.indexOf('h'))) >> zoom;
                            var h = parseInt(rect.substring(rect.indexOf('h')+1)) >> zoom;
                            $igdiv.append($ig);
                            $icgdiv.append($icg);   
                            var $pdiv = $('<div>').attr('style','border:3px solid green; position:absolute; top:'+y+'px; left:'+x+'px; width:' +w+'px; height:'+h+'px');
                            $icgdiv.append($pdiv);
                            //$snapli.append($icgdiv); 
                            //$snapli.append($igdiv);
                            $icgdiv.attr('style','float:left');
                            $igdiv.attr('style','float:right');
                            $snapli.attr('class','item active');                                                 
                        } else {
                            $ig.setAttribute('class','thumbnail');
                            title = data.results.snaps[d]['title']
                            if(title.indexOf('(') > 0){
                                rect = title.substring(title.indexOf('(')+1, title.indexOf(')'));
                                title = title.substring(0, title.indexOf('('))+'.png';
                            }
                            var x = parseInt(rect.substring(rect.indexOf('x')+1, rect.indexOf('y'))) >> zoom;
                            var y = parseInt(rect.substring(rect.indexOf('y')+1, rect.indexOf('w'))) >> zoom;
                            var w = parseInt(rect.substring(rect.indexOf('w')+1, rect.indexOf('h'))) >> zoom;
                            var h = parseInt(rect.substring(rect.indexOf('h')+1)) >> zoom;
                            $igdiv.append($ig);
                            var $pdiv = $('<div>').attr('style','border:3px solid green; position:absolute; top:'+y+'px; left:'+x+'px; width:' +w+'px; height:'+h+'px');
                            $igdiv.append($pdiv).attr('style','float:left'); 
                            $icgdiv = undefined;
                            $snapli.attr('class','item');                                     
                        }
		           $snaptitle = $('<span>');
		           $snaptitle.html('<h3>('+idx+'/'+total+')'+ title +'</h3>'); 
                           //$snapli.append($snaptitle);
                           if($icgdiv !== undefined) $snapli.append($icgdiv); 
                           $snapli.append($igdiv);
                           $snaplist.append($snapli);
                           //$snapli.append($snaptitle);
			}
			    $('#history_div').carousel({"interval":100000});
		      }
		   );
}

function createDetailTable(ids){
    var $div_detail = $("#cases_div");
    var $tb = $('<table>').attr('id', ids).attr('class','table table-striped table-hover').attr('style','table-layout:fixed;word-wrap:break-word;');
    var $th = '<thead>'+
              '<tr>'+
	      '<th align="left" width="5%">tid</th>'+
              '<th align="left" width="24%">TestCase</th>'+
	      '<th align="left" width="15%">StartTime</th>'+
	      '<th align="left" width="6%">Result</th>'+
	      '<th align="left" width="40%">Traceinfo</th>'+
	      '<th align="left" width="5%">Log</th>'+
	      '<th align="left" width="5%">snaps</th>'+
	      '</tr>'+
	      '</thead>';
    var $tbody = '<tbody></tbody>';
    $tb.append($th);
    $tb.append($tbody);
    $div_detail.html($tb);
}

var ws = undefined;
function showSnapDiv(gid, sid) {
    $("#history_div").hide();
    $("#snap_div").show();
    renderSnapshotDiv(gid,sid);
}

function showHistoryDiv(gid, sid, tid) { 
    $("#history_div").show();
    $("#snap_div").hide();
    renderCaseSnaps(gid, sid, tid);
}

function renderSnapshotDiv(gid, sid) {
    var zoom = 1;
    if(ws !== undefined)  ws.close();
    ws = getWebsocket("/group/"+gid+"/test/"+sid+"/screen");
    if(ws === null) {
        alert('Your browser don\'t support Websocket connection!');
        return;
    }

    var wd = parseInt(_appglobal.deviceinfo['width']) >> zoom;
    var ht = parseInt(_appglobal.deviceinfo['height']) >> zoom;
    $('#snap_div').dialog({
			                     title:"Real-time Screen Snap",
		                       height: ht+120,
			                     width: wd+40,
		                       resizable:false,
		                       modal: true
                         });
    var c=document.getElementById("snapCanvas");
    var cxt=c.getContext("2d");

    ws.onopen = function() {
        ws.send('sync:ok');
    }

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
    }

    function doRenderImg(data) {
        var img = new Image();
        img.src = 'data:image/png;base64,' + data;
        cxt.drawImage(img,0,0,wd,ht);
    }
}

function sortTestCases(data) {
    var datacases = data;
    if(datacases !== undefined) {
        datacases.sort(function(a,b){ 
           return parseInt(b['tid']) - parseInt(a['tid']) ; 
        });
    }
    return datacases;
}

function fillDetailTable(data, ids, tag){
    var detail_table = $("#"+ids+" > tbody").html('');
    var tablerows = '';
    for (var i = 0; i < data.length; i++){
         var citem = data[i];
         var cgid = citem['gid'];
         var ctid = citem['tid'];
         var csid = citem['sid'];
         var ctime = citem['starttime'];
         var cname = citem['casename'];
         var cresult = citem['result'];
         var ctraceinfo = citem['traceinfo'];
         if(cresult == '') cresult = 'running';
         if(tag !== 'all' && tag !== cresult) continue;
         var trId = "tr_"+ctid;
         if(cresult === 'fail'){
                tablerows += "<tr id=\""+trId+"\">"+
                                        "<td>"+ctid+"</td>"+    
                                        "<td>"+cname+"</td>"+              
                                        "<td>"+ctime+"</td>"+
                                        "<td><font color=\"red\">"+cresult+"<font></td>"+
                                        "<td>"+
                                        "\""+ctraceinfo+"\""+
                                        "</td>"+
                                        "<td><a href=\""+apiBaseURL+"/group/"+cgid+"/test/"+csid+"/case/"+ctid+"/log\">log</a> </td>"+
                                        "<td><a href=\"javascript:showHistoryDiv('"+cgid+"','"+csid+"','"+ctid+"');\">snaps</a></td>"+
                                        "</tr>";

         } else if (cresult === 'error') {
                tablerows += "<tr id=\""+trId+"\">"+
                                     "<td>"+ctid+"</td>"+
                                     "<td>"+cname+"</td>"+
                                     "<td>"+ctime+"</td>"+
                                     "<td><font color=\"red\">"+cresult+"<font></td>"+
                                     "<td>"+
                                     "\""+ctraceinfo+"\""+
                                     "</td>"+
                                     "<td></td>"+
                                     "<td></td>"+
                                     "</tr>";

         } else if (cresult === 'running' || cresult === 'pass'){
                 if (cresult == 'running'){
                    tablerows += "<tr id=\""+trId+"\">"+
                                        "<td>"+ctid+"</td>"+
                                        "<td>"+cname+"</td>"+
                                        "<td>"+ctime+"</td>"+
                                        "<td><img src=\"static/img/running1.gif\" alt=\"running\"/></td>"+
                                        "<td></td>"+
                                        "<td></td>"+
                                        "<td></td>"+
                                        "</tr>";     
                 } else {    
                    tablerows += "<tr id=\""+trId+"\">"+
                                        "<td>"+ctid+"</td>"+
                                        "<td>"+cname+"</td>"+
                                        "<td>"+ctime+"</td>"+
                                        "<td>"+cresult+"</td>"+
                                        "<td></td>"+
                                        "<td></td>"+
                                        "<td></td>"+
                                        "</tr>";
                 }    
          } 
    }
    detail_table.append(tablerows);
    TablePage('#'+ids, 100, 20);
}

function showSessionInfo(gid,sid) {
      invokeWebApi('/group/'+gid+'/test/'+sid+'/results',
                   prepareData({}),
                   function(data){
                       _appglobal.deviceinfo = data.results.deviceinfo;
                       _appglobal.deviceinfo.deviceid = data.results.deviceid;
                       _appglobal.caseslist = sortTestCases(data.results.cases);
                       createDeviceInfo(_appglobal.deviceinfo);
                       //$('#session-name').show();
                       $('#session-name').parent().attr('href','#/group/'+gid+'/session/'+sid);
                       $('#session-name').html('test:'+data.results['id']);
                       if(data['results'] !== undefined && data['results']['endtime'] !== 'N/A') {
                           createHistoryCaseSummary(data);
                           createDetailTable('table_all_' + sid);
                           fillDetailTable(_appglobal.caseslist,'table_all_' + sid,'all');                
                       } else {
                           createLiveCaseSummary(data);
                           createDetailTable('table_all_' + sid);
                           fillDetailTable(_appglobal.caseslist,'table_all_' + sid,'all');
                           _appglobal.t1 = setTimeout("showSessionInfo(\""+gid+"\",\""+sid+"\")", 60000);
                       }
                  });
}

function createDeviceInfo(data) {
    var $dev_table = $('<table>').attr('class','table table-bordered');
    var $th = '<thead><tr><th>device</th><th>product</th><th>build</th><th>width</th><th>height</th></tr></thead>';
    var $tbody = '<tbody></tbody>';
    $('#device_div').html('').append($dev_table);
    $dev_table.append($th);
    $dev_table.append($tbody);

    $tr = "<tr>"+     
          "<td>"+data.deviceid+"</td>"+ 
          "<td>"+data.product+"</td>"+    
          "<td>"+data.revision+"</td>"+
          "<td>"+data.width+"</td>"+
          "<td>"+data.height+"</td>"+          
          "</tr>";
    $dev_table.append($tr);
}

function createLiveCaseSummary(data) {
    data = data.results;
    if(data === undefined) return;
    $('#summary_div').html('');
    var sid = data['sid'];
    var gid = data['gid'];
    var oId = "o_"+sid;
    var $summary_table = $('<table>').attr('class','table table-bordered').attr('id','stable-'+sid);
    var $th = '<thead><tr>'+
               '<th>planname</th>'+
               '<th>tester</th>'+
               '<th>starttime</th>'+
               '<th>runtime</th>'+
               '<th></th>'+
               '</tr></thead>';
    var $tbody = '<tbody></tbody>';
    $('#summary_div').append($summary_table);
    $summary_table.append($th);
    $summary_table.append($tbody);
    $tr = "<tr>"+     
          "<td>"+data['planname']+"</td>"+    
          "<td>"+data['tester']+"</td>"+
          "<td>"+data['starttime']+"</td>"+
          "<td>"+setRunTime(data['runtime'])+"</td>"+
          "<td><a id="+oId+" href=\"javascript:void(0)\">livesnaps</a></td>"+
          "</tr>";
    $summary_table.append($tr);
    $('#'+oId).click(function() {
        showSnapDiv(gid,sid);
    }) 
}

function createHistoryCaseSummary(data) {
    data = data['results'];
    var key = data['sid'];
    var alllink = "o_"+key;
    var faillink = 'fail_'+key;
    var passlink = 'pass_'+key;
    var errorlink = 'error_'+key;
    $('#summary_div').html('');
    var $summary_table = $('<table>').attr('class','table table-bordered').attr('id','stable'+key);
    var $th = '<thead><tr>'+
              '<th>planname</th>'+
              '<th>tester</th>'+
              '<th>statrtime</th>'+
              '<th>runtime</th>'+
              '<th>all</th>'+
              '<th>pass</th>'+
              '<th>fail</th>'+
              '<th>error</th>'+
              '</tr></thead>';
    var $tbody = '<tbody></tbody>';
    $('#summary_div').append($summary_table);
    $summary_table.append($th);
    $summary_table.append($tbody);
    $tr = "<tr>"+     
          "<td>"+data['planname']+"</td>"+    
          "<td>"+data['tester']+"</td>"+
          "<td>"+data['starttime']+"</td>"+
          "<td>"+setRunTime(data['runtime'])+"</td>"+
          "<td>"+"<a id="+alllink+" href=\"javascript:void(0)\" >"+data['summary']['total']+"</a></td>"+
          "<td>"+"<a id="+passlink+" href=\"javascript:void(0)\" >"+data['summary']['pass']+"</a></td>"+
          "<td>"+"<a id="+faillink+" href=\"javascript:void(0)\" >"+data['summary']['fail']+"</a></td>"+
          "<td>"+"<a id="+errorlink+" href=\"javascript:void(0)\" >"+data['summary']['error']+"</a></td>"+
          "</tr>";
    $summary_table.append($tr);

    $("#"+alllink).click(function(){                           
                           createDetailTable('table_all_' + key);
                           fillDetailTable(_appglobal.caseslist,'table_all_' + key,'all');
                      });       

    $("#"+faillink).click(function(){
                           createDetailTable('table_fail_' + key);
                           fillDetailTable(_appglobal.caseslist,'table_fail_' + key,'fail');
                      });

    $("#"+passlink).click(function(){
                           createDetailTable('table_pass_' + key);
                           fillDetailTable(_appglobal.caseslist, 'table_pass_' + key, 'pass');
                        });

    $("#"+errorlink).click(function(){
                           createDetailTable('table_error_' + key);
                           fillDetailTable(_appglobal.caseslist, 'table_error_' + key, 'error');
                        });
}

var AppRouter = Backbone.Router.extend({
    routes: {
        "group/:gid":"showGroupView",
        "group/:gid/session/:sid" : "showSessionView",
    },
    showGroupView: function(gid){
        checkLogIn();
        $('#group-div').show();
        $('#session-div').hide();
        $('#session-name').hide();
        _appglobal.gid = gid;
        if(_appglobal.t1 !== undefined) clearTimeout(_appglobal.t1);
        if(_appglobal.t2 !== undefined) clearTimeout(_appglobal.t2);
        showGroupInfo(gid);
        showTestSummary(gid);
    },
    showSessionView: function(gid,sid){
        checkLogIn();   
        $('#group-div').hide();
        $('#session-div').show();
        $('#session-name').show();
        _appglobal.gid = gid;
        _appglobal.sid = sid;
        if(_appglobal.t1 !== undefined) clearTimeout(_appglobal.t1);
        if(_appglobal.t2 !== undefined) clearTimeout(_appglobal.t2);
        showGroupInfo(gid);
        showSessionInfo(gid,sid);
    }
});
var index_router = new AppRouter;
Backbone.history.start();
