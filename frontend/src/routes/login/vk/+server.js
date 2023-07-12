import { redirect } from '@sveltejs/kit';

const vkAuthURL = 'https://oauth.vk.com/authorize';
const clientId = import.meta.env.VITE_VK_CLIENT_ID;
const host = import.meta.env.VITE_HOST;
const redirectUri = `${host}/callback`;

export async function GET(req) {
	const sessionId = '1234';
	const location = `${vkAuthURL}?client_id=${clientId}&state=${sessionId}&display=popup&redirect_uri=${redirectUri}&scope=email&response_type=code`;

	throw redirect(302, location);
}
