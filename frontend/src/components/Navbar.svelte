<script>
	import { createEventDispatcher } from 'svelte';

	const dispatch = createEventDispatcher();

	export let isAuthenticated = false;

	function handleNavbarToggle() {
		dispatch('navbarToggle', NaN);
	}
</script>

<nav class="border-gray-200">
	<div class="max-w-screen-xl flex flex-wrap items-center justify-between mx-auto p-4">
		<button
			on:click={handleNavbarToggle}
			data-collapse-toggle="navbar-default"
			type="button"
			class="inline-flex items-center p-2 w-10 h-10 justify-center text-sm text-gray-500 rounded-lg md:hidden hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-gray-200 dark:text-gray-400 dark:hover:bg-gray-700 dark:focus:ring-gray-600"
			aria-controls="navbar-default"
			aria-expanded="false"
		>
			<span class="sr-only">Open main menu</span>
			<svg
				class="w-5 h-5"
				aria-hidden="true"
				xmlns="http://www.w3.org/2000/svg"
				fill="none"
				viewBox="0 0 17 14"
			>
				<path
					stroke="currentColor"
					stroke-linecap="round"
					stroke-linejoin="round"
					stroke-width="2"
					d="M1 1h15M1 7h15M1 13h15"
				/>
			</svg>
		</button>
		<div class="hidden w-full md:block md:w-auto" id="navbar-default">
			<ul class="flex flex-col p-1 md:p-0 mt-4 md:flex-row md:space-x-8 md:mt-0 md:border-0">
				<li>
					<a
						href="/"
						rel="noreferrer"
						target="_self"
						class="whitespace-pre block py-1 pl-1 pr-1 font-bold text-xl uppercase">Web assistant</a
					>
				</li>
				<li>
					<a
						href="/about"
						rel="noreferrer"
						class="whitespace-pre block py-1 pl-1 pr-1 text-xl uppercase">Про сайт</a
					>
				</li>
				{#if isAuthenticated === false}
					<li>
						<a
							href="/auth"
							rel="noreferrer"
							class="whitespace-pre block py-1 pl-1 pr-1 text-xl uppercase">Авторизоваться</a
						>
					</li>
				{/if}
				{#if isAuthenticated === true}
					<li>
						<a
							href="/replies"
							rel="noreferrer"
							class="whitespace-pre block py-1 pl-1 pr-1 text-xl uppercase pointer-events-none"
							disabled>Мои вопросы и ответы</a
						>
					</li>
				{/if}
			</ul>
		</div>
	</div>
</nav>
