<script lang="ts">
	import { browser } from '$app/environment';
	import { CameraPreview } from '@capacitor-community/camera-preview';
	import { Camera, CameraResultType, CameraSource } from '@capacitor/camera';
	import { onMount } from 'svelte';
	import ImageBackgroundLoader from './ImageBackgroundLoader.svelte';
	import { getImages } from '$lib/backend/ai-controller';
	import { getMaterial } from '$lib/backend/ai-controller';

	enum AppState {
		Capturing,
		Cropping,
		ObjectSelection,
		ObjectClassification,
		ObjectDetails,
		Error
	}

	let currentState: AppState = AppState.Capturing;

	let userImage: string | null = null;

	let objectImages: string[] | null = null;
	let currentObjectImage: string | null = null;
	let currentObjectDetails: any | null = null;

	let errorMessage: string | null = null;

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
			resultType: CameraResultType.Base64,
			saveToGallery: false
		});

		if (image.base64String == undefined) {
			return;
		}

		userImage = image.base64String;
		updateCurrentState(AppState.Cropping);

		try {
			objectImages = await getImages({ image: image.base64String! });
		} catch (error) {
			errorMessage = String(error);
			updateCurrentState(AppState.Error);
		}

		updateCurrentState(AppState.ObjectSelection);
	}

	async function selectObject(objectImage: string) {
		currentObjectImage = objectImage;
		updateCurrentState(AppState.ObjectClassification);

		try {
			const materials = await getMaterial({ image: objectImage });
		} catch (error) {
			errorMessage = String(error);
			updateCurrentState(AppState.Error);
		}

		updateCurrentState(AppState.ObjectDetails);
	}
</script>

<div class="h-full w-full px-3 py-2">
	{#if currentState == AppState.Capturing}
		<div id="cameraPreview" />
		<button on:click={captureImage} class="absolute bottom-2 left-1/2 right-1/2">O</button>
	{:else if currentState == AppState.Cropping}
		<ImageBackgroundLoader
			title="Detecting Objects..."
			src="data:image/png;base64,{userImage ?? ''}"
		/>
	{:else if currentState == AppState.ObjectSelection}
		<h2 class="font-bold text-xl text-center">Select an object</h2>
		<hr class="my-2" />
		<div class="grid overflow-auto grid-cols-2 gap-4 p-4 bg-zinc-700 rounded-lg">
			{#each objectImages ?? [] as objectImage}
				<button class="w-full max-h-96" on:click={() => selectObject(objectImage)}>
					<img src="data:image/png;base64,{objectImage}" class="rounded-lg w-full h-full" alt="" />
				</button>
			{/each}
		</div>
	{:else if currentState == AppState.ObjectClassification}
		<ImageBackgroundLoader
			title="Finding Recycling Details..."
			src="data:image/png;base64,{currentObjectImage ?? ''}"
		/>
	{:else if currentState == AppState.ObjectDetails}
		<p>Object Details here</p>
	{:else if currentState == AppState.Error}
		<h2 class="font-bold text-lg text-red-700">An error occured</h2>
		<p>{errorMessage}</p>
	{/if}
</div>
