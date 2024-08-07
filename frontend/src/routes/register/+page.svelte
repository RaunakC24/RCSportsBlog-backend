<script>
    import { writable } from "svelte/store";
    import { goto } from '$app/navigation';
    import { isAuthenticated, user } from "../../stores/auth";
    import Cookies from 'js-cookie';

    let username = '';
    let password = '';
    let email = '';
    let error = writable('');

    async function register (event) {
        event.preventDefault();
        error.set('');
        try {
            const response = await fetch('/api/register', {
                method: 'POST', 
                headers: {
                    'Content-Type': 'application/json', 
                },
                body: JSON.stringify({ email, username, password }),
            });
            const data = await response.json();
            if (response.ok) {
                goto('/login');
            } else {
                error.set(data.message || 'Registration Failed');
            }
        } catch (error) {
            error.set('An error occured');
        }
    }
</script>

<h2 class="font-bold text-4xl text-center mb-6 mt-4">Register</h2>

<form on:submit={register} class = "max-w-md mx-auto bg-white p-6 shadow-lg">  
    <div class="mb-5">
        <label class="block text-grey-700 text-sm font-bold" for="email">Email</label>
        <input id="email" type="text" bind:value={email} required class="shadow appearance-none w-full py-3 px-3 leading-tight rounded focus:shadow-outline"/>
    </div>
    <div class="mb-5">
        <label class="block text-grey-700 text-sm font-bold" for="username">Enter a username</label>
        <input id="username" type="text" bind:value={username} required class="shadow appearance-none w-full py-3 px-3 leading-tight rounded focus:shadow-outline focus:outline-none"/>
    </div>
    <div class="mb-5">
        <label class="block text-grey-700 text-sm font-bold" for="password">Password</label>
        <input id="password" type="text" bind:value={password} required class="shadow appearance-none w-full py-3 px-3 rounded leading-tight focus:shadow-outline focus:outline-none"/>
    </div>
    <div class="flex item-center justify-between">
        <button type="submit" class="bg-blue-500 hover:bg-blue-600 text-white font-bold rounded py-2 px-4 focus:outline-none focus:shadow-outline">Submit</button>
    </div>
</form>