$(function() {
	$(".btn").click(function() {
		$(".form-signin").toggleClass("form-signin-left");
    $(".form-signup").toggleClass("form-signup-left");
    $(".frame").toggleClass("frame-long");
    $(".signup-inactive").toggleClass("signup-active");
    $(".signin-active").toggleClass("signin-inactive");
    $(".forgot").toggleClass("forgot-left");
    $(this).removeClass("idle").addClass("active");
	});
});

function reg(){
    var phototval = new XMLHttpRequest();
    phototval.open('GET', "/reg?FIO=" + document.getElementById('fullname').value + '&email=' + document.getElementById('email').value
    + "&password1=" + document.getElementById('paassword').value + "&password2=" + document.getElementById('confirmpassword').value, true);
    phototval.send();
}

$(function() {
	$(".btn-signup").click(function() {
	reg();
  $(".nav").toggleClass("nav-up");
  $(".form-signup-left").toggleClass("form-signup-down");
  $(".success").toggleClass("success-left");
  $(".frame").toggleClass("frame-short");
	});
});

//$(function() {
//	$(".btn-signin").click(function () {
//		$(".btn-animate").toggleClass("btn-animate-grow");
////		$(".welcome").toggleClass("welcome-left");
////		$(".cover-photo").toggleClass("cover-photo-down");
////		$(".frame").toggleClass("frame-short");
////		$(".profile-photo").toggleClass("profile-photo-down");
////		$(".btn-goback").toggleClass("btn-goback-up");
////		$(".forgot").toggleClass("forgot-fade");
//	});
//});