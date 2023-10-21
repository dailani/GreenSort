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

	let cameraRunning: boolean = false;

	let userImage: string | null = null;

	let objectImages: string[] | null = null;
	let currentObjectImage: string | null = null;
	let currentObjectDetails: any | null = null;

	let errorMessage: string | null = null;

	onMount(() => {
		setTimeout(startCameraPreview, 500);
	});

	function updateCurrentState(state: AppState) {
		currentState = state;

		if (state == AppState.Capturing && !cameraRunning) {
			startCameraPreview();
		} else if (cameraRunning) {
			stopCameraPreview();
		}

		if (state <= AppState.ObjectSelection) {
			currentObjectImage = null;
		}
	}

	function startCameraPreview() {
		if (!browser || cameraRunning) {
			return;
		}

		cameraRunning = true;
		CameraPreview.start({
			parent: 'cameraPreview',
			position: 'rear',
			disableAudio: true,
			enableZoom: true,
			toBack: true,
			lockAndroidOrientation: true,	
			rotateWhenOrientationChanged: false
		});
	}

	function stopCameraPreview() {
		if (!browser) {
			return;
		}

		//CameraPreview.stop();
		cameraRunning = false;
	}

	async function captureImage() {
		const image = await CameraPreview.capture({
			quality: 90
		})

		if (image.value == null || image.value.length == 0) {
			return;
		}

		userImage = image.value;
		updateCurrentState(AppState.Cropping);

		try {
			objectImages = await getImages({ image: image.value! });
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
		<div class="w-full h-full -z-10" id="cameraPreview" />
		<div class="w-full absolute left-0 bottom-4 flex justify-center">

			<button on:click={captureImage} class="w-16 h-16 bg-gray-400 rounded-full"></button>
		</div>
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
