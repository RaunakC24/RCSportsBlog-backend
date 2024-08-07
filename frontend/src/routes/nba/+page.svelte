<script>    

    import { onMount } from "svelte";
    import Sportpage from "../../lib/sportpage.svelte";

    export let nbaArticles = [];

    onMount(async () => {
        try {
            const url = 'http://127.0.0.1:8000/api/category/2';
            const response = await fetch(url);
            const data = await response.json();
            nbaArticles = data.posts;
        } catch (error) {
            console.error('Error fetching the posts: ', error);
        }
    });
</script>

<h2 class="text-center py-3 text-2xl font-bold shadow-sm mx-auto w-full">NBA Posts</h2>
<Sportpage sportsarticles={nbaArticles}></Sportpage>


