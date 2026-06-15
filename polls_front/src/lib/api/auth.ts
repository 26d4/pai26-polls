import { getCSRFHeader, SHARED_FETCH_OPT, API_URL_BASE, getCurrentUser } from "./shared"

export async function login(username:string, password:string) {
	const response = await fetch(
		API_URL_BASE + 'login/',
		{
			method: 'POST',
			body: JSON.stringify({username, password}),
			headers: {
				'Content-Type': 'application/json',
				...getCSRFHeader()
			},
			...SHARED_FETCH_OPT
		}
	)

	return response.json()
}

export async function logout() {
	const response =  await fetch(
		API_URL_BASE + 'logout/',
		{
			method: 'POST',
			...SHARED_FETCH_OPT,
			headers: getCSRFHeader()
		}
	)

	return response.json()
}