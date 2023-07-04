<script>
	import AboutBlock from '../../components/AboutBlock.svelte';
	import { Accordion } from '@skeletonlabs/skeleton';

	const blocks = [
		{
			header: 'Диалог с нейросетью',
			content:
				'Тут можно вести диалог с нейросетью ChatGPT. Можно задавать ей любые вопросы и получать на них ответы.'
		},
		{
			header: 'Авторизация через социальные сети',
			content:
				'Есть возможность авторизации через социальные сети, например, Вконтакте. Это позволит вам задавать вопросы без ограничений на количество в минуту, как у неавторизованного пользователя.'
		},
		{
			header: 'Архив вопросов и ответов',
			content:
				'Авторизованные пользователи имеют возможность просмотреть заданные раннее вопросы и ответы на них.'
		}
	];
</script>

<div class="container h-full mx-auto flex justify-center items-center">
	<Accordion>
		{#each blocks as block}
			<AboutBlock {block} />
		{/each}
	</Accordion>
</div>
