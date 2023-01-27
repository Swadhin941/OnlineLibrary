document.getElementById('loginForm').addEventListener('submit', function (e) { 
    e.preventDefault();
    const email = e.target.email.value;
    const password = e.target.password.value;
    if (password.length < 6) {
        alert("Please Enter a password with at least 6 characters");
        return;
    }
    $.ajax({
        url: '/login',
        method: 'get',
        data: {
            email: email,
            password: password
        },
        success: function (data) {
            if (data.status === 201) {
                window.location.href = "/allBook";
            }
            else {
                alert("Wrong password");
            }
        }
    })

})