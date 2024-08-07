import { json } from '@sveltejs/kit';

export const POST = async ({ request }) => {
    try {
        const response = await fetch('http://127.0.0.1:8000/api/logout/', {
            method: 'POST',
            credentials: 'include'
        });

        if (response.ok) {
            return new Response(null, {
                status: 200,
                headers: {
                    'Content-Type': 'application/json'
                }
            });
        } else {
            const error = await response.json();
            return json(error, { status:response.status });
        }
    } catch (error) {
        return json({ message: 'An error occured' }, { status: 500});
    }
}