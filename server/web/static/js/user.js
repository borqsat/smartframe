function showUserInfo(){
      invokeWebApi('/account/info',
                   prepareData({}),
                   function(data){
                        data = data.results;
                        if(data === undefined) return;
                        var $username = $('#user-name').html('');
                        $username.append('<p class=\"bottom bold\">'+data['username']+'</p>')
                        var $usergrp = $('#user-groups').html('');
                        $.each(data['inGroups'],function(i, o) {
                            var $li = $('<li>');
                            $li.append('<a class=\"clearfix link-item highlight-icon js-open-board\" href=\"group.html?group='+o['gid']+'\">' + o['groupname']+ '</a>')
                            $usergrp.append($li);
                        })
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
        "":"showDefault"
    },
    showDefault: function(){
        checkLogIn();
        $('#user-view').show();        
        showUserInfo();
    }
});
var index_router = new AppRouter;
Backbone.history.start();
