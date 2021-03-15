$(function(){

    $('.return-btn').on('click',function(){
        let row = this.closest('tr');
        let title = row.cells[0].innerText;         
        let username = $('#username').text()
        $.ajax({
            url:'/library/book_return/',
            method:'POST',
            data:{
                book:title,
                user:username,
                csrfmiddlewaretoken:$('#csr').val()
            },
            success:function(data){
                console.log(data);
                row.setAttribute('id','dlt');
                let x = $('#dlt')
                x.fadeOut(2000);
                row.setAttribute('id','dlt1');
                // x.remove();
                          
            }
        });
    });
});