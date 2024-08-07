<script>
    import { goto } from '$app/navigation';
    import { onMount } from 'svelte';
    import { writable } from 'svelte/store';
    import Cookies from 'js-cookie';

    let title = '';
    let category = '';
    let content = '';
    let description = '';
    let categories = writable([]);
    let error = writable('');

    onMount(async () => {
        try {
            const url = 'http://127.0.0.1:8000/api/categories/';
            const response = await fetch(url, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                },
                credentials: 'include'
            });
            const data = await response.json();
            if (response.ok) {
                categories.set(data);
            } else {
                console.error('Categories could not loaded');
            }

        } catch (err) {
            console.error('An error happened:', err);
        }
    });

    async function submit(event) {
        event.preventDefault();
        error.set('');
        try {
            const url = 'http://127.0.0.1:8000/api/add_post/';
            const accessToken = Cookies.get('accessToken');
            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${accessToken}`
                },
                body: JSON.stringify({title, description, content, category }),
                credentials: 'include'
            });
            const data = await response.json();
            if (response.ok) {
                goto('/');
            } else {
                error.set(data.message || 'There was an error creating the post')
            }
        } catch (err) {
            error.set(data.message || 'Error');
        }
    }
</script>

<h2 class="text-4xl font-bold mb-6 mt-4 text-center">Add New Post</h2>

<form on:submit={submit} class="max-w-md mx-auto bg-white p-6 shaddow-lg">
    <div class="mb-5">
        <label class="block text-gray-700 font-bold text-sm" for="title">Title</label>
        <input id="title" type="text" bind:value={title} required class="shadow appearance-none w-full py-3 px-3 leading-tight rounded focus:shadow-outline"/>
    </div>
    <div class="mb-5">
        <label class="block text-gray-700 font-bold text-sm" for="description">Description of Post</label>
        <input id="description" type="text" bind:value={description} required class="shadow appearance-none w-full py-3 px-4 leading-tight rounded focus:shadow-outline"/>
    </div>
    <div class="mb-6">
        <label class="block text-gray-700 font-bold text-sm" for="content">Content</label>
        <textarea id="content" type="text" bind:value={content} required class="shadow appearance-none w-full py-3 px-3 leading-tight rounded focus:shadow-outline"></textarea>
    </div>
    <div class="mb-6">
        <label class="block text-gray-700 font-bold text-sm" for="category">Category</label>
        <select id="category" bind:value={category} required class="shadow appearance-none w-full py-3 px-3 leading-right rounded focus:shadow-outline">
            <option value="" disabled>Select a category</option>
            {#each $categories as cat}
                <option value={cat.id}>{cat.name}</option>
            {/each}
        </select>
    </div>
    <div class="fkex items-center justify-between">
        <button type="submit" class="bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline">Submit</button>
    </div>
    {#if $error}
        <p class="text-red-500 mt-3">{$error}</p>
    {/if}
</form>