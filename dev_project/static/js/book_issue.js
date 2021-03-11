$(function(){

    $('#issue-btn').on('click',function(){
        
        $.ajax({
            url:'/library/book_issue/',
            method:'POST',
            data:{
                book_id:$('#book-id').text(),
                user_id:$('#user-id').val(),
                csrfmiddlewaretoken:$('#csr').val(),
            },
            success: function(data){
                $('#avail').text(data.avail);
                let btn = $('#issue-btn');
                btn.text('Book Issued')
                

            }
        })
    });

});