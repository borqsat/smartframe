function afterlogin(data) {
    ret = data['results'];
    if (ret !== undefined && ret['token'] !== undefined) {
        $.cookie('ticket', ret['token'], { expires: 7 });
        $.cookie('username', $('#username').val(), { expires: 7 });
        $.cookie('userid', ret['uid'], { expires: 7 });                    
        window.location = "index.html";
    }
}

function afterRegister(data) {
    var ret = data["errors"];
    if(ret !== undefined ) {
        alert(ret["msg"]);
    } else {
        alert("Register account successfully!");
        window.location = "login.html";
    }
}


function afterUpdate(data) {
    var ret = data["errors"];
    if(ret !== undefined ) {
        alert(ret["msg"]);
    } else {
        alert("Update account successfully!");
        window.location = "index.html";
    }
}

function afterChnpass(data) {
    var ret = data["errors"];
    if(ret !== undefined ) {
        alert(ret["msg"]);
    } else {
        alert("Change password successfully!");
        window.location = "login.html";
    }
}

var AppRouter = Backbone.Router.extend({
    routes: {
         "":"showLogin",
         "signup":"showSignup",
         "editaccount":"showeditaccount"
    },
    showLogin: function(){
         $('#login-view').show();
         $('#signup-view').hide();
         $('#editaccount-view').hide();  
         $('#btnlogin').bind('click',
                             function(){
                                  var username = $('#username').val();
                                  var password = $('#password').val();
                                  if(username === '' || password === '') {
                                      $('#warning').html('<p class="error">The username,password can\'t be null.</p>');
                                      return;
                                  }
                                  $.cookie('password', password, { expires: 7 });
                                  invokeWebApiEx("/account/login", 
                                                  {"username": username, "password": hex_md5(password), "appid":"02"},
                                                  afterlogin);
                             })
          $('#btndownload').bind('click',function(){window.open('static/runner.tar.gz')})
    },
    showSignup: function(){
         $('#login-view').hide();
         $('#signup-view').show();
         $('#editaccount-view').hide();
         $('#btnsignup').bind('click',
                             function(){
                                 var email = $('#regemail').val();                              
                                 var password = $('#regpassword').val();
                                 var username = $('#regusername').val();
                                 var phone = $('#regphone').val();
                                 var company = $('#regcompany').val();
                                 var pattern = /^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+(.[a-zA-Z0-9_-])+/;
                                 $('#regwarning').html('');
                                 if(email === '' || username === '' || password === '') {
                                     $('#regwarning').html('<p class="error">The email, username, password can\'t be null.</p>');
                                     return;
                                 }
                                 invokeWebApiEx("/account/register",
                                                { 
                                                "username":username,
                                                "password":password,
                                                "appid":"01",
                                                "info":{"email":email, "phone":phone, "company":company}
                                                },
                                                afterRegister
                                  );
               })
    },
    showeditaccount: function(){
         $('#login-view').hide();
         $('#signup-view').hide();
         $('#editaccount-view').show();
         $('#btnchnpass').bind('click',
                             function(){                       
                                 var oldpassword = $('#orgpassword').val();
                                 var newpassword = $('#newpassword').val();
                                 var confpassword = $('#confpassword').val();
                                 $('#txtwarning').html('');
                                 if(oldpassword === '' || newpassword === '' || confpassword === '') {
                                     $('#txtwarning').html('<p class="error">The oldpassword, newpassword, confpassword can\'t be null.</p>');
                                     return;
                                 }
                                 if(newpassword !== confpassword ) {
                                     $('#txtwarning').html('<p class="error">The newpassword, confpassword are not consistent.</p>');
                                     return;
                                 }
                                 invokeWebApiEx("/account/changepasswd",
                                                prepareData({
                                                "oldpassword":oldpassword,
                                                "newpassword":newpassword
                                                }),
                                                afterChnpass
                                  );
               });


         $('#btnupdate').bind('click',
                             function(){
                                 var email = $('#upemail').val();                         
                                 var phone = $('#upphone').val();
                                 var company = $('#upcompany').val();
                                 var info = {};
                                 if (email !== '') info["email"] = email;
                                 if (password !== '') info["phone"] = phone;
                                 if (company !== '') info["company"] = company;

                                 $('#txtwarning').html('');
                                 invokeWebApiEx("/account/update",
                                                prepareData({
                                                "password":password,
                                                "info":info
                                                }),
                                                afterUpdate
                                  );
               })
   }

});
var loginRouter = new AppRouter;
Backbone.history.start();
