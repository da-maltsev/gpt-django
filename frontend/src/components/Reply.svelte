<script>
	import { clickToCopy } from '../utils/clickToCopy.js';
	import { fade } from 'svelte/transition';
	export let message = { role: 'assistant', content: 'Попробуйте задать любой вопрос.' };

	let visible = false;
	let isUser = message.role === 'user';

	let divClass = isUser ? 'grid grid-cols-[1fr_auto] gap-2' : 'grid grid-cols-[auto_1fr] gap-2';
	let contentClass = isUser
		? 'container card p-4 rounded-tr-none space-y-2 variant-soft-primary  card-hover'
		: 'container card p-4 variant-soft rounded-tl-none space-y-2  card-hover';

	function textCopiedAlert() {
		visible = true;
		setTimeout(() => (visible = false), 2000);
	}
</script>

<div class={divClass}>
	{#if visible && isUser}
		<aside class="alert variant-ghost" transition:fade|local={{ duration: 200 }}>
			Текст скопирован
		</aside>
	{/if}
	<div class={contentClass}>
		<pre class="whitespace-pre-wrap" use:clickToCopy on:click={textCopiedAlert}>
			{message.content.replace(/\r\n/g, '<br/>')}
		</pre>
	</div>
	{#if visible && !isUser}
		<aside class="alert variant-ghost" transition:fade|local={{ duration: 200 }}>
			Текст скопирован
		</aside>
	{/if}
</div>
