function showUserInfo(){
      invokeWebApi('/account/info',
                   prepareData({}),
                   function(data){
                        data = data.results;
                        if(data === undefined) return;
                        var $username = $('#user-name').html('');
                        $username.append('<p class=\"bottom bold\">'+data['username']+'</p>')
                        var $usergrp = $('#user-groups').html('');
                        var groups = data['inGroups'];
                        groups.sort(function(a,b){return a['groupname'].toLowerCase() >= b['groupname'].toLowerCase()});
                        $.each(groups,function(i, o) {
                            var $li = $('<li>');
                            $li.append('<a class=\"clearfix link-item highlight-icon js-open-board\" href=\"group.html#group/'
                                       + o['gid'] + '\">' + o['groupname'] + '</a>')
                            $usergrp.append($li);
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
