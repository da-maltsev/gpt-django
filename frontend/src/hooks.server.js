function redirect(location, body) {
	return new Response(body, {
		status: 303,
		headers: { location }
	});
}

const unProtectedRoutes = ['/', '/login/vk', '/about', '/callback', '/auth'];

export const handle = async ({ event, resolve }) => {
	const token = event.cookies.get('token');
	if (!token && !unProtectedRoutes.includes(event.url.pathname))
		return redirect('/auth', 'No authenticated user.');

	if (token) {
		event.locals.user = {
			isAuthenticated: true,
			token: token
		};
	} else {
		event.locals.user = {
			isAuthenticated: false,
			token: ''
		};
		if (!unProtectedRoutes.includes(event.url.pathname)) return redirect('/', 'Not a valid user');
	}

	return resolve(event);
};
