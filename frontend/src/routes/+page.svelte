<script>
	import Reply from '../components/Reply.svelte';
	import NewMessage from '../components/NewMessage.svelte';
	import { post } from '../utils/client.js';
	import { Modal, modalStore } from '@skeletonlabs/skeleton';
	import { ProgressBar } from '@skeletonlabs/skeleton';
	import { messageStore } from '../utils/messagesStore.js';
	import UsageCount from '../components/UsageCount.svelte';
	import { tokenStore } from '../utils/tokenStore.js';

	$tokenStore;
	$messageStore;
	$: messages = $messageStore;

	let disableNewMessage = false;

	const modalBadResponse = {
		type: 'alert',
		title: 'Что-то пошло не так',
		body: 'Попробуйте переформулировать вопрос или попробуйте позже.',
		image: 'https://media.tenor.com/rtKFHEGpoPwAAAAM/meme-lang.gif'
	};

	function handleNewMessage(event) {
		messages = [...messages, event.detail];
	}

	function handleRemoveMessages() {
		messageStore.set('');
	}

	function handleBadResponse() {
		messages.pop();
		messages = messages;
		modalStore.trigger(modalBadResponse);
	}

	async function sendChatMessage() {
		try {
			console.log(messages);
			disableNewMessage = true;

			const response = await post('/api/v1/chat/', {
				messages: messages
			});

			if (response.ok) {
				const data = await response.json();
				console.log(data);
				messages = [...data.messages];
				messageStore.set(messages);
			} else {
				handleBadResponse();
				console.error('BadResponse:', response);
			}
		} catch (error) {
			handleBadResponse();
			console.error('Error:', error);
		}

		disableNewMessage = false;
	}
</script>

<title>Web assistant</title>
<Modal />

<div class="container h-full mx-auto flex justify-center items-center">
	<div class="space-y-10 flex flex-col items-center">
		<h2 class="h2">Привет, давай общаться!</h2>
		<UsageCount />
		{#each messages as message}
			<Reply {message} />
		{/each}
		{#if disableNewMessage}
			<ProgressBar />
		{/if}
		<NewMessage
			disabled={disableNewMessage}
			on:newMessage={handleNewMessage}
			on:newMessage={sendChatMessage}
		/>
		<button type="button" class="btn variant-ghost-tertiary" on:click={handleRemoveMessages}
			>Начнем по новой</button
		>
	</div>
</div>
