$(document).ready(function () {
    $.ajax({
        url: '/blog',
        type: 'get',
        success: function (data) {
            console.log(data);
            let blog= document.getElementById('blogCard')
            for (let i = 0; i < data.blogId.length; i++){
                let div = document.createElement('div')
                div.classList.add('col-12');
                div.classList.add('col-sm-12');
                div.classList.add('col-md-12');
                div.classList.add('col-lg-12');
                div.innerHTML = `
                <div class="card">
                <div class="card-body">
                    <h5 class="card-title">
                        ${data.blogTitle[i]}
                    </h5>
                    <div class="card-text">${data.blogContent[i].slice(0,350)}...</div>
                </div>
                <div class="">
                <a href="#" class=""><button class="btn btn-success ms-3">Details</button></a>
                </div>
            </div>  
                `
                blog.appendChild(div);
            }
        }
    })
})