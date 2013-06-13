function TablePage(gid, sid, numPages, pageSize, renderfunc, id, tag) {
    var $table = $('#'+id);
    var currentPage = 0;
    $table.bind("repaginate", function()
    {   
        invokeWebApi('/group/'+gid+'/test/'+sid+'/history',
                    prepareData({'type': tag, 'page': (currentPage+1), 'pagesize':pageSize} ),
                    function(data){
                        if(data.results === undefined) return;
                        var caseslist = data.results.cases;
                        renderfunc(gid, sid, caseslist, id, tag);
                    });
    })
    
    var $pager = $("<div class = 'page'><a href = 'javascript:void(0)'><span id = 'Prev' style = 'margin-right:4px;'>« Prev</span></a></div>");  //分页div
    for(var page = 0; page < numPages; page++)
    {
        $("<a href = 'javascript:void(0)' class = 'pageno'><span id = '"+(page+1)+"'>"+ (page+1) +"</span></a>")
            .bind("click", { "newPage": page }, function(event){
                currentPage = event.data["newPage"];
                $(this).children("span").attr("class","click_page");
                $(this).children("span").css({"color":"#000000"}).css({"font-weight":"bold"});
                $(".page a span").not($(this).children("span")).attr("class","");
                $(".page a span").not($(this).children("span")).css({"color":"#0088cc"}).css({"font-weight":"normal"});
                $table.trigger("repaginate");
            })
            .appendTo($pager);
        $pager.append("  ");
    }
    var next = $("<a href = 'javascript:void(0)'><span id = 'Next'>Next »</span></a>");
    $pager.append(next);
    $pager.insertBefore($table);//分页div插入table
    $("#1").attr("class","click_page");
    $("#1").css({"color":"#000000"});
    $("#Prev").bind("click",function(){
        var prev = Number($(".click_page").text())-2;
        currentPage = prev;
        if(currentPage < 0) {
            return;
        }
        $("#"+(prev+1)).attr("class","click_page");
        $("#"+(prev+1)).css({"color":"#000000"}).css({"font-weight":"bold"});
        $(".page a span").not($("#"+(prev+1))).attr("class","");
        $(".page a span").not($("#"+(prev+1))).css({"color":"#0088cc"}).css({"font-weight":"normal"});
        $table.trigger("repaginate");
    });

    $("#Next").bind("click",function(){
        var next = $(".click_page").attr("id");
        currentPage = Number(next);
        if((currentPage+1) > numPages) {
           return;
        }
        $("#"+(currentPage+1)).attr("class","click_page");
        $("#"+(currentPage+1)).css({"color":"#000000"}).css({"font-weight":"bold"});
        $(".page a span").not($("#"+(currentPage+1))).attr("class","");
        $(".page a span").not($("#"+(currentPage+1))).css({"color":"#0088cc"}).css({"font-weight":"normal"});
        $table.trigger("repaginate");
    });
    
 }
