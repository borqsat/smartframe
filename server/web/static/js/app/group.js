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
                                  bAdmin = (o['rolename'] === 'owner') || (o['rolename'] === 'admin');                          
                         });
                         _appglobal.members = [];
                         $.each(members, function(i, o) {
                            _appglobal.members.push(o['username']);
                            var uid = o['uid'];
                            var role = o['rolename'];
                            $groupprf.append('<li>' + o['username'] + '('+ o['rolename'] + ')'
                                             + '<a href="javascript:deletemembersById(\''+id+'\',\''+uid+'\',\' '+role+'\')">' 
                                             + (bAdmin && o['rolename'] !== 'owner'? '[X]':'')+'</a></li>')
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

function deleteCycleById(gid, sid) {
  if(confirm('Confirm to delete this cycle?')){
      invokeWebApiEx('/group/'+gid+'/test/'+sid+"/update",
                prepareData({'cid':-1}),
                function(data) {
                  showTestSummary(gid);
                });
  }
}

function updateCycleById(gid, sid, cid) {
      invokeWebApiEx('/group/'+gid+'/test/'+sid+"/update",
                prepareData({'cid':parseInt(cid)}),
                function(data) {
                  showTestSummary(gid);
                });
}


function showCycleListDiv(gid, sid, cyclelist1) {
    var $cyclelist_table = $('<table>').attr('class','table table-bordered table-striped table-hover').attr('style','display:none');
    
    var cyclelist = new Array();
    cyclelist =  cyclelist1.split(',');
    $tr = "<tr>"+
              "<td>Cycle Id</td><td>opearation</a></td>"+
          "</tr>" ;
    $cyclelist_table.append($tr);
    for (var i = 2; i < cyclelist.length; i++) {
        var cid = cyclelist[i];
        $tr = "<tr>"+
                  "<td><a href=\"javascript:updateCycleById('"+gid+"','"+sid+"','"+cid+"')\" >"+cid+"</a></td><td><a href=\"javascript:deleteCycleById('"+gid+"','"+sid+"')\" >delete</a></td>"+ 
              "</tr>";
        $cyclelist_table.append($tr);
    };
    $("#"+sid).append($cyclelist_table);
    $cyclelist_table.dialog({title:"Choose cycles",
                              height: 900,
                              width: 250,
                              resizable:false,
                              buttons:{
                                "new cycle":function() { 
                                    invokeWebApiEx('/group/'+gid+'/test/'+sid+"/update",
                                    prepareData({'cid':0}),
                                    function(data) {
                                         showTestSummary(gid);
                                      }
                                    );
                                    $(this).dialog("close");
                              },
                                "use cycle":function(){}
                              },
                              close: function () { $(this).dialog("close"); },
                              modal: true
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

    $("#add-cycle")
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

function viewAllCycleList(){
    $('#tabcyclelist').addClass('active');
    $('#tabdeviceslist').removeClass('active');
    $('#cyclelist_panel').show();
    $('#devicelist_panel').hide();    
}

function viewAllDeviceList(){
    $('#tabcyclelist').removeClass('active');
    $('#tabdeviceslist').addClass('active');
    $('#cyclelist_panel').hide();
    $('#devicelist_panel').show();   
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
    $('#tabs_session').hide();
    $('#live_cases_div').hide();
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

function editCIdFunction(gid, sid, cid_sel){
    var cid_index = 0;
    var flag = false;
    if (cid_sel === "deleteCycleId"){
        cid_index = -1 ;
        flag = true;
    }else if(cid_sel === "newCycleId"){
        cid_index = 0 ;
        flag = true;
    }else{
        cid_index = cid_sel ;
        flag = true;
    }
    if (flag === true){
        invokeWebApiEx('/group/'+gid+'/test/'+sid+"/update",
                prepareData({'cid':parseInt(cid_index)}),
                    function(data) {
                        showTestSummary(gid);
                });
    };
    //return false;
}


function getCycleList(key, gid, sid, cid){
     var cyclelist_options = "";
     var cycles = _appglobal.cyclelist[key]||[];
     
     if ( cid !== "" ){
        cyclelist_options = "<li><a>"+cid+"</a><b></b>";
     }else {
        cyclelist_options = "<li><a>Edit</a><b></b>";
     }
     
     cyclelist_options = cyclelist_options + "<div class=\"panel dropanel1\">" ;
     for (var i = 0; i < cycles.length; i++) {
         if (cycles[i] !== cid){
             cyclelist_options = cyclelist_options + "<a href=\"javascript:editCIdFunction('"+gid+"','"+sid+"','"+cycles[i]+"')\">"+cycles[i] +"</a><br>";
         }
     };
     cyclelist_options = cyclelist_options + "<a href=\"javascript:editCIdFunction('"+gid+"','"+sid+"','newCycleId')\">New</a><br>" ;
     if ( cid !== "" ){
         cyclelist_options = cyclelist_options + "<a href=\"javascript:editCIdFunction('"+gid+"','"+sid+"','deletecycle')\">Delete</a>"
     }

     cyclelist_options = cyclelist_options + "</div></li>" ;
     return cyclelist_options;
}

function renderTestSessionDiv_devicelist(div_id, test_session){
    var $cycle_panel = $("#"+div_id).html('');
    var $product_table = $('<table>').attr('class','table table-bordered table-hover');
    var $th =     '<thead><tr>'+
                      '<th width="1%"></th>'+
                      '<th width="5%">Cycle</th>'+
                      '<th width="15%">Device#</th>'+
                      '<th width="10%">Build Version</th>'+
                      '<th width="15%">Start Time</th>'+
                      '<th width="15%">Uptime</th>'+
                      '<th width="5%">Product</th>'+
                      '<th width="5%">Tester</th>'+ 
                      '<th width="2%">Detail</th>'+
                      '<th width="3%"></th>'+
                      '</tr></thead>';
    var $tbody = '<tbody></tbody>';
    $product_table.append($th);
    $product_table.append($tbody);
    $cycle_panel.append($product_table);
    
    // _appglobal.cyclelist = [];//new Array();
    // for(var s = 0; s < test_session.length;s++){
    //     var cid = test_session[s].cid;
    //     if (cid !== "" && cid !== "N/A"){
    //         _appglobal.cyclelist.push(cid);
    //     }
    // }
    
    _appglobal.cyclelist = {};//new Array();

    for(var s = 0; s < test_session.length;s++){
        var cid = test_session[s].cid;
        if (cid !== "" && cid !== "N/A"){
            //_appglobal.cyclelist.push(cid);
            var product = test_session[s].product ;
            var revision = test_session[s].revision ;
            var key = product + ":" + revision;
            if (_appglobal.cyclelist[key] === undefined) {
                _appglobal.cyclelist[key] = [];
            }
            _appglobal.cyclelist[key].push(cid);
        }
    }  

    var sessions = [];
    for(var k = 0; k < test_session.length;k++){
        var cid = test_session[k].cid;
        var count = test_session[k].count;
        var starttime = test_session[k].starttime;
        var product = test_session[k].product;
        var revision = test_session[k].revision;
        for (var i = 0 ; i < test_session[k].sessions.length; i++) {
            var session_item = test_session[k].sessions[i];
            session_item['cid'] = cid;    
            session_item['product'] = product;
            session_item['revision'] = revision;
            sessions.push(session_item);
        }
    }

    sessions.sort(function(a,b) { return ( (a.status < b.status) || ((a.status == b.status) && (b.cid > a.cid))|| ((a.status == b.status) && (b.cid == a.cid) && (a.id < b.id)))?1:-1 ;})

    for(var t = 0; t < sessions.length; t++) {
            var value = sessions[t];
            var key = value.id ;
            var sid = value.sid;
            var endtime = value.endtime;
            var key = value.product + ":" + value.revision;
            var css = value.status == 'running' ? "style='background-color:#4682B4'":"style='background-color:#8C8C8C'";
            $tr = "<tr class='info'>"+
                      "<td "+css+"></td>"+
                      "<td><div id ='showCidSelect'"+value.sid+" class=\"sitenav\"><ul class='cycleposition'>"+getCycleList(key,value.gid,value.sid,value.cid)+
                      "</ul></div></td>"+
                      "<td>"+value.deviceid+"</td>"+     
                      "<td>"+value.revision+"</td>"+              
                      "<td>"+value.starttime+"</td>"+
                      "<td>"+setRunTime(value.runtime)+"</td>"+
                      "<td>"+value.product+"</td>"+
                      "<td>"+value.tester+"</td>"+
                      "<td><a href=\"#/group/"+value.gid+"/session/"+value.sid+"\">detail</a></td>"+ 
                      "<td><a href=\"javascript:deleteSessionById('"+value.gid+"','"+value.sid+"');\">[X]</a></td>"+
                      "</tr>";
            $product_table.append($tr);
    };
}

function linkToSessionDetailList(gid, sid, cid){
    window.location = "#/group/"+gid+"/session/"+sid;
}

function renderTestSessionDiv_cyclelist(div_id, test_session){
    var $cycle_panel = $("#"+div_id).html('');
    var $product_table = $('<table>').attr('class','table table-bordered table-striped table-hover');
    var $th =     '<thead><tr>'+
                      '<th width="2%">Cycle</th>'+
                      '<th width="5%">Product</th>'+
                      '<th width="20%">Build Version</th>'+
                      //'<th width="10%">Start Time</th>'+
                      //'<th width="10%">End Time</th>'+
                      '<th width="5%">Devices</th>'+
                      '<th width="7%">Living Devices</th>'+
                      '<th width="1%">Report</th>'+ 
                      '</tr></thead>';
    var $tbody = '<tbody></tbody>';
    $product_table.append($th);
    $product_table.append($tbody);
    $cycle_panel.append($product_table);
    
    test_session.sort(function(a,b) { return (b.cid > a.cid)?1:-1 ;});
    for(var k = 0; k < test_session.length;k++){
        var cid = test_session[k].cid;
        var count = test_session[k].count;
        var livecount = test_session[k].livecount;
        var starttime = test_session[k].starttime;
        var endtime = test_session[k].endtime;
        var product = test_session[k].product;
        var revision = test_session[k].revision;
        if (cid !== "" && cid !== "N/A") {
            $tr = "<tr>"+
                "<td>"+cid+"</td>"+ 
                "<td>"+product+"</td>"+      
                "<td>"+revision+"</td>"+
                //"<td>"+starttime+"</td>"+
                //"<td>"+endtime+"</td>"+
                "<td>"+count+"</td>"+                   
                "<td>"+livecount+"</td>"+
                "<td><a href=\"#/group/"+test_session[k].sessions[0].gid+"/report/"+cid+"\">Report</a></td>"+
                "</tr>";
            $product_table.append($tr);
        }
    };
}


function renderTestSessionView(data) {
    var run_session_data = [];
    var stop_session_data = [];
    var sdata = data.results;
    if(sdata === undefined) 
        return;
    
    renderTestSessionDiv_cyclelist('cyclelist_panel', data.results);
    renderTestSessionDiv_devicelist('devicelist_panel', data.results);
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
                        var $ig = document.createElement('img');
                        var $icg = document.createElement('img');
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
              '<th align="left" width="3%"></th>'+
              '<th align="left" width="6%">Tid</th>'+
              '<th align="left" width="31%">Testcase</th>'+
              '<th align="left" width="17%">Start Time</th>'+
              '<th align="left" width="7%">Result</th>'+
              '<th align="left" width="5%">Log</th>'+
              '<th align="left" width="7%">Image</th>'+
              '<th align="left" width="24%"><a href="javascript:showComment()">Comments</th>'+
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
        var img = document.createElement('img');
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

function collectID(ctid){
  var key = _appglobal.collectIDs['tids'].indexOf(ctid);
  if (key === -1){
    _appglobal.collectIDs['tids'].push(ctid);
  }
  else{
    _appglobal.collectIDs['tids'].splice(key, key);
  }
}

function fillDetailTable(gid, sid, data, ids, tag) {
    var tablerows = '';
    var detail_table = $("#"+ids+" > tbody").html('');
    var len = data.length;
    _appglobal.collectIDs = {'tids':[]};
    _appglobal.collectIDs['gid'] = gid;
    _appglobal.collectIDs['sid'] = sid;
    for (var i = 0; i < data.length; i++){
          var citem = data[i];
          var ctid = citem['tid'];
          var ctime = citem['starttime'];
          var cname = citem['casename'];
          var cresult = citem['result'];
          var clog = citem['log'];
          var comResult = citem['comments'];
          if(tag !== 'total' && tag !== cresult) continue;
          var trId = "tr_"+ctid;
          
          if(comResult !== undefined){
             if(comResult['endsession'] === 0)
                 {var sessionCom = "";}
             else
                 {var sessionCom = " :: Yes";}

             if(comResult['commentinfo'] !== undefined && comResult['issuetype'] !== undefined && comResult['caseresult'] !== undefined){
                 var hintInfo = comResult['commentinfo'];
                 var showComment = ""+comResult['caseresult']+" :: "+comResult['issuetype']+""+sessionCom+"";
             }
             else{             
                 var showComment = "";
                 var hintInfo = "";}
          }
          else{
             var showComment = "";
             var hintInfo = "";
          }
          if(cresult === 'fail'){
              tablerows += "<tr id=\""+trId+"\">"+
                                        "<td><input id=\"checkbox_"+ctid+"\" type=\"checkbox\" onclick=\"collectID('"+ctid+"')\"></input></td>"+
                                        "<td>"+ctid+"</td>"+    
                                        "<td>"+cname+"</td>"+              
                                        "<td>"+ctime+"</td>"+
                                        "<td><font color=\"red\">"+cresult+"<font></td>"+
                                        "<td><a href=\""+storeBaseURL+"/log/"+clog+"\">log</a></td>"+
                                        "<td><a href=\"javascript:showHistoryDiv('"+gid+"','"+sid+"','"+ctid+"');\">image</a></td>"+
                                        "<td>"+                                      
                                        "<span id=\"span_"+ctid+"\" onmouseover=\"showHint('"+ctid+"')\" onmouseout=\"hideHint('"+ctid+"')\">"+showComment+"</span>"+
                                        "<br><div id=\"hint_"+ctid+"\" style=\"display:none\">"+hintInfo+"</div>"+
                                        "</td></tr>";                                                 
         } else if (cresult === 'error') {
                tablerows += "<tr id=\""+trId+"\">"+
                                     "<td><input type=\"checkbox\" onselect=\"collectID('"+ctid+"')\"></input></td>"+
                                     "<td>"+ctid+"</td>"+
                                     "<td>"+cname+"</td>"+
                                     "<td>"+ctime+"</td>"+
                                     "<td><font color=\"red\">"+cresult+"<font></td>"+
                                     "<td></td>"+
                                     "<td></td>"+
                                     "<td>"+
                                     "<span id=\"span_"+ctid+"\" onmouseover=\"showHint('"+ctid+"')\" onmouseout=\"hideHint('"+ctid+"')\">"+showComment+"</span>"+
                                     "<br><div id=\"hint_"+ctid+"\" style=\"display:none\">"+hintInfo+"</div>"+
                                     "</td></tr>";
         } else if (cresult === 'running' || cresult === 'pass'){
                 if (cresult == 'running'){
                    tablerows += "<tr id=\""+trId+"\">"+
                                        "<td></td>"+
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
                                        "<td></td>"+
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
    tablerows += fillCommentDiv(gid, sid);
    detail_table.append(tablerows);
}

function showHint(ctid){$("#hint_"+ctid).slideDown('slow');}

function hideHint(ctid){$("#hint_"+ctid).hide('slow');}

function fillCommentDiv(gid, sid){
    var commentDiv = "<tr id=\"comDiv\" style=\"display:none\"><td colspan=\"7\"><form class=\"form-inner\">"+
                       "<div class=\"row\">"+
                         "<div class=\"span4\">"+
                            "<textarea name=\"commentinfo\" id=\"commentInfo\" class=\"input-xlarge span4\" rows=\"9\" placeholder=\"Please comments here...\"></textarea>"+
                         "</div>"+
                         "<div class=\"span3\">"+
                            "<label>Issue Type</label>"+
                            "<select class=\"span3\">"+
                               "<option value=\"na\" name=\"issuetype\" selected=\"\">Choose One:</option>"+
                               "<option id=\"PhoneHang\" name=\"issuetype\" value=\"PhoneHang\">PhoneHang</option>"+
                               "<option id=\"ForceClose\" name=\"issuetype\" value=\"ForceClose\">ForceClose</option>"+
                               "<option id=\"ANR\" name=\"issuetype\" value=\"ANR\" >ANR</option>"+
                               "<option id=\"SystemCrash\" name=\"issuetype\" value=\"SystemCrash\">SystemCrash</option>"+
                               "<option id=\"UiFreeze\" name=\"issuetype\" value=\"UIFreeze\">UIFreeze</option>"+
                               "<option id=\"Others\" name=\"issuetype\" value=\"Others\">Others</option>"+
                            "</select>"+
                        "<label>Case Result</label>"+
                        "<select class=\"span3\">"+
                          "<option value=\"na\" name=\"caseresult\" selected=\"\">Choose One:</option>"+
                          "<option id=\"Fail\" name=\"caseresult\" value=\"Fail\">Fail</option>"+
                          "<option id=\"Block\" name=\"caseresult\" value=\"Block\">Block</option>"+
                        "</select>"+
                        "<label class=\"checkbox\" for=\"endsession\">"+
                        "<span>Session ends here?</span><input id=\"endsession\" type=\"checkbox\">"+
                        "</label><br>"+
                        "<input id=\"btnc\" onclick=\"submitUpdate('"+gid+"', '"+sid+"', 'clear')\" type=\"button\" class=\"pull-right\" value=\"Clear\"></input>"+
                        "<input id=\"btn\" onclick=\"submitUpdate('"+gid+"', '"+sid+"', 'submit')\" type=\"button\" class=\"pull-right\" value=\"Commit\"></input>"+
                      "</div>"+
                   "</div></form></td></tr>";
    return commentDiv;
}

function submitUpdate(gid, sid, tag){
    if (_appglobal.collectIDs['tids'].length === 0){
      alert("No case selected!!");
      return
    }
    var comResult = {};
    if (tag === 'submit'){
      $("option[name='issuetype']").each(function(i,obj){if(obj.selected){comResult['issuetype']=obj.value;}});
      $("option[name='caseresult']").each(function(i,obj){if(obj.selected){comResult['caseresult']=obj.value;}});
      $("input#endsession").each(function(i,obj){if(obj.checked){comResult['endsession'] = 1;}
                                                 else{comResult['endsession'] = 0;}});
      comResult['commentinfo'] = $("textarea[name='commentinfo']").val();
      comResult['tids'] = _appglobal.collectIDs['tids'];

      if (comResult['issuetype'] === 'na' || comResult['caseresult'] === 'na' || comResult['commentinfo'] === ''){
        alert("IssueType, CaseResult and Comments are all expected to be provided!");
        return
      }
      if (comResult['tids'].length > 1 && comResult['endsession'] === 1){
        alert("Session end can only be assigned to ONE case!");
        return
      }

      if (comResult['endsession'] === 0){var sessionCom = "";}
      else{var sessionCom = " :: Yes";}
      var $hintInfo = comResult['commentinfo'];
      var $showComment = ""+comResult['caseresult']+" :: "+comResult['issuetype']+""+sessionCom+"";
      for (var i = 0; i < _appglobal.collectIDs['tids'].length; i++){
          $("span#span_"+_appglobal.collectIDs['tids'][i]).html("");
          $("span#span_"+_appglobal.collectIDs['tids'][i]).append($showComment);
          $("div#hint_"+_appglobal.collectIDs['tids'][i]).html("");
          $("div#hint_"+_appglobal.collectIDs['tids'][i]).append($hintInfo);
          $("#checkbox_"+_appglobal.collectIDs['tids'][i]+"").attr('checked', false);
      }

      invokeWebApiEx("/group/"+gid+"/test/"+sid+"/case/00000/update",
                     prepareData({'comments':comResult}),
                     afterCommit);
    }
    else if (tag === 'clear'){
      for (var i = 0; i < _appglobal.collectIDs['tids'].length; i++){
          var $hintInfo = "";
          var $showComment = "";
          $("span#span_"+_appglobal.collectIDs['tids'][i]).html("");
          $("span#span_"+_appglobal.collectIDs['tids'][i]).append($showComment);
          $("div#hint_"+_appglobal.collectIDs['tids'][i]).html("");
          $("div#hint_"+_appglobal.collectIDs['tids'][i]).append($hintInfo);
          $("#checkbox_"+_appglobal.collectIDs['tids'][i]+"").attr('checked',false);
      }

      comResult['endsession'] = 0;
      comResult['tids'] = _appglobal.collectIDs['tids'];
      
      invokeWebApiEx("/group/"+gid+"/test/"+sid+"/case/00000/update",
                 prepareData({'comments': comResult}),
                 afterCommit);
    }
    _appglobal.collectIDs = {'tids':[]};
    $("#comDiv").dialog('close');
}

function showComment(){
    $("tr#comDiv").dialog({title: "Comments for Cases:",
                                  height: 310,
                                  width: 595,
                                  resizable:false,
                                  modal: true,
                                  draggable: false});
}

function afterCommit(data){
  var ret = data['error'];
  if (ret !== undefined){
    alert(ret['msg']);
  }
  else{
    alert("Commit successfully!");
  }
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
              '<th>Planname</th>'+
              '<th>Tester</th>'+
              '<th>Device#</th>'+
              '<th>Product</th>'+
              '<th>Build Version</th>'+
              '<th>Start Time</th>'+
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
              '<th>Uptime</th>'+
              '<th>All</th>'+
              '<th>Pass</th>'+
              '<th>Fail</th>'+              
              '<th>Error</th>'+
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


function showReportInfo(gid,cid){
    invokeWebApi('/group/'+gid+'/testsummary',
                prepareData({'cid':cid}),
                function(data) {
                  showCommentInfo();
                  showCycleBaseInfo(data);
                  showFailureSummaryInfo(data);
                  showFailureDetailsInfo(data,gid);
                  showDomainInfo(data);
                },true);
}

function toggle(){
        var articleID=document.getElementById("article");
            if (articleID.style.display=="none"){
                articleID.style.display="block";
            } else {
                articleID.style.display="none";
            }
}
 



function showCommentInfo(){

    $('#show-title').html('<a style="text-align:center" href=\"javascript:void(0)\">Tap here to get more information</a><br />');
    $('#article').html( "<b>MTBF</b> = Total Uptime/Total Failures  <br />" +
    					"<b>Product:</b> The device platform and product information. <br />" + 
    					"<b>Start Time:</b> The test start time. <br />" + 
    					"<b>End Time: </b>The test finish timestamp. Genericlly the value should be the ciritical issue happen time or the test stop time. 'N/A' means the test is ongoing. <br />" + 
    					"<b>Uptime:</b> Uptime = Endtime - StarTime . EndTime is the critical issue happen time or test stop time. <br />" + 
                        "<b>Failures</b>= (critical issues) + (Non-Critical issues). <br />"+
                        "<b>Critial Issues:</b> Phone hang, kernel reboot/panic, system crash, etc. <br />"+
                        "<b>Non-Critical Issues:</b> Application/process force close/ANR, core dump (native process crash), etc.<br />"+
                        "<b>First Failure Uptime:</b> From the <b>Start Time</b> to first failure occurs. <br />");

}

function showCycleBaseInfo(data){
    var data = data.results.cylesummany
    var $dev_table = $('<table>').attr('class','table table-bordered');
    var $th = '<thead><tr>'+
              '<th width="8%">Product</th>'+
              '<th width="18%">Build Version</th>'+           
              '<th width="12%">Devices</th>'+            
              '<th width="12%">Total Failures</th>'+
              '<th width="12%">Total Uptime</th>'+
              '<th width="12%">MTBF</th>'+
              '</tr></thead>';
    var $tbody = '<tbody></tbody>';
    $('#product-div').html('').append($dev_table);
    $dev_table.append($th);
    $dev_table.append($tbody);

    if (data.failcnt == 0)
      avgTime = data.totaldur;
    else
      avgTime = Math.round((data.totaldur/data.failcnt)*100)/100;

    var $tr = "<tr>"+ 
          "<td>"+data.product+"</td>"+
          "<td>"+data.buildid+"</td>"+
          "<td>"+data.count+"</td>"+ 
          "<td>"+data.failcnt+"</td>"+
          "<td>"+setRunTime(data.totaldur)+"</td>"+
          "<td>"+setRunTime(avgTime)+"</td>"+
          "</tr>"

    $dev_table.append($tr);

}

function showFailureSummaryInfo(data) {

    var data = data.results.issuesummany;

    var $dev_table = $('<table>').attr('class','table table-bordered');
    var $title = '<thead><tr><th colspan="2" style="text-align:center;font-size:16px;">Failure Summary</th></tr></thead>'
    var $th = '<thead><tr>'+
              '<th style="text-align:center" width="50%">Issue Type </th>'+
              '<th style="text-align:center" width="50%">Occurs</th>'+
              '</tr></thead>';
    $dev_table.append($title);
    $dev_table.append($th);
    if (data.length==0){
          var $th1 = '<thead><tr>'+
                  '<td style="text-align:center">'+'No issue'+'</td>'+
                  '<td style="text-align:center">'+0+"</td>"+
                  '</tr></thead>';
          $dev_table.append($th1);
    }    
    else{
        for (var i = 0; i < data.length; i++){
            var $th1 = '<thead><tr>'+
                  '<td style="text-align:center">'+data[i].issuetype+'</td>'+
                  '<td style="text-align:center">'+data[i].count+"</td>"+
                  '</tr></thead>';
            $dev_table.append($th1);
        }
    }
    var $tbody = '<tbody></tbody>';
    $('#failure-detail-div').html('').append($dev_table);
    $dev_table.append($tbody);
  }

function showPic(picID){
    var imgSrc=["static/img/spread.png","static/img/combine.png"];
    var img = document.getElementById(picID);
    img.src = img.src.match(imgSrc[0])?imgSrc[1]:imgSrc[0];
}

function showFailuresInfo(gid,sid){
    viewHistory();
      invokeWebApi('/group/'+gid+'/test/'+sid+'/summary',
                   prepareData({}),
                   function(data){
                        initScreenInfo(data);
                  });
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
}

function showFailureDetailsInfo(data,gid){
    var data = data.results.issuedetail;

    var $dev_table = $('<table border="1">').attr('class','table table-bordered');
    var $th = '<thead><tr>'+
              '<th></th>'+
              '<th>Device#</th>'+
              '<th>Start Time</th>'+           
              '<th>End Time</th>'+            
              '<th>Failures</th>'+
              '<th>First Failure Uptime</th>'+
              '<th>Uptime</th>'+
              '</tr></thead>';
    var $tbody = '<tbody></tbody>';
    $('#device-failure-detail-div').html('').append($dev_table);
    $dev_table.append($th);
    $dev_table.append($tbody);

    for (var i = 0; i < data.length; i ++){
        var failureCount = data[i].failcount;
        var sid = data[i].sid;
        var deviceSerial = data[i].imei;
        if (deviceSerial ==="") deviceSerial = "N/A";
        var $tr = "<tr>"+
                    (failureCount==0?"<td></td>":"<td onclick=showPic('pic_"+i.toString()+"'); id='tr_"+i.toString()+"'><img id='pic_"+i.toString()+"' src='static/img/spread.png'></img></td>")+        
                    "<td><a href=\"#/group/"+gid+"/session/"+sid+"\">"+deviceSerial+"</a></td>"+
                    "<td>"+data[i].starttime+"</td>"+
                    "<td>"+data[i].endtime+"</td>"+ 
                    (failureCount==0?"<td style='text-align:center'>"+0+"</td>":"<td style='text-align:center'><a href=\"#/group/"+gid+"/session/"+sid+"/fail\">"+failureCount+"</a></td>")+
                    "<td>"+setRunTime(data[i].faildur)+"</td>"+
                    "<td>"+setRunTime(data[i].totaldur)+"</td>"+
                    "</tr>";
        var $th_sub = '<tr  id="subtr_'+i.toString()+'" class="hidden">'+
              '<td></td>'+
              '<th style="background:#ECECFF"></th>'+      
              '<th style="background:#ECECFF;">Happened Time</th>'+
              '<th style="background:#ECECFF">Issue Type</th>'+
              '<th style="background:#ECECFF;text-align:center" colspan="3">Comments</th>'+
              '</tr>';

        $dev_table.append($tr);
        if (data[i].caselist.length != 0){
            $dev_table.append($th_sub);
        }
        
        $('#tr_'+i.toString()).toggle(function(){
              $('tr#sub'+this.id).removeClass('hidden');              
            },function(){
              $('tr#sub'+this.id).addClass('hidden');
          });
        
        for (var j = 0; j < data[i].caselist.length; j ++){
            var $th_sub1 = "<tr  id='subtr_"+i.toString()+"' class='hidden'>"+ 
                    '<td></td>'+ 
                    "<td style='background:#ECECFF;text-align:center'>"+(j+1)+"</td>"+            
                    "<td style='background:#ECECFF'>"+data[i].caselist[j].happentime+"</td>"+
                    "<td style='background:#ECECFF'>"+data[i].caselist[j].issuetype+"</td>"+
                    "<td style='background:#ECECFF' colspan='3'>"+data[i].caselist[j].comments+"</td>"+
                    "</tr>";
            
            $dev_table.append($th_sub1)
        }
     }
}

function countRate(num1,num2){
    if (!isNaN(num1) && !isNaN(num2)){
        if (num1 > num2){ a=[num1,num2];num1=a[1];num2=a[0]}
        if (num1 == 0) {return '0%'}
        rate = Math.round((num1/num2)*10000)/100;
        return rate.toString()+"%"
  }else{
    alert("Parameters Num1 and Num2 must be a number!!!")
    return;
  }
}

function showDomainInfo(data){
    var data = data.results.domain
    var $dev_table = $('<table>').attr('class','table table-bordered');
    var $th = '<thead><tr>'+
              '<th width="4%"></th>'+
              '<th width="20%">Domain</th>'+
              '<th >Total</th>'+           
              '<th >Pass</th>'+            
              '<th >Fail</th>'+
              '<th >Block</th>'+
              '<th >Success Rate</th>'+
              '</tr></thead>';
    var $tbody = '<tbody></tbody>';
    $('#domain-div').html('').append($dev_table);
    $dev_table.append($th);
    $dev_table.append($tbody);

    for (var i = 0; i < data.length; i++){
          var passCount = data[i].passcnt;
          var totalCount = data[i].totalcnt;
          passRate = countRate(passCount,totalCount)

          var $tr = "<tr>"+ 
                "<td onclick=showPic('pic1_"+i.toString()+"') id='tr_domain_"+i.toString()+"';><img id='pic1_"+i.toString()+"' src='static/img/spread.png'></img></td>"+
                "<td style='font-size:15px'>"+data[i].domain+"</td>"+
                "<td>"+totalCount+"</td>"+
                "<td>"+passCount+"</td>"+ 
                "<td>"+data[i].failcnt+"</td>"+
                "<td>"+data[i].blockcnt+"</td>"+
                "<td>"+passRate+"</td>"+
                "</tr>"
          $dev_table.append($tr);

          var $th_sub = '<tr class="hidden" id="subtr_domain_'+i.toString()+'">'+
              '<td></td>'+
              '<th style="background:#ECECFF">Run Case</th>'+      
              '<th style="background:#ECECFF">Total</th>'+
              '<th style="background:#ECECFF">Pass</th>'+
              '<th style="background:#ECECFF;color:red">Fail</th>'+
              '<th style="background:#ECECFF">Block</th>'+
              '<th style="background:#ECECFF">Success Rate</th>'+
              '</tr>';
          $dev_table.append($th_sub);
          
          $('#tr_domain_'+i.toString()).toggle(function(){
              $('tr#sub'+this.id).removeClass('hidden');
            },function(){
              $('tr#sub'+this.id).addClass('hidden');
          });

          for (var j = 0; j < data[i].detail.length; j ++){
              var passCnt = data[i].detail[j].passcnt;
              var totalCnt = data[i].detail[j].totalcnt;
              var passRate1 = countRate(passCnt,totalCnt)
              var $th_sub1 = "<tr class='hidden' id='subtr_domain_"+i.toString()+"'>"+ 
                    '<td></td>'+ 
                    "<td style='background:#ECECFF'>"+data[i].detail[j].casename+"</td>"+            
                    "<td style='background:#ECECFF'>"+totalCnt+"</td>"+
                    "<td style='background:#ECECFF'>"+passCnt+"</td>"+
                    "<td style='background:#ECECFF;color:red'>"+data[i].detail[j].failcnt+"</td>"+
                    "<td style='background:#ECECFF'>"+data[i].detail[j].blockcnt+"</td>"+
                    "<td style='background:#ECECFF'>"+passRate1+"</td>"+
                    "</tr>";
            $dev_table.append($th_sub1)
       }
    }
}


var AppRouter = Backbone.Router.extend({
    routes: {
        "group/:gid" : "showGroupView",
        "group/:gid/session/:sid" : "showSessionView",
        "group/:gid/report/:cid" : "showReportView",
        "group/:gid/session/:sid/fail" : "showFailView"
    },
    showGroupView: function(gid){
        checkLogIn();
        $('#group-div').show();
        $('#session-div').hide();
        $('#session-name').hide();
        $('#report-div').hide();
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
        $('#report-div').hide();
        _appglobal.gid = gid;
        _appglobal.sid = sid;
        if(_appglobal.t1 !== undefined) clearInterval(_appglobal.t1);
        if(_appglobal.t2 !== undefined) clearTimeout(_appglobal.t2);
        showGroupInfo(gid);
        showSessionInfo(gid,sid);
    },
    showFailView: function(gid,sid){
        checkLogIn();   
        $('#group-div').hide();
        $('#session-div').show();
        $('#session-name').show();
        $('#report-div').hide();
        _appglobal.gid = gid;
        _appglobal.sid = sid;
        if(_appglobal.t1 !== undefined) clearInterval(_appglobal.t1);
        if(_appglobal.t2 !== undefined) clearTimeout(_appglobal.t2);
        showGroupInfo(gid);
        showFailuresInfo(gid,sid);
    },
    showReportView: function(gid,cid){
        checkLogIn();   
        $('#group-div').hide();
        $('#session-div').hide();
        $('#session-name').hide();
        $('#report-div').show();
        _appglobal.gid = gid;
        _appglobal.cid = cid;
        if(_appglobal.t1 !== undefined) clearInterval(_appglobal.t1);
        if(_appglobal.t2 !== undefined) clearTimeout(_appglobal.t2);
        showGroupInfo(gid);
        showReportInfo(gid,cid);
    }
});
var index_router = new AppRouter;
Backbone.history.start();
