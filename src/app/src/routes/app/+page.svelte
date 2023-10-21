<script lang="ts">
	import { browser } from '$app/environment';
	import LoadingSpinner from '$lib/components/LoadingSpinner.svelte';
	import { debounceSync } from '$lib/utils';
	import { CameraPreview } from '@capacitor-community/camera-preview';
	import { Camera, CameraResultType, CameraSource } from '@capacitor/camera';
	import { onDestroy, onMount } from 'svelte';

	enum AppState {
		Capturing,
		Cropping,
		ObjectSelection,
		Error
	}

	let currentState: AppState = AppState.Capturing;

	let userImageSrc: string | null;

	let objectImages: string[] | null;

	let errorMessage: string | null;

	onMount(() => {
		startCameraPreview();
	});

	function updateCurrentState(state: AppState) {
		currentState = state;

		if (state == AppState.Capturing) {
			startCameraPreview();
		} else {
			stopCameraPreview();
		}
	}

	function startCameraPreview() {
		if (!browser) {
			return;
		}

		CameraPreview.start({
			parent: 'cameraPreview',
			position: 'rear',
			toBack: true
		});
	}

	function stopCameraPreview() {
		if (!browser) {
			return;
		}
		CameraPreview.stop();
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

		userImageSrc = image.webPath;
		updateCurrentState(AppState.Cropping);

		try {
		} catch (error) {
			errorMessage = String(error);
			updateCurrentState(AppState.Error);
		}

		//ToDo: Call backend for cropping

		await new Promise((resolve) => setTimeout(resolve, 30000));

		updateCurrentState(AppState.ObjectSelection);
	}
</script>

<div class="h-full w-full">
	{#if currentState == AppState.Capturing}
		<div id="cameraPreview" />
		<button on:click={captureImage} class="absolute bottom-2 left-1/2 right-1/2">O</button>
	{:else if currentState == AppState.Cropping}
		<div class="w-full h-full flex justify-center items-center">
			<img src={userImageSrc} alt="" class="opacity-60 blur-sm" />
			<div class="absolute w-full h-full flex justify-center items-center z-30 top-0">
				<div class="h-20 w-20">
					<LoadingSpinner />
				</div>
			</div>
		</div>
	{:else if currentState == AppState.ObjectSelection}
		<h2>Select an object</h2>
		<div class="grid grid-cols-2">
			{#each objectImages ?? [] as objectImage}
				<button class="w-full max-h-28">
					<img src={objectImage} class="w-full h-full" alt="" />
				</button>
			{/each}
		</div>
	{:else if currentState == AppState.Error}
		<h2 class="font-bold text-lg text-red-700">An error occured</h2>
		<p>{errorMessage}</p>
	{/if}
</div>
