export interface User {
	id: number,
	username: string,
	email: string,
	first_name: string | undefined,
	last_name: string | undefined,
	date_joined: Date,
	is_authenticated: boolean
	// ('id', 'username', 'email', 'first_name', 'last_name', 'date_joined', 'is_authenticated')
}