$('#change_avatar').bind("click",
		function(){
		    var panel=document.getElementById("avatar_panel");
		    if (panel.style.display=="none"){
		    	panel.style.display="block";
		    } else {
		    	panel.style.display="none";
		    }
});

$('#close_panel').bind("click",
		function(){	
			$('#avatar_panel').css("display","none");
});

$("#initial_div").bind("click", function(){
    var info = {"avatar":"default_avatar", "default_avatar":"http://storage.aliyun.com/wutong-data/system/1_L.jpg"};
    invokeWebApiEx("/account/update",
                   prepareData({
                	   "info":info,
                	   }),
                   afterChangeToIniteAvatar);
});

function afterChangeToIniteAvatar(){
    $("#profile-avatar").attr("src","http://storage.aliyun.com/wutong-data/system/1_L.jpg");
	$("#small-avatar").attr("src","http://storage.aliyun.com/wutong-data/system/1_S.jpg");
	$("#initial_hint").attr("src","static/css/images/display.png");
	$("#upload_hint").attr("src","static/css/images/none.png");
	$('#avatar_panel').css("display","none");
}

$("#upload_div").bind("click", function(){
	  invokeWebApi('/account/info',
				prepareData({}),
				function(data){
			    	data = data.results;
			    	if(data === undefined) return;
			    	
			    	uploaded_avatar = data.info['uploaded_avatar'];
			    	if(uploaded_avatar !== undefined){
			    			path = storeBaseURL + "/snap/" + uploaded_avatar;
			    	}else{
			    			alert("You haven't upload the avatar, so can not get it!!!")
			    			return;
			    	}
			    	$("#profile-avatar").attr("src",path);
			    	$("#small-avatar").attr("src",path);
			    	$("#upload_avatar").attr("src",path);
			    	$("#upload_hint").attr("src","static/css/images/display.png");
			    	$("#initial_hint").attr("src","static/css/images/none.png");
			    	$('#avatar_panel').css("display","none");
				});
	  info = {}
	  info['avatar'] = "uploaded_avatar";
	  invokeWebApiEx("/account/update",
			  		prepareData({"info":info}),
			  		function(data){
		  				var ret = data['errors'];
		  				if (ret !== undefined){
		  					alert(ret['msg'])
		  				}
	  				});
});

$('#upload_file').bind("change",
		function(){
					
                    invokeWebApiEx("/account/update",
                                   prepareData({}),
                                   aferUploadAvatar,
                                  "avatarForm");
});

function aferUploadAvatar(data){
	var ret = data['errors'];
	if(ret !== undefined) {
		alert(ret["msg"]);
	} else {
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
					});
		}
};

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
    }
}

function afterUpdateEmail(data) {
    var ret = data["errors"];
    if(ret !== undefined ) {
        alert(ret["msg"]);
    } else {
        window.location = "login.html#emailVerify";
    }
}

function sendEmailForForgotPasswd(data) {
    var ret = data["errors"];
    if(ret !== undefined ) {
        //alert(ret["msg"]);
        alert('No this user or your email not activity before !');
    } else {
        alert('Sent new password to your email successful!')
        window.location = "login.html";
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
    if(temp.value!=""){
        if(!myreg.test(temp.value)){
            document.getElementById("mail").innerHTML="请输入有效的email!";
            document.getElementById("mail").style.color="red";
            temp.value="";
            temp.focus();
            return false;
        } else {
            document.getElementById("mail").innerHTML="email可以使用";
            document.getElementById("mail").style.color="green";
        }
    }
}


function checkemail1(){
    var temp = document.getElementById("verify_email");
    var myreg = /^\w+((-\w+)|(\.\w+))*\@[A-Za-z0-9]+((\.|-)[A-Za-z0-9]+)*\.[A-Za-z0-9]+$/;
    if(temp.value!=""){
        if(!myreg.test(temp.value)){
            document.getElementById("mail1").innerHTML="请输入有效的email!";
            document.getElementById("mail1").style.color="red";
            temp.value="";
            temp.focus();
            return false;
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
         "forgotpassword":"forgotpassword",
         "emailVerify":"showemailverify"
    },
    showLogin: function(){
         $('#login-view').show();
         $('#signup-view').hide();
         $('#editaccount-view').hide();  
         $('#emailVerify-view').hide();
         $('#forgotpassword').hide();
         $('#btnlogin').bind('click',
                             function(){
                                  var username = $('#username').val();
                                  var password = $('#password').val();
                                  if(username === '' || password === '') {
                                      $('#warning').html('<p class="error">The username,password can\'t be null.</p>');
                                      return;
                                  }
                                  $.cookie('password', password, { expires: 7 });
                                  invokeWebApiEx("/account", 
                                                  {"action": "login", "data":{"username": username, "password": hex_md5(password), "appid":"02"}},
                                                  afterlogin);
                             })
          $('#btndownload').bind('click',function(){window.open('static/runner.tar.gz')})
    },
    showSignup: function(){
         $('#login-view').hide();
         $('#signup-view').show();
         $('#editaccount-view').hide();
         $('#emailVerify-view').hide();
         $('#forgotpassword').hide();
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
         $('#forgotpassword').hide();
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
                                 var phone = $('#upphone').val();
                                 var company = $('#upcompany').val();
                                 var info = {};
                                 if (phone !== '') info["phone"] = phone;
                                 if (company !== '') info["company"] = company;
                                 $('#txtwarning').html('');
                                 invokeWebApiEx("/account/update",
                                                prepareData({"info":info}),
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
                                 var info = {};
                                 if (email !== '') info["email"] = email;
                                 if (oldemail === email) {
                                        document.getElementById("emailExists").style.display="block";
                                 }
                                 else {
                                     invokeWebApiEx("/account/update",
                                                    prepareData({"info":info}),
                                                    afterUpdateEmail);
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
     forgotpassword: function(){
         $('#login-view').hide();
         $('#signup-view').hide();
         $('#editaccount-view').hide();
         $('#emailVerify-view').hide();
         $('#forgotpassword').show();
         $('#btnSendEmailForgotPass').bind('click',
                             function(){
                                 var email = $('#verify_email').val();  
                                 if (email === ''){
                                     alert('Please input correct email!');
                                 }else{
                                     invokeWebApiEx("/account/forgotpasswd",
                                                    prepareData({'email':email}),
                                                    sendEmailForForgotPasswd);
                                 }
                                  
               })
     },
     showemailverify: function(){
         $('#login-view').hide();
         $('#signup-view').hide();
         $('#editaccount-view').hide();
         $('#forgotpassword').hide();
         $('#emailVerify-view').show();
     }
});
var loginRouter = new AppRouter;
Backbone.history.start();
