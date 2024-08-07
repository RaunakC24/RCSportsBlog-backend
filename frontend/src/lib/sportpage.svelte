<script>
    export let sportsarticles = [];

</script>


<div class="article-container">
    {#each sportsarticles as articles}
    <div class="article-card">
        <h3>{articles.title}</h3>
        <p>{articles.description}</p>
        <a href={`/post/${articles.id}`}>Read More</a>
    </div>
    {/each}
</div>
<style>
.article-container {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        padding: 20px;
    }
    .article-card {
        border: 1px solid #ddd;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        border-radius: 5px;
        padding: 20px;
        margin: 10px; 
        width: calc(30% - 40px);
        background-color: #fff;
    }
    .article-card h3 {
        font-size: 20px;
        margin-bottom: 10px;
    }
    .article-card p {
        font-size: 14px;
        color: #555;
        margin-bottom: 10px;
    }
    .article-card a {
        text-decoration: none;
        color: #3b5998;
        font-weight: bold;
        border: 1px solid #3b5998;
        border-radius: 5px;
        padding: 10px 20px;
        display: inline-block;
        transition: background-color 0.3s, color 0.3s;

    }
    .article-card a:hover {
        background-color: #3b5998;
        color: white;
    }
    @media (max-width: 1024px) {
        .article-card {
            width: calc(50% - 30px);
        }
    }
    @media (max-width: 768px) {
        .article-card {
            width: calc(50% - 30px);
        }
    }
    @media (max-width: 480px) {
        .article-card {
            width: calc(100% - 40px);
        }
    }

</style>