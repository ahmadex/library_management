$(function(){

    let x = $('#id_no_of_copy');
    x.after(`<a href="#" id='plus' class="btn btn-primary btn-lg">+</a>`);
    x.after(`<a href="#" id='minus' class="btn btn-danger btn-lg">-</a>`);
    let y = $('#id_available_copy');
    y.attr("disabled","disabled");
    x.attr("disabled","disabled");

    $('#plus').on('click',function(){
        console.log($('#book_id').val());
        console.log($('#csr').val());      

        $.ajax({
            url:'/library/copy_incrmt/',
            method:'POST',
            data: {
                id:$('#book_id').val(),
                csrfmiddlewaretoken: $('#csr').val(),
                sign:'plus'
            },
            success: function(data){
                if(data.status == "1"){
                    x.val(data.book_copy);
                    y.val(data.avail);

                }
            }
        })
    });

    // no of copy decreament
    $('#minus').on('click',function(){
            
        let noOfCopy = Number($('#id_no_of_copy').val());
        if(noOfCopy < 1){
                alert('NO of Copies Can not be Negative')  
                throw error('Minus Copy not valid')
        }
            
        $.ajax({
            url:'/library/copy_incrmt/',
            method:'POST',
            data: {
                id:$('#book_id').val(),
                csrfmiddlewaretoken: $('#csr').val(),
                sign:'minus'
            },
            success: function(data){
                console.log(data.status)
                if(data.status == "1"){
                    x.val(data.book_copy);
                    y.val(data.avail);

                }
            }
        })
    });
});
