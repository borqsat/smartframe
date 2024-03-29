function showUserInfo(){
      invokeWebApi('/account/info',
                   prepareData({}),
                   function(data){
                        data = data.results;
                        if(data === undefined) return;
                        
				    	var avatar = data.info['avatar'];
				    	var default_avatar = data.info['default_avatar'];
				    	var uploaded_avatar = data.info['uploaded_avatar'];
				    	
				    	switch (avatar)
				    	{
				    	case "default_avatar":
				    		if (default_avatar !== undefined){
				    			path = default_avatar;
				    			if (uploaded_avatar !== undefined){
				    				upload = storeBaseURL + "/snap/" + uploaded_avatar;
				    				$("#upload_avatar").attr("src",upload);
				    			}else{
				    				$("#upload_avatar").attr("src",path);
				    			}
				    			$("#initial_hint").attr("src","static/css/images/display.png");
				    			$("#upload_hint").attr("src","static/css/images/none.png");
				    		}else{
				    			alert("Can not get the default avatar!!!");
				    			return;
				    		}
				    		break;
				    	case "uploaded_avatar":
				    		if (uploaded_avatar !== undefined) {
				    			path = storeBaseURL + "/snap/" + uploaded_avatar;
				    			$("#upload_avatar").attr("src",path);
				    		}else{
				    			alert("You haven't upload the avatar, so can not get it!!!");
				    			return;
				    		}
				    		$("#initial_hint").attr("src","static/css/images/none.png");
				    		$("#upload_hint").attr("src","static/css/images/display.png");
				    		break;
				    	default:
				    		path = "http://storage.aliyun.com/wutong-data/system/1_L.jpg";
				    	}
			    		$("#profile-avatar").attr("src",path);
			    		$("#small-avatar").attr("src",path);
			    		$('#avatar_panel').css("display","none");
                        var $username = $('#user-name').html('');
                        $username.append('<p class=\"bottom bold\">'+data['username']+'</p>')
                        var $usergrp = $('#user-groups').html('');
                        var groups = data['inGroups'];
                        groups.sort(function(a,b){return a['groupname'].toLowerCase() >= b['groupname'].toLowerCase()});
                        $.each(groups,function(i, o) {
                            var $li = $('<li>');
                            var showdel = o['role']=='1'? '[x]':'';
                            $li.append('<a class=\"clearfix link-item highlight-icon js-open-board\" id=\"group' + o['gid'] + '\">'
                                       + '<span class=\"item-name\">' + o['groupname'] + '</span>'
                                       + '<span class=\"list-item-menu\" id=\"group-icon' + o['gid'] + '\">'
                                       + showdel
                                       + '</span>'
                                       +'</a>')
                            $usergrp.append($li);
                            $('#group'+o['gid']).attr('href', "group.html#group/"+ o['gid'] );
                            $('#group-icon'+o['gid']).bind('click',function () {
                                                                                 deleteGroup(o['gid']);  
                                                                                return false;
                                                                             });

                        });
                        var $usertst = $('#user-tests').html('');
                        var tests = data['inTests']
                        tests.sort(function(a,b){return a['groupname'].toLowerCase() >= b['groupname'].toLowerCase()});
                        $.each(tests,function(i, o) {
                            var $li = $('<li>');
                            $li.append('<a class=\"clearfix link-item highlight-icon js-open-board\" href=\"group.html#group/'
                                        + o['gid'] + '/session/' + o['sid']+ '\">' + o['groupname'] + '-' + o['sessionid'] + '</a>')
                            $usertst.append($li);
                        });

                 })
      $('#dialog-group').dialog(
                      {
                        resizable:false,
                        autoOpen: false,
                        modal: true,
                        buttons:{
                          "Create":function(){
                              $dlg = $(this);
                              invokeWebApiEx('/group/create',
                                              prepareData({'groupname':$('#dialog-group #name').val(),'info':{}}),
                                              function(data) {
                                                  showUserInfo();
                                                  $dlg.dialog("close"); 
                                              }
                                            )
                          },
                          "Cancel":function(){
                              $(this).dialog("close");
                          }
                        }
                      })
      $("#create-group")
            .button()
            .click(function() {
                $("#dialog-group").dialog("open");
            });
}

function deleteGroup(gid){
      if(confirm('Confirm to delete this group?')) {
        invokeWebApi('/group/'+gid+'/delete',
                    prepareData({}),
                    function(data) {
                       showUserInfo();
                    });
    }
}


var AppRouter = Backbone.Router.extend({
    routes: {
        "":"showDefault",
        "showTests":"showTests"

    },
    showDefault: function(){
        checkLogIn();
        $('.js-member-groups').addClass('active');
        $('.js-member-tests').removeClass('active');
        $('#group-div').show();
        $('#session-div').hide();        
        showUserInfo();
    },
    showTests: function(){
        checkLogIn();
        $('.js-member-groups').removeClass('active');
        $('.js-member-tests').addClass('active');
        $('#group-div').hide();
        $('#session-div').show();
        showUserInfo();
    }
});
var index_router = new AppRouter;
Backbone.history.start();
