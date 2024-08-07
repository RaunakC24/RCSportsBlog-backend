import { json } from "@sveltejs/kit";

export const POST = async ({ request }) => {
    try {
        const { username, password } = await request.json();

        const response = await fetch('http://127.0.0.1:8000/api/login/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json'},
            body: JSON.stringify({ username, password }),
            credentials: 'include',
        });

        if (response.ok) {
            const data = await response.json();
            return json(data);
        } else {
            const error = await response.json();
            return json(error, {status: response.status });
        }
    } catch (error) {
        return json({ message: 'An error occured' }, {status: 500});
    }
}
