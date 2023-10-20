<script lang="ts">
	import { browser } from '$app/environment';
	import LoadingSpinner from '$lib/components/LoadingSpinner.svelte';
	import { debounceSync } from '$lib/utils';
	import { CameraPreview } from '@capacitor-community/camera-preview';
	import { Camera, CameraResultType, CameraSource } from '@capacitor/camera';
	import { onDestroy, onMount } from 'svelte';

	var started = false;
	var processing = false;

	var imageSrc: string | null = null;
	var parentDiv: HTMLDivElement;
	var sizeObserver: ResizeObserver = null!;

	onMount(() => {
		sizeObserver = new ResizeObserver((elem) => {
			console.log(elem[0].contentRect);
			debounceSync(
				'o',
				() => startCameraPreview(elem[0].contentRect.width, elem[0].contentRect.height),
				100
			);
		});

		sizeObserver.observe(parentDiv);
		startCameraPreview(parentDiv.clientWidth, parentDiv.clientHeight);
	});

	onDestroy(() => {
		if (browser) {
			sizeObserver.disconnect();
		}
	});

	function startCameraPreview(width: number, height: number) {
		if (!browser || processing) {
			return;
		}
		if (started) {
			CameraPreview.stop();
		}
		started = true;

		CameraPreview.start({
			parent: 'cameraPreview',
			position: 'rear',
			toBack: true,
			height: height,
			width: width
		});
	}

	async function captureImage() {
		const image = await Camera.getPhoto({
			source: CameraSource.Camera,
			quality: 90,
			resultType: CameraResultType.Uri,
			saveToGallery: false
		});

		if (image.webPath == undefined) {
			return;
		}

		processing = true;
		imageSrc = image.webPath;

		CameraPreview.stop();

		await new Promise((resolve) => setTimeout(resolve, 30000));

		imageSrc = null;
		processing = false;
		startCameraPreview(parentDiv.clientWidth, parentDiv.clientHeight);
	}
</script>

<div class="h-full w-full" bind:this={parentDiv}>
	<div id="cameraPreview" />

	{#if imageSrc != null}
		<div class="w-full h-full flex justify-center items-center">
			<img src={imageSrc} alt="" class="opacity-60 blur-sm" />
			<div class="absolute w-full h-full flex justify-center items-center z-30 top-0">
				<div class="h-20 w-20">
					<LoadingSpinner />
				</div>
			</div>
		</div>
	{:else}
		<button on:click={captureImage} class="absolute bottom-2 left-1/2 right-1/2">O</button>
	{/if}
</div>
