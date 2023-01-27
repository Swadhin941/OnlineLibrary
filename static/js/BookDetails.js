$(document).ready(function () {
    $("dt").mouseover(function () {
        let current = $(this);
        $("dt").each(function (index) {
            $(this).addClass('text-warning')
            if (index == current.index()) {
                return false;
            }
        })
    })
    $("dt").click(function () {
        $("dt").removeClass("text-yellow")
        $(".text-warning").addClass("text-yellow")
        $("#mass").html($(".text-yellow").length)
        rat_val = $(".text-yellow").length

        $.ajax({
            url: '/rating',
            type: 'get',
            data: {
                isbn: "{{book[2]}}",
                rating: rat_val
            },
            success: function (data) {
                alert('Your'+rat_val+' rating has been updated')
            }
        })
    })
    $("dt").mouseleave(function () {
        $("dt").removeClass('text-warning');
    })

    document.getElementById('cart').addEventListener('click', function () {
        let bookname = "{{book[1]}}"
        let authorname = "{{book[4]}}";
        let isbn = "{{book[2]}}";
        let image = "{{book[5]}}";
        let price = "{{book[8]}}";
        let username = "{{session.get('username')}}";
        let userid = "{{session.get('userid')}}";
        console.log(bookname, authorname)
        $.ajax({
            url: "/addtocart",
            type: "GET",
            contentType: "application/json",
            data: {
                bookname: bookname,
                authorname: authorname,
                isbn: isbn,
                price: price,
                username: username,
                userid: userid,
                image: image
            },
            success: function (data) {
                alert(data.message)
            }
        })
    })
    $.ajax({
        url:'/customer',
        type: 'get',
        data:{
            isbn: '{{book[2]}}'
        },
        success: function(data){
            let count = parseInt(data.rat);
            document.getElementById('total').textContent= count
            let avg = document.getElementById('avg');
            for (let i = 1; i <=5;i++){
                let span= document.createElement('span');
                span.classList.add('p-1')
                if( i<= count){
                    span.innerHTML=`<i class="bi bi-star-fill text-success"></i> `
                }
                else{
                    span.innerHTML=`<i class="bi bi-star-fill"></i> `
                }
                avg.appendChild(span)
            }
            
        }
    })
})