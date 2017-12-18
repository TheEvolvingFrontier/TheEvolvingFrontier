var useractions = (function() {
	var url = 'http://127.0.0.1:5000/' //CHANGE BEFORE DEPLOY
	var apiUrl = url + 'api/';
	var emailButton;
	var verifyButton;
	// getURLParameter is a direct copy off the internet
	// https://stackoverflow.com/questions/11582512/how-to-get-url-parameters-with-javascript
	function getURLParameter(name) 
	{
		return decodeURIComponent((new RegExp('[?|&]' + name + '=' + '([^&;]+?)(&|#|;|$)').exec(location.search) || [null, ''])[1].replace(/\+/g, '%20')) || null;
	}
	var makePostRequest = function(url, data, onSuccess, onFailure)
	{
		$.ajax({
			type: 'POST',
			url: apiUrl + url,
			data: data,
			contentType: "application/json",
			dataType: "json",
			success: function(response)
				{
					 onSuccess(response);
				},
			error: onFailure
		});
	};
	var attachEmailSendingHandler = function(e) 
	{
	//console.log('AESH START');
		emailButton.on("click", function () 
		{
			//console.error('MB START');
			var email = document.getElementById('emailInput').value;
			var onSuccess = function(data)
			{
				document.location = data[0].url; //email argument given in the app.py
				console.log('Email sending success:' + JSON.stringify(data));
			}
			var onFailure = function(data)
			{
				alert('Failure to send email');
				console.log('Email sending failure:' + JSON.stringify(data));
			}
			var dat = JSON.stringify({"email" : email});
			//console.log(dat + '       ' + apiUrl + 'newaccount');
			makePostRequest('newaccount', dat, onSuccess, onFailure);
			//console.log('MB END');
		});
	//console.error('AESH END');
	};
	var sendUserInfoHandler = function(e)
	{
		verifyButton.on("click",function()
		{
			usr = document.getElementById('usernameInput').value;
			pswd = document.getElementById('passwordInput').value;
			cPswd = document.getElementById('confirmpasswordinput').value;
			code = document.getElementById('codeinput').value;
			email = getURLParameter('email');
			alert(email);
			if(pswd == cPswd)
			{
				var onSuccess = function(data)
				{
					console.log('success in sendUserInfoHandler');
					document.location = data[0].url; // moves to facility page
				}
				var onFailure = function(data)
				{
					console.log('failure in sendUserInfoHandler');
					alert('failed to send or process information.');
				}
				var dat = JSON.stringify({'usr':usr,'pswd':pswd, 'code':code, 'email':email});
	                        makePostRequest('accountinfo', dat, onSuccess, onFailure); //sends account info
			}
			else
			{
				alert('passwords dont match');
			}
		});
	}
	var getCommInfo = function() 
	{
		var e = document.getElementById("Area");
		var str = e.options[e.selectedIndex].value;
		var x = parseInt(str) % 4;
		var y = parseInt(parseInt(str) / 4);
		var onSuccess = function(data)
		{
			console.log('success in comment pull');
			document.getElementById("servComments").innerHTML=data[0].comments;
		}
		var onFailure = function(data)
		{
			console.log('failure in comment pull');
		}
		var dat = JSON.stringify({'x':x, 'y':y});
		makePostRequest('getComments', dat, onSuccess, onFailure);
	}
	var postCom = function() {
		var myInp = document.getElementById("comInput");
		var myVal = myInp.value;
                var combo = document.getElementById("Area");
                var loc = combo.options[combo.selectedIndex].value;
		onSuccess = function(data)
		{
			console.log('succeaded in commenting');
			alert('comment has been posted')
		}
		onFailure = function(data)
		{
			alert('comment failed to post');
		}
		var dat = JSON.stringify({'comment':myVal, 'loc': loc});
		makePostRequest('postComment', dat, onSuccess, onFailure);
	}
	var start = function() {
		console.log('Start Start');
		emailButton = $("#myemailbutton"); //this is in the email page and eventually leads to verification page
		attachEmailSendingHandler();
		verifyButton = $("#verifyButton"); //this is in the verification page
		sendUserInfoHandler();
		log2fac = $("#log2fac");
		log2fac.on("click",function(){
				document.location = url + 'facilitySense.html'
			});
		log2new = $("#log2new");
		log2new.on("click",function(){
                                document.location = url + 'newAccountEmail.html'
                        });
		facComVis = $("#showComments");
		facComVis.on("click", function(){
				var comBox = document.getElementById('commentBox')
				if(comBox.style.visibility != "hidden")
				{
					comBox.style.visibility = "hidden"
				}
				else
				{
					comBox.style.visibility = "visible"
				}
				});
		$("#Area").change(function(){
                		getCommInfo()
			});
		$("#postCom").on("click", function(){
				postCom()
			});
		console.log('Start End');
	};
        return {
        start: start
        };
})()
