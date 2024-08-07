<script>
    
    import { writable } from "svelte/store";
    import { goto } from '$app/navigation';
    import { isAuthenticated, user, isSuperuser } from "../../stores/auth";
    import Cookies from 'js-cookie';
    

    let username = '';
    let password = '';
    let error = writable('');

    async function handleLogin(event) {
        event.preventDefault();
        error.set('');
        try {
            const response = await fetch('/api/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ username, password }),
                credentials: 'include'
            });
            const data = await response.json();
            if (response.ok) {
                console.log('User data from server:', data.user);
                user.set(data.user);
                isAuthenticated.set(true);
                isSuperuser.set(data.is_superuser);
                Cookies.set('accessToken', data.access, {secure: true});
                Cookies.set('refreshToken', data.refresh, {secure: true});
                Cookies.set('username', data.user.username, {secure: true});
                Cookies.set('userId', data.user.id, {secure: true});
                Cookies.set('is_superuser', data.is_superuser, {secure: true});
                goto('/');
            } else {
                error.set(data.message || 'Incorrect username or password');
            }
            
        } catch (err) {
            error.set('An error occured');
        }
    }

    function checkAuth() {
        const accessToken = Cookies.get('accessToken');
        const name = Cookies.get('username');
        const isSuper = Cookies.get('is_superuser') === 'true';
        const userId = Cookies.get('userId');
        if (accessToken && name) {
            user.set({username: name, id: parseInt(userId, 10) });
            isAuthenticated.set(true);
            isSuperuser.set(isSuper);
        } else {
            isAuthenticated.set(false);
            user.set(null);
            isSuperuser.set(false);
        }
    }
    checkAuth();
</script>

<h2 class="text-4xl font-bold mb-6 mt-4 text-center">Login</h2>

<form on:submit={handleLogin} class="max-w-md mx-auto bg-white p-6 shadow-lg">
    <div class="mb-5">
        <label class="block text-gray-700 text-sm font-bold" for="username">Username</label>
        <input id="username" type="text" bind:value={username} required class="shadow appearance-none w-full py-3 px-3 rounded leading-tight focus:outline-none focus:shadow-outline"/>
    </div>
    <div class="mb-6">
        <label class="block text-gray-700 text-sm font-bold" for="password">Password</label>
        <input id="password" type="text" bind:value={password} required class="shadow appearance-none w-full py-3 px-3 rounded leading-tight focus:outline-none focus:shadow-outline"/>
    </div>
    <div class="flex items-center justify-between">
        <button type="submit" class="bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline">Login</button>
    </div>
    {#if $error}
        <p class="text-red-500">{$error}</p>
    {/if}
</form>