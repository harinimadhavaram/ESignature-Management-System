$(function(){
	$('#btnSignUp').click(function(){
		console.log("This is working so far");
		$.ajax({
			url: '/showsignup',
			data: $('form').serialize(),
			type: 'POST',
			success: function(response){
				console.log(response);
			},
			error: function(error){
				console.log(error);
			}
		});
	});
});
