<script>
    import { onMount } from 'svelte';
    import { writable } from 'svelte/store';
    import Cookies from 'js-cookie';
    import { goto } from '$app/navigation';
    import { isAuthenticated, isSuperuser, user } from '../stores/auth'

    let mainTitle = "Raunak's Sports Blog";

    async function handleLogout() {
        const response = await fetch ('/api/logout', {
            method: 'POST',
            credentials: 'include'
        });
        if (response.ok) {
            user.set(null);
        isAuthenticated.set(false);
        Cookies.remove('accessToken');
        Cookies.remove('refreshToken');
        Cookies.remove('username');
        Cookies.remove('is_superuser');
        Cookies.remove('userId');
        sessionStorage.removeItem('featuredPost');
        goto('/');
        } else {
            console.error('Logout not successful');
        }
    }

    function addPost () {
        goto('/add-post');
    }

    function handleHomeNavigation () {
        goto('/');
    }

    onMount(() => {
        console.log("Checking authentication status...");
        try {
            const accessToken = Cookies.get('accessToken');
            const sUser = Cookies.get('username');
            const sIsSuperuser = Cookies.get('is_superuser') === 'true';
            const userId = parseInt(Cookies.get('userId'), 10);

            if (accessToken && sUser && userId) {
                user.set({username: sUser, id: userId})
                isAuthenticated.set(true);
                isSuperuser.set(sIsSuperuser);
                console.log("User is authenticated");
            } else {
                console.log("No valid credentials found");
                user.set(null);
                isAuthenticated.set(false);
                isSuperuser.set(false);
            }
        } catch (error) {
            console.log('Error checking status: ', error);
            user.set(null);
            isAuthenticated.set(false);
            isSuperuser.set(false);
        }
    })
</script>

<nav class="nav-container">
    <h1>
        <button class="logo-button" on:click={handleHomeNavigation}>{mainTitle}</button>
    </h1>
    <div class="authorization-button">
        {#if $isAuthenticated}
            <p class="">Welcome, {$user ? $user.username : 'Guest'}</p>
            {#if $isSuperuser}
                <button on:click={addPost}>Add Post</button>
            {/if}
            <button on:click={handleLogout}>Logout</button>
        {:else}
            <a href="/login">Login</a>
            <a href="/register">Register</a>
        {/if}
    </div>
</nav>




<style>
    .nav-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: linear-gradient(to right, #c6dff0, #4889e9);
        box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1);
        padding: 10px 20px;
        
    }
    
    .logo-button {
        font-size: 40px;
        color: black;
        font-family:'Lucida Sans';
        padding: 10px 20px;
        margin: 5px;
        position:relative;
        top: 5px;
        left: -5px;
        border-radius: 5px;
        font-style: italic;
        text-decoration: none;
        transition: color 0.3s ease, transform 0.3s ease;
        }

    .logo-button:hover {
        color: rgb(51, 139, 240);
        transform: scale(1.02);
    }
    .authorization-button {
        display: flex;
        align-items: flex-start;
        gap: 25px;
    }

    .authorization-button a {
        font-size: 20px;
        color: black;
        cursor: pointer;
        background: none;
        border: none;
        text-decoration: none;
    }
    
    .authorization-button a:hover, .authorization-button button:hover {
        background-color: #e0e4e8;
    }
</style>