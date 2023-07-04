<script>
	import { createEventDispatcher } from 'svelte';
	import { is_empty } from 'svelte/internal';
	import { addLineBreaks } from '../utils/lineBreaker.js';

	const dispatch = createEventDispatcher();
	const maxlength = 1000;

	export let disabled = false;
	let currentMessage = '';
	let rows = 1;
	$: isEmpty = is_empty(currentMessage);

	function addMessage() {
		if (!isEmpty) {
			let messageWithBreaks = addLineBreaks(currentMessage);

			const newMessage = {
				role: 'user',
				content: messageWithBreaks
			};
			currentMessage = '';
			rows = 1;

			dispatch('newMessage', newMessage);
		}
	}

	function autoResizeTextarea(event) {
		const textarea = event.target.value;
		rows = Math.floor(textarea.length / 100) + 1;
	}
</script>

<div class="input-group input-group-divider grid-cols-[1fr_auto] rounded-container-token">
	<textarea
		bind:value={currentMessage}
		class="bg-transparent border-0 ring-0"
		name="prompt"
		id="prompt"
		placeholder="Напиши свой вопрос..."
		{rows}
		{maxlength}
		on:input={autoResizeTextarea}
	/>
	<button class="variant-filled-primary" {disabled} on:click={addMessage}>Спросить</button>
</div>
