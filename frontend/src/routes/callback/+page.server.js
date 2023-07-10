import { redirect } from '@sveltejs/kit';

const tokenURL = 'https://oauth.vk.com/access_token';

const hostDev = 'http://app:8000';
const getApiTokenFromVk = `${hostDev}/api/v1/auth/vk-oauth2/`;

const host = import.meta.env.VITE_HOST;
// const getApiTokenFromVk = `${host}/api/v1/auth/vk-oauth2/`;
const redirectUri = `${host}/callback`;
const clientId = import.meta.env.VITE_VK_CLIENT_ID;
const secret = import.meta.env.VITE_VK_SECRET;

export async function load({ params, url, cookies }) {
	const code = url.searchParams.get('code');
	const accessToken = await getAccessToken(code);
	const apiToken = await getUser(accessToken);

	cookies.set('token', apiToken.token, {
		httpOnly: false,
		sameSite: 'strict',
		secure: false,
		path: '/',
		maxAge: 60 * 60 * 24 * 7
	});
}

function getAccessToken(code) {
	const url = `${tokenURL}?client_id=${clientId}&client_secret=${secret}&redirect_uri=${redirectUri}&code=${code}`;
	return fetch(url)
		.then((r) => r.json())
		.then((r) => r.access_token);
}

function getUser(accessToken) {
	return fetch(getApiTokenFromVk, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json'
		},
		body: JSON.stringify({
			accessToken: accessToken
		})
	}).then((r) => r.json());
}
