$(function(){
        
    //No of copies increament
    
    $('#plus').on('click',function(){
        $.ajax({
            url:'/library/copy_incrmt/',
            method:'POST',
            data: {
                id:$('#book_id').text(),
                csrfmiddlewaretoken: $('#copy').val(),
                sign: 'plus'
            },
            success: function(data){
                console.log(data.status)
                if(data.status == "1"){
                    $('#no_copy').text(data.book_copy) 
                    $('#avail').text(data.avail)
                }
            }
        });
    });


    // no of copies decreamnet

    $('#minus').on('click',function(){

        if(Number($('#no_copy').text()) < 1){
            alert('NO of Copies Can not be Negative')  
            throw error('Minus Copy not valid')
        }

        let bookId = $('.text-muted').text()
        
        $.ajax({
            url:'/library/copy_incrmt/',
            method:'POST',
            data: {
                id:$('#book_id').text(),
                csrfmiddlewaretoken: $('#copy').val(),
                sign: 'minus'
            },
            success: function(data){
                console.log(data.status)
                if(data.status == "1"){
                    $('#no_copy').text(data.book_copy)
                    $('#avail').text(data.avail)
                }
            }
        })
    });


});

