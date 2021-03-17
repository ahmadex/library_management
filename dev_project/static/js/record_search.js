$(function(){
    $('#record').on('input',function(){
        let record = $('#record').val();    
      if(record != ""){
            $.ajax({

                url:'/library/record_search/',
                method:'GET',
                data:{
                    title:record
                },
                success:function(data){
                    if(data.records.length > 0){
                        console.log(data);
                        $('#old-table').remove();
                        th = `
                        <table id='new-table' class="table student-list">
                        <thead class="thead-light">
                            <tr>
                            <th scope="col">ID</th>
                            <th scope="col">Title</th>
                            <th scope="col">User</th>
                            <th scope="col">Issue Date</th>
                            <th scope="col">Due Date</th>
                            <th scope="col">Return Date</th>
                            </tr>
                        </thead>
                        <tbody>`

                        for(let i=0; i<data.records.length; i++){
                            th  += `<tr>
                                <td>${data.records[i]['id']}</td>
                                <td>${data.records[i]['book']}</td>
                                <td>${data.records[i]['user']}</td>
                                <td>${data.records[i]['isuue_date']}</td>
                                <td>${data.records[i]['due_date']}</td>`
                            if(data.records[i]['return_date'] == null){
                                th += `<td>--------</td>`
                            }
                            else{
                                th += `<td>${data.records[i]['return_date']}</td>`
                            }
                            th += `</tr>`
                        }
                        th += `</tbody>
                        </table>`

                        $('#contain').html(th);

                    }
                    else{
                        $('#contain').html(`<div class="alert alert-danger">
                        <strong>Oopss!!!</strong> The Record U r Looking for is not Available.
                    </div>`)
                    }

                }

            });
        }
        else{
            // $('#new-table').remove();
            // let new_th = oldHtml.outerHTML;
            // $.each(oldHtml, function(k,v){
            //     console.log(k,v);
            // });
            // $('#contain').html(new_th);
        }
      
    });


});