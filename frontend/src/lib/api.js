import Cookies from 'js-cookie';

export async function tokenRefresh(url, options) {
    let response = await fetch(url, options);

    if (response.status === 401) {
        const refreshToken = Cookies.get('refreshToken');
        const refeshUrl = 'http://127.0.0.1:8000/api/token/refresh/'
        const refreshResponse = await fetch(refeshUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ refresh: refreshToken})
        });
        
        if (refreshResponse.ok) {
            const { access } = await refreshResponse.json();
            Cookies.set('accessToken', access);
            options.headers['Authorization'] = `Bearer ${access}`;
            response = await fetch(url, options);
        } else {
            console.error('Token refresh could not happen');
        }
    }
    return response;
}   

export async function fetchAuth(url, method = 'GET', body = null) {
    const accessToken = Cookies.get('accessToken');
    const options = {
        method: method,
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${accessToken}`
        },
        body: JSON.stringify(body) 
    };
    return tokenRefresh(url, options);
}