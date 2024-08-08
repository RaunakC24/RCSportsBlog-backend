<script>

    import { onMount } from 'svelte';
    import {category} from '../../sport-store'
    import Sportpage from '../../lib/sportpage.svelte';

    let sports = []

    category.subscribe(values => sports = values)

    export let nflArticles = [];

    onMount(async () => {
        try {
            const url = 'http://127.0.0.1:8000/api/category/1';
            const response = await fetch(url);
            const data = await response.json();
            nflArticles = data.posts;
        } catch (error) {
            console.error('Error fetching NFL Articles:', error);
        }
    });

</script>

<h2 class="bg-gradient-to-r from-blue-200 via-blue-300 via-40% to-blue-200 text-center py-3 mt-5 text-2xl font-bold shadow-sm mx-auto max-w-sm">NFL Posts</h2>
<Sportpage sportsarticles={nflArticles}></Sportpage>

<style>
    :global(body) {
        background-color: #f0f4f8;
        color: #333;
    }
</style>

