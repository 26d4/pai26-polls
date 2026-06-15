import { getCSRFHeader, SHARED_FETCH_OPT } from "./shared"

export async function login(username:string, password:string) {
	const response = await fetch(
		'http://localhost:8000/api/login/',
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
		'http://localhost:8000/api/logout/',
		{
			method: 'POST',
			...SHARED_FETCH_OPT,
			headers: getCSRFHeader()
		}
	)

	return response.json()
}