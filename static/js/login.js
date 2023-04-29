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

let login_form = document.getElementById("login-form")

login_form.addEventListener('submit', (e) => {
    e.preventDefault()

    const username = document.querySelector('#username').value;
    const password = document.querySelector('#password').value;
    const data = {
        username: username,
        password: password
    };
    fetch('/accounts-api/login/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
            'Authorization': `Bearer ${localStorage.getItem("access_token")}`
        },
        body: JSON.stringify(data)
    })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                showError(data.error)
            }
            // Get the access and refresh tokens from the response
            const access_token = data.tokens.access;
            const refresh_token = data.tokens.refresh;

            // Store the tokens in local storage or cookies for later use
            localStorage.setItem('user-detail', JSON.stringify(data))
            localStorage.setItem('username', data.username);
            localStorage.setItem('access_token', access_token);
            localStorage.setItem('refresh_token', refresh_token);

            // Redirect the user to the homepage
            window.location.href = 'http://localhost:8000/';

        })
});

function showError(message) {
    document.getElementById('error_message').classList.remove('d-none')
    document.getElementById('error_message').textContent = message
    document.getElementById("login-form").reset()
    setTimeout(() => {
        document.getElementById('error_message').classList.add('d-none')
    }, 1000);
}