// Login functionality

document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');

    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            
            // get form values
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;

            // call login function
            await loginUser(email, password)
        });
    }
});

async function loginUser(email, password) {
  try {
        const response = await fetch('http://127.0.0.1:5000/api/v1/auth/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email, password })
    });
    
    // Handle the response
    if (response.ok) {
      const data = await response.json();

      // save JWT token in cookie
      document.cookie = `token=${data.access_token}; path=/`;

      // redirect to home/index page
      window.location.href = 'http://127.0.0.1:5000/';
    } else {
        alert('Login failed: ' + response.statusText);
    }
  } catch (error) {
    alert('Login failed: Could not connect to server')
  }
} 
