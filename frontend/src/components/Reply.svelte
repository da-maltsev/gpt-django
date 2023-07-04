<script>
	export let message;

	let isUser = message.role === 'user';

	let divClass = isUser ? 'grid grid-cols-[1fr_auto] gap-2' : 'grid grid-cols-[auto_1fr] gap-2';
	let contentClass = isUser
		? 'card p-4 rounded-tr-none space-y-2 variant-soft-primary'
		: 'card p-4 variant-soft rounded-tl-none space-y-2';
</script>

<div class={divClass}>
	<div class={contentClass}>
		<pre>{message.content}</pre>
	</div>
</div>
