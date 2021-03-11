$(function(){

    //check if avaible books are 0 then remove issu btn nd show msg
    if (Number($('#avail').text()) < 1){
        $('#issue-btn').remove();
        $('#msgbox').after(`<div class="alert alert-danger">
        <strong>Sorry!!</strong> Book is Not Available.
      </div>`)    
    }

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
                if(data.status == 0){
                    alert(data.msg);
                }
                else if(data.status == 2){
                    alert(data.msg);
                }
                else{
                    $('#avail').text(data.avail);
                    let btn = $('#issue-btn');
                    btn.text('Book Issued')
                }
                
                

            }
        })
    });

});