<script>
	import { onMount } from 'svelte';
	import '../app.css';
	import { Camera } from '@capacitor/camera';
	import { getAddress, getCategory } from '$lib/backend/ai-controller';

	onMount(() => {
		Camera.requestPermissions();
	});

</script>

<div class="flex flex-col w-full h-full">
	<main class="grow flex-1 min-h-0">
		<slot />
	</main>
</div>
