
// Generic API call function
async function apiCall(endpoint, method = 'POST', data = {}, headers = {'Content-Type': 'application/json'}) {
    try {
        const response = await fetch(endpoint, {
            method,
            headers,
            body: method === 'GET' ? undefined : JSON.stringify(data)
        });
        let result;
        try {
            result = await response.json();
        } catch (e) {
            result = {};
        }
        return { ok: response.ok, status: response.status, data: result };
    } catch (error) {
        return { ok: false, status: 0, data: { error: 'Network error: ' + error } };
    }
}

async function isLoggedIn() {
    const response = await fetch('/api/check_user', {
        method: 'GET',
        credentials: 'include' // Include cookies in the request
    });
    if (response.ok) {
        console.log('User is logged in');
        window.location.href = '/store';
    } else {
        window.location.href = '/login';
    }
    
}

// Example usage:
// apiCall('/api/login', 'POST', { user_hash: '...', b64enc_img: '...' })
//   .then(res => {
//     if (res.ok && res.data.success) { /* handle success */ }
//     else { /* handle error */ }
//   });
