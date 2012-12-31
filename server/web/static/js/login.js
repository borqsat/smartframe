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

var AppRouter = Backbone.Router.extend({
    routes: {
         "":"showLogin",
         "signup":"showSignup",
    },
    showLogin: function(){
         $('#login-view').show();
         $('#signup-view').hide();   
         $('#btnlogin').bind('click',
                             function(){
                                  var username = $('#username').val();
                                  var password = $('#password').val();
                                  if(username === '' || password === '') {
                                      $('#warning').html('<p class="error">The username & password can\'t be null.</p>');
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
         $('#btnsignup').bind('click',
                             function(){
                                 var email = $('#regemail').val();                              
                                 var password = $('#regpassword').val();
                                 var username = $('#regusername').val();
                                 if(email === '' || username === '' || password === '') {
                                      $('#regwarning').html('<p class="error">The email& username & password can\'t be null.</p>');
                                      return;
                                  }
                                 invokeWebApiEx("/account/register",
                                                { 
                                                "username":username,
                                                "password":password,
                                                "appid":"01",
                                                "info":{"email":email,"phone":"N/A","company":"N/A"}
                                                },
                                                afterRegister
                                  );
               })
   }
});
var loginRouter = new AppRouter;
Backbone.history.start();