<script>
	import { createEventDispatcher } from 'svelte';
	import { is_empty } from 'svelte/internal';

	const dispatch = createEventDispatcher();
	const maxlength = 2000;
	const LINE_LENGTH = 35;

	export let disabled = false;
	let currentMessage = '';
	let rows = 1;
	$: isEmpty = is_empty(currentMessage);

	function addMessage() {
		if (!isEmpty) {
			const newMessage = {
				role: 'user',
				content: currentMessage
			};
			currentMessage = '';
			rows = 1;

			dispatch('newMessage', newMessage);
		}
	}

	function autoResizeTextarea(event) {
		const textarea = event.target.value;
		let rows_on_length = Math.floor(textarea.length / LINE_LENGTH) + 1;
		let rows_on_breaks = textarea.split('\n').length;
		rows = rows_on_length > rows_on_breaks ? rows_on_length : rows_on_breaks;
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
