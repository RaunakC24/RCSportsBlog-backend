import { json } from "@sveltejs/kit";
import Cookies from 'js-cookie';

export async function POST ({ request }) {
    try {
        const { title, description, content, category } = await response.json();

        const accessToken = Cookies.get('accessToken');
        const response = await fetch('http://127.0.0.1:8000/api/add_post/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${accessToken}`
            },
            body: JSON.stringify({ title, description, content, category})
        });
        if (response.ok) {
            const data = await response.json()
            return json(data);
        } else {
            const error = await response.json();
            return json(error, {status: response.status});
        }
    } catch (error) {
        return json({ message: 'An error occured'});
    }
}