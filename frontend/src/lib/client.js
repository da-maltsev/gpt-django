function getHeaders(token = '') {
	return token.length > 5
		? {
				'Content-Type': 'application/json',
				Authorization: `Token ${token}`
		  }
		: {
				'Content-Type': 'application/json'
		  };
}

export async function post(url, body, token = '') {
	const headers = getHeaders(token);
	return await fetch(url, {
		method: 'POST',
		headers: headers,
		body: JSON.stringify(body)
	});
}

export async function get(url, token = '') {
	const headers = getHeaders(token);
	return await fetch(url, {
		method: 'GET',
		headers: headers
	});
}
