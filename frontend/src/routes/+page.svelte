<script>
    import { writable } from 'svelte/store';
    import {category} from '../sport-store'
    import { isAuthenticated, user } from "../stores/auth";
    import  Cookies from 'js-cookie';
    import { onMount } from 'svelte';
    import { tokenRefresh } from '../lib/api';
    
    

    let sports = []

    category.subscribe(values => sports = values)

    let featuredPost = writable();

    function getFeaturedPost() {
        const storedPost = sessionStorage.getItem('featuredPost');
        if (storedPost) {
            featuredPost.set(JSON.parse(storedPost));
        } else {
            randomPost();
        }
    }

    async function randomPost() {
        const accessToken = Cookies.get('accessToken');
        const url = 'http://127.0.0.1:8000/api/random_post/';
        const options = {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${accessToken}`
            }
        };
        try {
            const response = await tokenRefresh(url, options);
            if(response.ok) {
                const data = await response.json();
                featuredPost.set(data);
                sessionStorage.setItem('featuredPost', JSON.stringify(data));
            } else {
                console.error('Failed to fetch the random post');
                featuredPost.set(null);
            }
        } catch (error) {
            console.error(error.message);
            featuredPost.set(null);
        }
        
    }

    onMount(() => {
        if ($isAuthenticated) {
            getFeaturedPost();
        }  
    })

</script>

<div class="bg-gradient-to-r from-indigo-300 via-sky-300 via-40% to-indigo-300 rounded-sm shadow-lg p-12 mb-6 mt-10 min-h-[400px] flex flex-col text-center items-center justify-center">
    <h2 class="text-4xl font-bold mb-4 mb-4">Welcome to Raunak's Sports Blog</h2>
    <p class="text-lg">Once authenticating, a featured post will display on the home page, and you
                       will be able to add comments and reply to comments.
    </p>
    <p class="text-lg mt-2">If you are not authenticated, you will still be able to view posts and comments, however you won't be able to post anything.</p>
</div>

<div class="mx-auto p-4 container max-w-2xl text-center">
    {#if $isAuthenticated}
        {#if $featuredPost}
            <div class="bg-gradient-to-r from-indigo-200 via-sky-300 via-40% to-indigo-300 rounded-lg p-6 mb-6 shadow-xl">
                <h2 class="font-bold text-2xl mb-4">Featured Post: {$featuredPost.title}</h2>
                <p class="text-gray-700 mb-4">{$featuredPost.description}</p>
                <a href="{$featuredPost.link}" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-1 px-2 rounded inline-block">Read More</a>
            </div>
        {:else}
            <p class="text-center text-gray-500 text-md">Loading Featured Post</p>
        {/if}
    {/if}

</div>


