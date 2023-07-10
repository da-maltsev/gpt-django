<script>
	// The ordering of these imports is critical to your app working properly
	import '@skeletonlabs/skeleton/themes/theme-crimson.css';
	// If you have source.organizeImports set to true in VSCode, then it will auto change this ordering
	import '@skeletonlabs/skeleton/styles/skeleton.css';
	// Most of your app wide CSS should be put in this file
	import '../app.postcss';
	import { AppShell, AppBar } from '@skeletonlabs/skeleton';
	import { LightSwitch } from '@skeletonlabs/skeleton';
	import Navbar from '../components/Navbar.svelte';

	export const ssr = false;

	let hiddenTrail = false;

	function handleNavbarToggle() {
		hiddenTrail = !hiddenTrail;
	}
</script>

<!-- App Shell -->
<AppShell>
	<svelte:fragment slot="header">
		<!-- App Bar -->
		<AppBar>
			<svelte:fragment slot="lead">
				<Navbar on:navbarToggle={handleNavbarToggle} />
			</svelte:fragment>
			<svelte:fragment slot="trail">
				{#if !hiddenTrail}
					<LightSwitch />
					<a
						class="btn btn-sm variant-ghost-surface"
						href="https://github.com/da-maltsev/gpt-django"
						target="_blank"
						rel="noreferrer"
					>
						GitHub
					</a>
				{/if}
			</svelte:fragment>
		</AppBar>
	</svelte:fragment>
	<slot />
	<svelte:fragment slot="pageFooter">
		<!-- Animated Logo -->
		<figure>
			<section class="img-bg" />
			<svg class="fill-token -scale-x-[80%]" viewBox="0 0 50 50">
				<path
					fill-rule="evenodd"
					d=" M30.3,32.6c7.2,6.8,12.1,17,12.1,23c0,9.7-9.3,5.4-21,5.4S0.1,65.2,0.1,55.6c0-6.1,4.9-16.2,12.1-23"
				/>
				<path
					fill-rule="evenodd"
					d=" M27.2,33c8.7-1.8,15.1-7.4,15.1-14.1c0-2.9-2-7.2-2.8-8.8C40.4,8.4,41,0.9,39.6,0c-1.5-0.8-8.3,6.4-8.3,6.4 c-3.2-1.4-6-2.2-10.1-2.2S13.3,5,10.1,6.4c0,0-5.6-7.1-7.1-6.2C1.6,1,1.9,8.1,2.7,10C1.9,11.6,0,16,0,18.9 C0,25.6,6.4,31.2,15.1,33"
				/></svg
			>
		</figure>
	</svelte:fragment>
</AppShell>

<style lang="postcss">
	figure {
		@apply flex relative flex-col;
	}
	figure svg,
	.img-bg {
		@apply w-32 h-32 md:w-40 md:h-40;
	}
	.img-bg {
		@apply absolute z-[-1] rounded-full blur-[50px] transition-all;
		animation: pulse 5s cubic-bezier(0, 0, 0, 0.5) infinite, glow 5s linear infinite;
	}
	@keyframes glow {
		0% {
			@apply bg-primary-400/50;
		}
		33% {
			@apply bg-secondary-400/50;
		}
		66% {
			@apply bg-tertiary-400/50;
		}
		100% {
			@apply bg-primary-400/50;
		}
	}
	@keyframes pulse {
		50% {
			transform: scale(1.5);
		}
	}
</style>
