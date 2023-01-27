
let handleClick = (isbn) => {
    $.ajax({
        url: "/selectedbook",
        type: 'get',
        data: {
            isbn: isbn
        },
        success: function (data) {
            location.href = "{{url_for('bookdetails')}}"
        }
    })
}
let id = document.getElementById('topBook')
$.ajax({
    url: '/topBook',
    type: 'get',
    success: function (data) {
        for (let i = 0; i < data.books.length; i++) {
            let div = document.createElement('div')
            div.classList.add('col-12')
            div.classList.add('col-sm-6')
            div.classList.add('col-md-3')
            div.classList.add('col-lg-4')
            div.innerHTML = `
        <div class ="card bookCard shadow-lg">
            <div class="row">
                <div class="col-4 col-sm-4 col-md-4 col-lg-4">
                    <img
                    class="card-img-top" src= ${data.image[i]}
                    alt="" style="height: 200px;width: 100%;"/>
                </div>
                <div class="col-8 col-sm-8 col-md-8 col-lg-8">
                    <div class="card-body">
                    <div class="card-title fw-bold">${data.books[i]}</div>
                    <div class="card-text">ISBN: ${data.isbn[i]}</div>
                    </div>
                </div>
            </div>
                <div class="card-footer">
                    <div class="d-flex justify-content-between">
                        <span class="bg-success text-white p-2 border rounded">Price: ${data.price[i]}</span>
                        <a onclick="handleClick('${data.isbn[i]}')"  class="btn btn-warning" id="btn-search">Details</a>
                    </div>
                </div>
        
        </div>
      
      `
            id.appendChild(div)
        }
    }
})

// let handleReco = false;
// document.getElementById('handleRecommend').addEventListener('click', function () {
//     if (!handleReco) {
//         document.getElementById('recommending').classList.remove('d-none');
//         document.getElementById('handleRecommend').classList.add('d-none');
//         handleReco = true;
//     }
// })
// if (handleReco) {
    let id2 = document.getElementById("recommend")
    let id3 = document.getElementById("recommendedbook")
      $.ajax({
        url: '/recommend',
        type: 'get',
        data: {

        },
        success: function (data) {
          console.log(data)
          if (data.len < 3) {
            id2.classList.add('hidden')
          }
          else {
            id2.classList.remove('hidden')
            for (let i = 0; i < data.books.length; i++) {
                let div = document.createElement('div')
                div.classList.add('col-12')
                div.classList.add('col-sm-6')
                div.classList.add('col-md-3')
                div.classList.add('col-lg-4')
                div.innerHTML = `
              <div class ="card bookCard shadow-lg">
                  <div class="row">
                      <div class="col-4 col-sm-4 col-md-4 col-lg-4">
                          <img
                          class="card-img-top" src= ${data.image[i]}
                          alt="" style="height: 200px;width: 100%;"/>
                      </div>
                      <div class="col-8 col-sm-8 col-md-8 col-lg-8">
                          <div class="card-body">
                          <div class="card-title fw-bold">${data.books[i]}</div>
                          <div class="card-text">ISBN: ${data.isbn[i]}</div>
                          </div>
                      </div>
                  </div>
                      <div class="card-footer">
                          <div class="d-flex justify-content-between">
                              <span class="bg-success text-white p-2 border rounded">Price: ${data.price[i]}</span>
                              <a onclick="handleClick('${data.isbn[i]}')"  class="btn btn-warning" id="btn-search">Details</a>
                          </div>
                      </div>
              
              </div>
            
            `
              id3.appendChild(div)
            }
          }
        }
      })
