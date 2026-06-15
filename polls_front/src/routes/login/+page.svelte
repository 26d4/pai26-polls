<script lang="ts">
	import { goto } from '$app/navigation';
	import { resolve } from '$app/paths';
	import { login } from '$lib/api/auth'

	async function handleSubmit(evt:Event) {
		evt.preventDefault()

		let target = evt.currentTarget as HTMLFormElement
		let formData = new FormData(target)

		let result = await login(
			formData.get('username')!.toString(),
			formData.get('password')!.toString()
		)

		if(result && result?.login_success) {
			goto(resolve('/'))
		}
	}
</script>

<svelte:head>
	<title>Log in</title>
</svelte:head>

<h1>Log in</h1>

<form onsubmit={handleSubmit}>
	<input id="login-form-username" name="username" type="text">
	<input id="login-form-password" name="password" type="password">
	<button type="submit">Submit</button>
</form>