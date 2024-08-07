/** @type {import('./$types').PageLoad} */
export async function load({ fetch, params }) {
    try {
        const response = await fetch(`http://127.0.0.1:8000/api/post/${params.id}/`);
        const data = await response.json();
        if (response.ok) {
            console.log('Data fetched successfully:', data);
            return {
                props: {
                    post: data.post,
                    comments: data.comments,
                    commentForm: data.comment_form,
                    replyForm: data.reply_form,
                    error: null
                }
            };
        } else {
            console.error('Failed to fetch post:', response.status);
            return {
                status: response.status,
                props: {
                    error: 'Could not load the post'
                }
            };
        }
    } catch (err) {
        console.error('Error fetching post:', err);
        return {
            status: err.status || 500,
            props: {
                error: 'An error occurred'
            }
        };
    }
}