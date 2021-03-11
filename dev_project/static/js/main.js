let pass1 = document.getElementById('id_password1')
let pass2 = document.getElementById('id_password2')
let phone = document.getElementsByName('phone_no')[0]
pass2.addEventListener('blur',function(){

    if(pass1.value != pass2.value){
        alert('Two Passwords did not Match')
    }
    
});

// phone.addEventListener('input',function(){
//     if(phone.value != typeof ''){
//         alert('Phone no does not support Character')
//     }
// });