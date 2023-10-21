<script lang="ts">
	import { browser } from '$app/environment';
	import LoadingSpinner from '$lib/components/LoadingSpinner.svelte';
	import { debounceSync } from '$lib/utils';
	import { CameraPreview } from '@capacitor-community/camera-preview';
	import { Camera, CameraResultType, CameraSource } from '@capacitor/camera';
	import { onDestroy, onMount } from 'svelte';
	import ImageBackgroundLoader from './ImageBackgroundLoader.svelte';
	import getImages from '$lib/backend/ai-controller';

	enum AppState {
		Capturing,
		Cropping,
		ObjectSelection,
		ObjectClassification,
		ObjectDetails,
		Error
	}

	let currentState: AppState = AppState.Capturing;

	let userImageSrc: string | null;

	let objectImages: string[] | null;
	let currentObjectImage: string | null;
	let currentObjectDetails: any | null;

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

		if (state <= AppState.ObjectSelection) {
			currentObjectImage = null;
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
			resultType: CameraResultType.Base64 || CameraResultType.Uri,
			saveToGallery: false
		});

		console.log(image.base64String);

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
		await getImages({image: image.base64String!});
	

		await new Promise((resolve) => setTimeout(resolve, 5000));

		updateCurrentState(AppState.ObjectSelection);
	}

	async function selectObject(objectImage: string) {
		currentObjectImage = objectImage;
		updateCurrentState(AppState.ObjectClassification);

		//ToDo: Run Classification
		await new Promise((resolve) => setTimeout(resolve, 5000));

		updateCurrentState(AppState.ObjectDetails);
	}
</script>

<div class="h-full w-full">
	{#if currentState == AppState.Capturing}
		<div id="cameraPreview" />
		<button on:click={captureImage} class="absolute bottom-2 left-1/2 right-1/2">O</button>
	{:else if currentState == AppState.Cropping}
		<ImageBackgroundLoader src={userImageSrc ?? ''} />
	{:else if currentState == AppState.ObjectSelection}
		<h2 class="font-bold text-lg">Select an object</h2>
		<div class="grid grid-cols-2">
			{#each objectImages ?? [] as objectImage}
				<button class="w-full max-h-28" on:click={() => selectObject(objectImage)}>
					<img src={objectImage} class="w-full h-full" alt="" />
				</button>
			{/each}
		</div>
	{:else if currentState == AppState.ObjectClassification}
		<ImageBackgroundLoader src={currentObjectImage ?? ''} />
	{:else if currentState == AppState.ObjectDetails}
		<p>Object Details here</p>
	{:else if currentState == AppState.Error}
		<h2 class="font-bold text-lg text-red-700">An error occured</h2>
		<p>{errorMessage}</p>
	{/if}
</div>
