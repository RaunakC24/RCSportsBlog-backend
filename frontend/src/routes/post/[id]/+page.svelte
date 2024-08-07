<script>
    export let data;

    import { onMount } from 'svelte';
    import { writable } from 'svelte/store';
    import Cookies from 'js-cookie';
    import { isAuthenticated, user } from "../../../stores/auth";
    

    let post = writable(null);
    let comments = writable(null);
    let commentForm = writable(null);
    let replyForm = writable(null);
    let newComment = '';

    onMount(() => {
        post.set(data.props.post);
        let enhanceComment = data.props.comments.map(comment => ({
            ...comment, newReply: '', replying: false, likes: Number(comment.likes) || 0, dislikes: Number(comment.dislikes) || 0,
            replies: comment.replies ? comment.replies.map(reply => ({
                ...reply, 
                likes: Number(reply.likes) || 0,
                dislikes: Number(reply.dislikes) || 0
            })) : []
        }));
        comments.set(enhanceComment);
        commentForm.set(data.props.commentForm);
        replyForm.set(data.props.replyForm);
    })

    function dateFormat(isoString) {
        const date = new Date(isoString);
        return date.toLocaleDateString('en-us', { day: 'numeric', month: 'long', year: 'numeric'});
    }

    async function addComment() {
        const url = 'http://127.0.0.1:8000/api/add_comment';
        const accessToken = Cookies.get('accessToken');
        const response = await fetch(`${url}/${data.props.post.id}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${accessToken}`
            },
            body: JSON.stringify({ content: newComment})
        });
        const result = await response.json();
        if (response.ok) {
            const newAddCommentData = {
                ...result.comment,
                likes: 0,
                dislikes: 0
            };
            comments.update(currentComments => [...currentComments, newAddCommentData]);
            newComment = '';
        } else {
            console.error('Comment could not be added');
        }

    }

    async function deleteComment(commentId) {
        const url = 'http://127.0.0.1:8000/api/delete_comment';
        const accessAToken = Cookies.get('accessToken');
        const response = await fetch(`${url}/${commentId}/`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${accessAToken}`
            }
        });
        if (response.ok) {
            comments.update(currentComments => currentComments.filter(comment => comment.id !== commentId));
        } else {
            const result = response.json();
            console.error('Could not delete comment', result.message);
        }

    }

    async function addReply(commentId, replyContent) {
        if (!replyContent.trim()) return;
        const url = 'http://127.0.0.1:8000/api/add_reply';
        const accessToken = Cookies.get('accessToken');
        const response = await fetch(`${url}/${commentId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${accessToken}`
            },
            body: JSON.stringify({ content: replyContent})
        });
        const result = await response.json();
        if (response.ok) {
            comments.update(allComments => {
                return allComments.map(comment => {
                    if (comment.id === commentId) {
                        const newReplyData = {
                            ...result.reply,
                            likes: 0,
                            dislikes: 0
                        };
                        comment.replies = [...comment.replies, newReplyData];
                        comment.newReply = '';
                        comment.replying = false;
                    }
                    return comment;
                });
            });
        } else {
            console.error('Could not add reply', result.errors);
        }
    }

    function replyToggle(comment) {
        comments.update(allComments => {
            return allComments.map(c => {
                if (c.id === comment.id) {
                    c.replying = !c.replying;
                } else {
                    c.replying = false;
                }
                return c;
            });
        });
    }

    async function deleteReply(replyId, commentId) {
        const url = 'http://127.0.0.1:8000/api/delete_reply';
        const accessToken = Cookies.get('accessToken');
        const response = await fetch(`${url}/${replyId}`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${accessToken}`
            }
        });
        if (response.ok) {
            comments.update(allComments => {
                return allComments.map(comment => {
                if (comment.id === commentId) {
                    comment.replies = comment.replies.filter(reply => reply.id !== replyId);
                }
                return comment;
                });      
            });
        } else { 
            console.error('Could not delete reply');
        }
    }

    async function likeDislikeSwitch(type, id, isLike) {
        const accessToken = Cookies.get('accessToken');
        const endpoint = isLike ? `like_${type}` : `dislike_${type}`;
        const url = 'http://127.0.0.1:8000/api'
        const response = await fetch(`${url}/${endpoint}/${id}/`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${accessToken}`
            }
        });

        if (!response.ok) {
        console.error('Failed to fetch from API');
        return;
        }

        const result = await response.json();
        console.log(`API response for ${isLike ? 'like' : 'dislike'}:`, result);

        if (response.ok) {
            comments.update(allComments => {
                return allComments.map(comment => {
                if (type === 'comment' && comment.id === id) {
                    console.log('Updating likes/dislikes for comment:', comment);
                    return {...comment, likes: result.likes_count, dislikes: result.dislikes_count};
                }
                if (type === 'reply') {
                    comment.replies = comment.replies.map(reply => {
                        if (reply.id === id) {
                            console.log('Updating likes/dislikes for reply:', reply);
                            return {...reply, likes: result.likes_count, dislikes: result.dislikes_count}
                        }
                        return reply;
                    });
                }
                return comment;
                });
            })    
        } else {
            console.error('There was an error with toggling the likes and dislikes');
        }
    }

</script>
 
<div class="bg-gray-200 min-h-screen flex justify-center">
    <div class="container mx-auto p-4 bg-white rounded-lg shadow">
    <div class="p-6">
        {#if $post}
            <h1 class="text-black-800 font-bold text-3xl text-center px-3 py-2 mb-4">{$post.title}</h1>
            <div class="text-left text-xs text-gray-500">Posted on: {dateFormat($post.publish)}</div>
            <p class="text-black-700 text-xl mb-3 mt-3 py-3">{$post.content}</p>
        {:else}
            <p class="text-center">Post is loading</p>
        {/if}
        {#if $comments}
            <div class="mt-10">
                <h2 class="text-black-700 font-semibold text-lg">Comments</h2>
                <ul>
                    {#each $comments as comment}
                        <li class="border-t border-gray-400 mt-4 pt-4 shadow-inner rounded-lg px-2">
                            <p class="text-gray-800 text-md">{comment.content}</p>
                            <span class="text-gray-800 mb-2 text-sm">Posted by: {comment.user.username}</span>
                            {#if $isAuthenticated}
                                <div class="flex space-x-2 mt-2 flex-wrap items-center">
                                    <button class="bg-blue-400 hover:bg-blue-600 text-xs text-white px-2 py-1 rounded transition duration-300 ease-in-out" on:click={() => likeDislikeSwitch('comment', comment.id, true)}>Likes ({comment.likes})</button>
                                    <button class="bg-gray-400 hover:bg-gray-600 text-xs text-white px-2 py-1 rounded transition duration-300 ease-in-out" on:click={() => likeDislikeSwitch('comment', comment.id, false)}>Dislikes ({comment.dislikes})</button>
                                    <button class="bg-gray-400 hover:bg-gray-600 text-xs text-white px-2 py-1 rounded transition duration-300 ease-in-out" on:click={() => replyToggle(comment)}>{comment.replying ? 'Cancel' : 'Reply'}</button>
                                </div>
                                {#if comment.replying}
                                    <textarea class="mt-4 p-2 w-full rounded border border-gray-400" bind:value={comment.newReply}/>
                                    <button class="mt-3 bg-green-400 hover:bg-green-600 text-white px-2 py-1 text-sm rounded transition duration-300 ease-in-out" on:click={() => addReply(comment.id, comment.newReply)} >Submit</button>
                                {/if}
                            {/if}
                            {#if $isAuthenticated && $user && $user.id === comment.user.id}
                                <div class="mt-2">
                                    <button on:click={() => deleteComment(comment.id)} class="text-white mt-2 bg-red-500 text-xs px-1 py-1 hover:bg-red-700 transition duration-300 ease-in-out">Delete Comment</button>
                                </div>    
                            {/if}
                            {#if comment.replies.length > 0}
                                <ul class="pl-4 mt-2">
                                    {#each comment.replies as reply}
                                        <li class="border-t border-gray-300 mt-2 pt-2 px-2 rounded-lg">
                                            <p class="text-black-700 text-md">{reply.content}</p>
                                            <div class="text-gray-600 text-sm">Replied by: {reply.user.username}</div>
                                        </li>
                                        {#if $isAuthenticated}
                                            <button class="text-xs bg-blue-400 text-white hover:bg-blue-600 px-2 py-1 text-xs rounded transition duration-300 ease-in-out" on:click={() => likeDislikeSwitch('reply', reply.id, true)}>Likes ({reply.likes})</button>
                                            <button class="text-xs bg-gray-400 text-white hover:bg-gray-600 px-2 py-1 text-xs rounded transition duration-300 ease-in-out" on:click={() => likeDislikeSwitch('reply', reply.id, false)}>Dislikes ({reply.dislikes})</button>
                                        {/if}
                                        {#if $isAuthenticated && $user && $user.id === reply.user.id}
                                            <div class="mt-2">
                                                <button on:click={() => deleteReply(reply.id, comment.id)} class="text-white bg-red-500 hover:text-red-700 px-1 py-1 text-xs transition duration-300 ease-in-out">Delete Reply</button>
                                            </div>
                                        {/if}
                                    {/each}
                                </ul>
                            {/if}
                        </li>
                    {/each}
                </ul>
            </div>
        {/if}
        {#if $isAuthenticated}
            <div class="mt-6">
                <h3 class="font-semibold">Add Comment</h3>
                <textarea id="content" type="text" bind:value={newComment} required class="shadow appearance-none w-full py-3 px-3 leading-tight rounded border border-gray-400 focus:shadow-outline"></textarea>
                <button class="bg-indigo-500 hover:bg-indigo-700 text-white font-bold py-2 px-3 rounded focus:outline-none focus:shadow-outline transition duration-300 ease-in-out" on:click={addComment}>Submit Comment</button>
            </div>
        {/if}
    </div>
</div>
</div>
