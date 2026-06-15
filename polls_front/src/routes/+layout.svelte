<script lang="ts">
	import favicon from '$lib/assets/favicon.svg';
	import { resolve } from '$app/paths';

	let { children } = $props();
</script>

<svelte:head>
	<link rel="icon" href={favicon} />
</svelte:head>

<nav>
	<a href={resolve('/')}>Home</a>
	<!-- <a href={resolve("/poll/new")}>New Poll</a> -->
	<a href={resolve("/login")}>Login</a>
</nav>

{@render children()}
