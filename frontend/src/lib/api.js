import Cookies from 'js-cookie';

export async function tokenRefresh(url, options) {
    const response = await fetch(url, options);

    if (response.status === 401) {
        const refreshToken = Cookies.get('refreshToken');
        const refeshurl = 'http://127.0.0.1:8000/api/token/refresh/'
        const refreshResponse = await fetch(refeshurl, {
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