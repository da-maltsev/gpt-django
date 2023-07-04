<script>
	import { AccordionItem } from '@skeletonlabs/skeleton';
	export let block;
</script>

<AccordionItem>
	<!--		<svelte:fragment slot="lead">(icon)</svelte:fragment>-->
	<svelte:fragment slot="summary"><h2 class="h2 text-center">{block.header}</h2></svelte:fragment>
	<svelte:fragment slot="content"><p class="text-center">{block.content}</p></svelte:fragment>
</AccordionItem>
