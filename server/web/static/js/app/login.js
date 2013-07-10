function showTab(tabHeadId,tabContentId)
        {

            //tab层

            var tabDiv = document.getElementById("tabDiv");

            //将tab层中所有的内容层设为不可见

            //遍历tab层下的所有子节点

            var taContents = tabDiv.childNodes;

            for(i=0; i<taContents.length; i++)

            {

                //将所有内容层都设为不可见

                if(taContents[i].id!=null && taContents[i].id != 'tabsHead')

                {

                    taContents[i].style.display = 'none';

                }

            }

            //将要显示的层设为可见

            document.getElementById(tabContentId).style.display = 'block';

           

            //遍历tab头中所有的超链接

            var tabHeads = document.getElementById('tabsHead').getElementsByTagName('a');

            for(i=0; i<tabHeads.length; i++)

            {

                //将超链接的样式设为未选的tab头样式

                tabHeads[i].className='tabs';

            }

            //Set current Hyperlink style as the selected tab header style

            document.getElementById(tabHeadId).className='curtab';

            document.getElementById(tabHeadId).blur();

        }
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
        //window.location = "group.html";
    }
}

function afterUpdateEmail(data) {
    var ret = data["errors"];
    if(ret !== undefined ) {
        alert(ret["msg"]);
    } else {
        //alert("Update account successfully!");
        window.location = "login.html#emailVerify";
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

function viewTab1(){
    $('#tab1').addClass('active');
    $('#tab2').removeClass('active');
    $('#tab3').removeClass('active');
    $('#change_pass_panel').show();
    $('#change_userinfo_panel').hide();  
    $('#email_verify_panel').hide();    
}

function viewTab2(){
    $('#tab1').removeClass('active');
    $('#tab2').addClass('active');
    $('#tab3').removeClass('active');
    $('#change_pass_panel').hide();
    $('#change_userinfo_panel').show();  
    $('#email_verify_panel').hide();   
}

function viewTab3(){
    $('#tab1').removeClass('active');
    $('#tab2').removeClass('active');
    $('#tab3').addClass('active');
    $('#change_pass_panel').hide();
    $('#change_userinfo_panel').hide();  
    $('#email_verify_panel').show();   
}

function checkemail(){
var temp = document.getElementById("upemail");
var myreg = /^\w+((-\w+)|(\.\w+))*\@[A-Za-z0-9]+((\.|-)[A-Za-z0-9]+)*\.[A-Za-z0-9]+$/;

//  /^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+(.[a-zA-Z0-9_-])+/;

//  /^w+((-w+)|(.w+))*@[A-Za-z0-9]+((.|-)[A-Za-z0-9]+)*.[A-Za-z0-9]+$/;
if(temp.value!=""){
if(!myreg.test(temp.value)){
document.getElementById("mail").innerHTML="请输入有效的email!";
document.getElementById("mail").style.color="red";
temp.value="";
temp.focus();
return false;
}else{
document.getElementById("mail").innerHTML="email可以使用";
document.getElementById("mail").style.color="green";
}
}
}

//show user info
 
function showEditAccountInfo(){
      invokeWebApi('/account/info',
                   prepareData({}),
                   function(data){
                        data = data.results;
                        email = data.info['email'];
                        phone = data.info['phone'];
                        company = data.info['company'];
                        //upemail.value=email
                        //upcompany.value=company
                        //upphone.value=phone
                        $('#oldemail').html('<label style="color:#991515" />'+ email+'</label>')                       
                        $('#upemail').val(email);
                        $('#upcompany').val(company);
                        $('#upphone').val(phone);
                   })
        }     
                        
var AppRouter = Backbone.Router.extend({
    routes: {
         "":"showLogin",
         "signup":"showSignup",
         "editaccount":"showeditaccount",
         "emailVerify":"showemailverify"
    },
    showLogin: function(){
         $('#login-view').show();
         $('#signup-view').hide();
         $('#editaccount-view').hide();  
         $('#emailVerify-view').hide();
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
         $('#emailVerify-view').hide();
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
         $('#emailVerify-view').hide();
         
         showEditAccountInfo();
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
               
          $('#btneditemail').bind('click',
                             function(){
                                 document.getElementById("upemail").style="";
                                 $('#upemail').show();
                                 $('#oldemail').hide();
                                 $('#btneditemail').hide();
                                 $('#btnconfirmemail').show();
                                 $('#btnCancelUpdateEmail').show();
                                 
                                 })
          
          $('#oldEmail').html('')       
          $('#oldEmail').html('<label style="color:#FFEFD5" />'+ $('#upemail').val()+'</label>')
          
          invokeWebApi('/account/info',
                                   prepareData({}),
                                   function(data){
                                        data = data.results;
                                        oldemail = data.info['email'];
                                   })
          
          $('#btnconfirmemail').bind('click',
                             function(){
                                 var email = $('#upemail').val();  
                                 var phone = $('#upphone').val();
                                 var company = $('#upcompany').val();
                                 var info = {};
                                 if (email !== '') info["email"] = email;
                                 if (password !== '') info["phone"] = phone;
                                 if (company !== '') info["company"] = company;
                                 if (oldemail === email) {
                                     document.getElementById("emailExists").style.display="block";
                                 }
                                 else {
                                     invokeWebApiEx("/account/update",
                                                prepareData({
                                                "password":password,
                                                "info":info
                                                }),
                                                afterUpdateEmail
                                  );
                                 }
                                 
                                  
               })
          $('#btnCancelUpdateEmail').bind('click',
                             function(){
                                 //document.getElementById("upemail").style="display:none";
                                 $('#upemail').hide();
                                 $('#oldemail').show();
                                 $('#btneditemail').show();
                                 $('#btnconfirmemail').hide();
                                 $('#btnCancelUpdateEmail').hide();
               })
               
     },
     showemailverify: function(){
         $('#login-view').hide();
         $('#signup-view').hide();
         $('#editaccount-view').hide();
         $('#emailVerify-view').show();
     }
});
var loginRouter = new AppRouter;
Backbone.history.start();
