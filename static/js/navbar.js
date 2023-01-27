
document.getElementById('logoutLink').addEventListener('click', function (e) {
    const location = window.location.pathname;
    $.ajax({
        url: '/logout',
        type: 'get',
        data: {
            location : location,
        },
        success: function (data) {
            window.location.href = data.location;
        }
    })
})
let show = false;
document.getElementById('profileClick').addEventListener('click', function () {
    if (!show) {
        document.getElementById('profile').classList.remove('d-none');
        show = true;
    }
    else {
        document.getElementById('profile').classList.add('d-none');
        show = false;
    }
})