<script>
	import { onMount } from 'svelte';
	import '../app.css';
	import { Camera } from '@capacitor/camera';
	import { getAddress, getCategory } from '$lib/backend/ai-controller';

	onMount(() => {
		Camera.requestPermissions();
	});

	async function captureImage(){
		let a = await getAddress("Akkus");
		try {
			let a = await getAddress("material");
			console.log('Category:' + a);
		} catch (error) {
			console.log("lol")
			return;
		}
	}
</script>

<div class="flex flex-col w-full h-full">
	<button on:click={captureImage} class="w-16 h-16 bg-gray-400 rounded-full" />
	<main class="grow flex-1 min-h-0">
		<slot />
	</main>
</div>
