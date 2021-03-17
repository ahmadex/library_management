$(function(){

    let pass1 = document.getElementById('id_password1')
    let pass2 = document.getElementById('id_password2')
    let phone = document.getElementsByName('phone_no')[0]
    pass2.addEventListener('blur',function(){

    if(pass1.value != pass2.value){
        alert('Two Passwords did not Match')
    }
    
    });


    $('#id_username').on('change',function(){
        
        $.ajax({

            url:'/library/username_valid/',
            method:'POST',
            data:{
                uname:$('#id_username').val(),
                csrfmiddlewaretoken:$("input[name='csrfmiddlewaretoken']").val()
            },
            success:function(data){
                if(data.taken){
                    alert('User with this Username Already Exist!')
                }
            }

        });
    });


});
