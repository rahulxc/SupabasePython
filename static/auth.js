
async function handleSignIn(e) {
    e.preventDefault();
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    
    try {
        const response = await fetch('/login', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({email, password})
        });
        const data = await response.json();
        if (response.ok) {
            localStorage.setItem('userEmail', email);
            localStorage.setItem('access_token', data.session.access_token);
            window.location.href = '/dashboard';
        } else {
            alert(data.error);
        }
    } catch (error) {
        alert('Error signing in');
    }
}

async function handleSignUp(e) {
    e.preventDefault();
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    
    try {
        const response = await fetch('/signup', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({email, password})
        });
        const data = await response.json();
        if (response.ok) {
            alert('Signup successful! Please sign in.');
            window.location.href = '/signin';
        } else {
            alert(data.error);
        }
    } catch (error) {
        alert('Error signing up');
    }
}

async function handleLogout() {
    try {
        const response = await fetch('/logout', {
            method: 'POST'
        });
        if (response.ok) {
            localStorage.removeItem('userEmail');
            window.location.href = '/';
        }
    } catch (error) {
        alert('Error logging out');
    }
}
