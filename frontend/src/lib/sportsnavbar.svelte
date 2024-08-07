<script>
    import { goto } from '$app/navigation';
    export let sports = [];

    function handleNavigation(event, path) {
        event.preventDefault();
        goto(path);
    }
</script>

<style>
    .nav-bar {
        display: flex;
        background-color: #7d99d3;
        padding: 20px;
               
        
    }
    .nav-item {
        margin-right: 20px;
        list-style: none;
        position: relative;
        padding: 0 20px;
    }
    .nav-item:last-child::after{
        content:"";
        border: 1px solid white;
        border-width: 1px 1px 0 0;
        position: absolute;
        right: -10px;
        top: -100%;
        height: 284%
    }

    .nav-item::after {
        content: "";
        border: 1px solid white;
        border-width: 1px 1px 0 0;
        position: absolute;
        right: -10px;
        top: -100%;
        height: 284%
    }
    .nav-item button {
        text-decoration: none;
        color: black;
        font-weight: bold;
        cursor: pointer;
        background-color: #7d99d3;
        border: none;
        transition: background-color 0.3s ease;
        
    }
    .nav-item button:hover {
        color: rgb(201, 222, 226);
        transition: color 0.3s;
        transform: scale(1.05);
    }
</style>

<ul class="nav-bar">
    {#each sports as sport}
    <li class="nav-item">
        
        <button on:click="{(event) => handleNavigation(event, '/' + sport.id)}">{sport.name}</button>
    </li>
    {/each}
</ul>