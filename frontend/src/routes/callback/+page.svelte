<script>
	import { onMount } from 'svelte';
	let goAuthorized;
	onMount(() => goAuthorized.focus());
</script>

<div class="container h-full mx-auto flex justify-center items-center">
	<div class="space-y-10 flex flex-col items-center">
		<h2 class="h2">Прекрасно, ты авторизовался. Теперь продолжим общение!</h2>
		<a
			bind:this={goAuthorized}
			href="/"
			target="_self"
			class="btn-xl variant-filled card-hover rounded-full"
		>
			<span>Возвращаемся с именем!</span>
		</a>
	</div>
</div>
