
$(document).ready(function () {
 $.ajax('http://127.0.0.1:8000/captcha/getStart/?client_key=inlOpgbwgZ108OX',{
 type: "GET",
 success: function(response) {
    $("#fairCaptcha").append(response);    
 }}); 
});
