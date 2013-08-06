function afterRequest(data){
   showCommentInfo(data);
   showCycleBaseInfo(data);
   showFailureSummaryInfo(data);
   showFailureDetailsInfo(data);
   showDomainInfo(data);

}

function showReportInfo(token){
    invokeWebApiEx("/token/reportdata",
                   {"token" : token},
                   afterRequest);
}

function toggle(){
    var articleID=document.getElementById("article");
    if (articleID.style.display=="none"){
        articleID.style.display="block";
    } else {
        articleID.style.display="none";
    }
}

function showCommentInfo(data){
    $('#show-title').html('<a style="text-align:center" href=\"javascript:void(0)\" onclick=\"toggle()\">Tap here to get more information</a>');
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

function showFailureDetailsInfo(data){
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
                    "<td>"+deviceSerial+"</td>"+
                    "<td>"+data[i].starttime+"</td>"+
                    "<td>"+data[i].endtime+"</td>"+ 
                    (failureCount==0?"<td style='text-align:center'>"+0+"</td>":"<td style='text-align:center'>"+failureCount+"</td>")+
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
        "token/:token" : "showReportView"
    },
    showReportView: function(token){
        $('#report-div').show();
        showReportInfo(token);
    }
});
var index_router = new AppRouter;
Backbone.history.start();
