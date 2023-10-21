<script>
	import { onMount } from 'svelte';
	import '../app.css';
	import { Camera } from '@capacitor/camera';
	import { CameraPreview } from '@capacitor-community/camera-preview';

	onMount(() => {
		Camera.requestPermissions();
	});
</script>

<div class="flex flex-col w-full h-full bg-neutral-600 text-white">
	<main class="grow flex-1 min-h-0">
		<slot />
	</main>
</div>
