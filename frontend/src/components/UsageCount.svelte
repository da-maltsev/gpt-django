<script>
	import { get } from '../utils/client.js';
	import { onMount } from 'svelte';

	$: usageCount = 0;
	$: hidden = false;

	function hideElement() {
		hidden = true;
	}

	async function getUsageCount() {
		try {
			const response = await get('/api/v1/replies/count/');
			console.log(response);
			if (response.ok) {
				const data = await response.json();
				usageCount = data.count;
			}
		} finally {
			usageCount = usageCount;
		}
	}

	onMount(async () => {
		getUsageCount();
	});
</script>

{#if usageCount > 0 && !hidden}
	<span class="badge variant-tertiary card-hover" on:click={hideElement}
		>уже было получено: {usageCount} ответов</span
	>
{/if}
