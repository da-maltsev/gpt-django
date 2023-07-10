import { get as getFromStore } from 'svelte/store';
import { tokenStore } from './tokenStore.js';

let token;
tokenStore.subscribe(($tokenStore) => (token = $tokenStore));
console.log('TOKEN SUBSCRIBE  ' + token);

let headers =
	token.length > 5
		? {
				'Content-Type': 'application/json',
				Authorization: `Token ${token}`
		  }
		: {
				'Content-Type': 'application/json'
		  };

console.log(headers);

export async function post(url, body) {
	console.log('SDASDASDASDASD');
	console.log(headers);
	return await fetch(url, {
		method: 'POST',
		headers: headers,
		body: JSON.stringify(body)
	});
}

export async function get(url) {
	return await fetch(url, {
		method: 'GET',
		headers: headers
	});
}
