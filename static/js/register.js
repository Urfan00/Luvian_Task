function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');

const registerForm = document.getElementById('register-form');

registerForm.addEventListener('submit', function (event) {
    event.preventDefault();

    const first_name = document.getElementById('first_name').value;
    const last_name = document.getElementById('last_name').value;
    const email = document.getElementById('email').value;
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const password_confirm = document.getElementById('password_confirm').value;

    const data = {
        first_name: first_name,
        last_name: last_name,
        email: email,
        username: username,
        password: password,
        password_confirm: password_confirm
    };

    fetch('/accounts-api/register/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify(data)
    })
        .then(response => response.json())
        .then(data => {
            if (!data.error) {
                if (data.email && data.email[0] === 'MyUser with this email already exists.') {
                    showError('This E-mail address already exists');
                } else if (data.username && data.username[0] === 'MyUser with this username already exists.') {
                    showError('This username already exists');
                } else {
                    // Redirect the user to the login
                    window.location.href = '/login/';
                }
            }else{
                for (let err in data) {
                    showError(data[err][0])
                }
            }
        })
});

function showError(message) {
    document.getElementById('error_message').classList.remove('d-none')
    document.getElementById('error_message').innerHTML += `<p class="alert alert-danger rounded-pill">${message}</p>`
    document.getElementById("register-form").reset()
    setTimeout(() => {
        document.getElementById('error_message').classList.add('d-none')
    }, 3000);
}