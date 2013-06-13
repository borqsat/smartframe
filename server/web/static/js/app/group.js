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
                         var bAdmin = false;
                         var userid = $.cookie('userid');
                         $.each(members, function(i, o) {
                              if(o['uid'] === userid)
                                  bAdmin = (o['role'] === 'owner') || (o['role'] === 'admin');                          
                         });
                         _appglobal.members = [];
                         $.each(members, function(i, o) {
                            _appglobal.members.push(o['username']);
                            var uid = o['uid'];
                            var role = o['role'];
                            $groupprf.append('<li>' + o['username'] + '('+ o['role'] + ')'
                                             + '<a href="javascript:deletemembersById(\''+id+'\',\''+uid+'\',\' '+role+'\')">' 
                                             + (bAdmin && o['role'] !== 'owner'? '[X]':'')+'</a></li>')
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

function deletemembersById(id, uid,role){
      if(confirm('Confirm to delete this members?')) {
        invokeWebApiEx('/group/'+id+'/delmember',
                    prepareData({'members':[{'uid':uid,'role':role}]}),
                    function(data) {
                       showGroupInfo(id);
                    });
    }
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

function viewLatest(){
    $('#tablatest').addClass('active');
    $('#tabhistory').removeClass('active');
    $('#live_cases_div').show();
    $('#cases_div').hide();
}

function viewHistory(){
    $('#tablatest').removeClass('active');
    $('#tabhistory').addClass('active');
    $('#live_cases_div').hide();
    $('#cases_div').show();    
}

function clearTab() {
    $('#cases_div').show();
}

function deleteSessionById(gid,sid) {
    if(confirm('Confirm to delete this session?')) {
        invokeWebApi('/group/'+gid+'/test/'+sid+'/delete',
                    prepareData({}),
                    function(data){
                       showTestSummary(gid);
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

    test_session.sort(function(a,b){return b.id - a.id});
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
    var $snaplist = $('#img_list').html('');
    var wd = _appglobal.screensize['width']
    var ht = _appglobal.screensize['height']
    var zoom = 1;

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
                        var imgurl = data.results.snaps[d]['url'];
                        if(imgurl === "")
                            $ig.src = 'static/img/notFound.png';
                        else
                            $ig.src = storeBaseURL + "/snap/" + imgurl;

                        $ig.setAttribute("id","snap"+idx);
                        $ig.setAttribute("width",wd+"px");
                        $ig.setAttribute("height",ht+"px");
                        if((idx === total) && (data.results.checksnap !== undefined)) {  
                            $icg.src = storeBaseURL + "/snap/" + data.results.checksnap['url'];
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

function createDetailTable(div, ids){
    var $div_detail = $("#"+div);
    var $tb = $('<table>').attr('id', ids).attr('class','table table-striped table-hover').attr('style','table-layout:fixed;word-wrap:break-word;');
    var $th = '<thead><tr>'+
              '<th align="left" width="5%">tid</th>'+
              '<th align="left" width="24%">TestCase</th>'+
              '<th align="left" width="15%">StartTime</th>'+
              '<th align="left" width="6%">Result</th>'+
              '<th align="left" width="40%">Traceinfo</th>'+
              '<th align="left" width="4%">Log</th>'+
              '<th align="left" width="6%">Image</th>'+
              '</tr></thead>';
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
    if(ws !== undefined && ws !== null) {
        ws.close(); 
    }
    ws = getWebsocket("/group/"+gid+"/test/"+sid+"/screen");
    if(ws === null) {
        alert('Your browser doesn\'t support Websocket connection!');
        return;
    }
    var wd = _appglobal.screensize['width'];
    var ht = _appglobal.screensize['height'];
    $('#snap_div').dialog({
                          title:"Real-time Snapshot",
                          height: ht+120,
                          width: wd+40,
                          resizable:false,
                          modal: true,
                          close: function () { if(ws !== undefined)  ws.close() }
                         });

    var c = document.getElementById("snapCanvas");
    var cxt = c.getContext("2d");
    ws.onopen = function() {
        ws.send('sync:ok');
    }

    ws.onmessage = function (evt) {
        var data = evt.data;
        if (data !== undefined) {
            doRenderImg(data);
            ws.send('sync:ok');
        }
    }

    function doRenderImg(data) {
        var img = new Image();
        img.src = data;
        img.onload = function() {
            cxt.drawImage(img, 0, 0, wd, ht);
        }
    }
}

function sortTestCases(data) {
    var datacases = data;
    if(datacases !== undefined) {
        datacases.sort(function(a,b){ 
           return parseInt(b['tid']) - parseInt(a['tid']) ; 
        });
        _appglobal.tid = datacases[0]['tid'];
    } else _appglobal.tid = 0;

    return datacases;
}

function fillDetailTable(gid, sid, data, ids, tag) {
    var detail_table = $("#"+ids+" > tbody").html('');
    var tablerows = '';
    var len = data.length;
    for (var i = 0; i < data.length; i++){
          var citem = data[i];
          var ctid = citem['tid'];
          var ctime = citem['starttime'];
          var cname = citem['casename'];
          var cresult = citem['result'];
          var ctraceinfo = citem['traceinfo'];
          var clog = citem['log']
          if(tag !== 'total' && tag !== cresult) continue;
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
                                        "<td><a href=\""+storeBaseURL+"/log/"+clog+"\">log</a></td>"+
                                        "<td><a href=\"javascript:showHistoryDiv('"+gid+"','"+sid+"','"+ctid+"');\">image</a></td>"+
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
                                        "<td>N/A</td>"+
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
}

function pollSessionStatus(gid, sid) {
    invokeWebApi('/group/' + gid + '/test/' + sid + '/poll',
                  prepareData({'tid':_appglobal.tid}),
                  function(data) {
                      var status = data.results;
                      if(status > 0) {
                          showLiveSessionCases(gid, sid);
                      }
                })
}

function showLiveSessionCases(gid,sid) {
      invokeWebApi('/group/'+gid+'/test/'+sid+'/live',
                    prepareData({'limit':20}),
                    function(data){
                        if(data.results === undefined) return;
                        var caseslist = sortTestCases(data.results.cases);
                        createSessionSummary(data, gid, sid);
                        createDetailTable('live_cases_div', 'table_latest_' + sid);
                        fillDetailTable(gid, sid, caseslist,'table_latest_' + sid, 'total');
                  });
}

function showHistorySessionCases(gid,sid) {
      invokeWebApi('/group/'+gid+'/test/'+sid+'/history',
                   prepareData({'type':'total'}),
                   function(data){
                        if(data.results === undefined) return;
                        var paging = data.results.paging;
                        var caseslist = data.results.cases;
                        createDetailTable('cases_div','table_total_' + sid);
                        fillDetailTable(gid, sid, caseslist,'table_total_' + sid, 'total');
                        if(paging !== undefined)  TablePage(gid, sid, paging['totalpage'], paging['pagesize'], fillDetailTable,'table_total_' + sid,'total');
                  },true);
}

function initScreenInfo(data) {
    var deviceinfo = data.results.deviceinfo;
    var wd = parseInt(deviceinfo['width']) >> 1;
    var ht = parseInt(deviceinfo['height']) >> 1;
    var c = document.getElementById("snapCanvas");
    c.setAttribute('width', wd + 'px');
    c.setAttribute('height', ht + 'px');
    _appglobal.screensize = {'width':wd, 'height':ht}
}

function showSessionInfo(gid,sid) {
      invokeWebApi('/group/'+gid+'/test/'+sid+'/summary',
                   prepareData({}),
                   function(data){
                        $('#session-name').parent().attr('href','#/group/' + gid + '/session/' + sid);
                        $('#session-name').html('session:' + data.results['id']);
                        initScreenInfo(data);
                        if(data['results']['endtime'] === undefined 
                          || data['results']['endtime'] === 'N/A') {
                            $('#tabs_session').show();
                            viewLatest();
                            createSessionBaseInfo(data, gid, sid);
                            createSessionSummary(data, gid, sid);
                            showLiveSessionCases(gid, sid);
                            $('#tabhistory').bind('click', function() {
                                viewHistory();
                            });
                            $('#tablatest').bind('click', function() {
                                viewLatest();
                            });
                            showHistorySessionCases(gid, sid);                                                    
                            _appglobal.t1 = setInterval("pollSessionStatus(\""+gid+"\",\""+sid+"\")", 20000);
                        }
                        else {
                            clearTab();
                            createSessionBaseInfo(data, '', '');
                            createSessionSummary(data, gid, sid);
                            showHistorySessionCases(gid, sid);
                        }
                  });
}

function createSessionBaseInfo(data, gid, sid) {
    data = data['results'];
    var $dev_table = $('<table>').attr('class','table table-bordered');
    var $th = '<thead><tr>'+
              '<th>planname</th>'+
              '<th>tester</th>'+           
              '<th>device</th>'+
              '<th>product</th>'+
              '<th>revision</th>'+              
              '<th>starttime</th>'+
              '</tr></thead>';   
    var $tbody = '<tbody></tbody>';
    $('#device_div').html('').append($dev_table);
    $dev_table.append($th);
    $dev_table.append($tbody);

    var strid = data.deviceid;
    if(gid !== '' && sid !== '') {
        strid = "<a href=javascript:showSnapDiv(\""+gid+"\",\""+sid+"\")>"+strid+"</a>";      
    }

    var $tr = "<tr>"+ 
          "<td>"+data['planname']+"</td>"+
          "<td>"+data.tester+"</td>"+
          "<td>"+strid+"</td>"+ 
          "<td>"+data.deviceinfo.product+"</td>"+
          "<td>"+data.deviceinfo.revision+"</td>"+
          "<td>"+data.starttime+"</td>"+
          "</tr>"

    $dev_table.append($tr);
}

function createSessionSummary(data, gid, sid) {
    data = data['results'];
    var key = data['sid'];
    var alllink = "o_"+key;
    var faillink = 'fail_'+key;
    var passlink = 'pass_'+key;
    var errorlink = 'error_'+key;
    $('#summary_div').html('');
    var $summary_table = $('<table>').attr('class','table table-bordered').attr('id','stable'+key);
    var $th = '<thead><tr>'+
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
          "<td>"+setRunTime(data.runtime)+"</td>"+
          "<td>"+"<a id="+alllink+" href=\"javascript:void(0)\" >"
          +data['summary']['total']+"</a></td>"+
          "<td>"+"<a id="+passlink+" href=\"javascript:void(0)\" >"
          +data['summary']['pass']+"</a></td>"+
          "<td>"+"<a id="+faillink+" href=\"javascript:void(0)\" >"
          +data['summary']['fail']+"</a></td>"+
          "<td>"+"<a id="+errorlink+" href=\"javascript:void(0)\" >"
          +data['summary']['error']+"</a></td>"+
          "</tr>";
    $summary_table.append($tr);

    $("#"+alllink).click(function(){
                           viewHistory();
                           invokeWebApi('/group/'+gid+'/test/'+sid+'/history',
                                        prepareData({'type':'total'}),
                                        function(data){
                                            if(data.results === undefined) return;
                                            var paging = data.results.paging;
                                            var caseslist = data.results.cases;
                                            createDetailTable('cases_div','table_total_' + sid);
                                            fillDetailTable(gid, sid, caseslist,'table_total_' + sid, 'total');
                                            if(paging !== undefined) TablePage(gid, sid, paging['totalpage'], paging['pagesize'], fillDetailTable,'table_total_' + sid,'total');
                                        });
                      });       

    $("#"+faillink).click(function(){
                           viewHistory();
                           invokeWebApi('/group/'+gid+'/test/'+sid+'/history',
                                        prepareData({'type':'fail'}),
                                        function(data){
                                            if(data.results === undefined) return;
                                            var paging = data.results.paging;
                                            var caseslist = data.results.cases;
                                            createDetailTable('cases_div','table_fail_' + sid);
                                            fillDetailTable(gid, sid, caseslist,'table_fail_' + sid,'fail');
                                            if(paging !== undefined) TablePage(gid, sid, paging['totalpage'], paging['pagesize'], fillDetailTable, 'table_fail_' + sid,'fail');
                                        });
                          });

    $("#"+passlink).click(function(){
                           viewHistory();
                           invokeWebApi('/group/'+gid+'/test/'+sid+'/history',
                                        prepareData({'type':'pass'}),
                                        function(data){
                                            if(data.results === undefined) return;
                                            var paging = data.results.paging;
                                            var caseslist = data.results.cases;
                                            createDetailTable('cases_div','table_pass_' + sid);
                                            fillDetailTable(gid, sid, caseslist,'table_pass_' + sid,'pass');
                                            if(paging !== undefined) TablePage(gid, sid, paging['totalpage'], paging['pagesize'], fillDetailTable, 'table_pass_' + sid,'pass');
                                        });
                          });

    $("#"+errorlink).click(function(){
                           viewHistory();
                           invokeWebApi('/group/'+gid+'/test/'+sid+'/history',
                                        prepareData({'type':'error'}),
                                        function(data){
                                            if(data.results === undefined) return;
                                            var paging = data.results.paging;
                                            var caseslist = data.results.cases;
                                            createDetailTable('cases_div','table_error_' + sid);
                                            fillDetailTable(gid, sid, caseslist,'table_error_' + sid,'error');
                                            if(paging !== undefined) TablePage(gid, sid, paging['totalpage'], paging['pagesize'], fillDetailTable, 'table_error_' + sid, 'error');
                                        });
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
        if(_appglobal.t1 !== undefined) clearInterval(_appglobal.t1);
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
        if(_appglobal.t1 !== undefined) clearInterval(_appglobal.t1);
        if(_appglobal.t2 !== undefined) clearTimeout(_appglobal.t2);
        showGroupInfo(gid);
        showSessionInfo(gid,sid);
    }
});
var index_router = new AppRouter;
Backbone.history.start();
