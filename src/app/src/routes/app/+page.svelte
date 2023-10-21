<script lang="ts">
	import { browser } from '$app/environment';
	import { CameraPreview } from '@capacitor-community/camera-preview';
	import { Camera, CameraResultType, CameraSource } from '@capacitor/camera';
	import { onMount } from 'svelte';
	import ImageBackgroundLoader from './ImageBackgroundLoader.svelte';
	import { getImages } from '$lib/backend/ai-controller';
	import { getMaterial } from '$lib/backend/ai-controller';
	import { App } from '@capacitor/app';
	import Summary from '../summary/Summary.svelte';
	import GalleryIcon from "$lib/static/gallery.svg"

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
		console.log("App Mounted!");

		setTimeout(startCameraPreview, 50);

		App.addListener("backButton", e => {
			if (currentState == AppState.Capturing) {
				App.exitApp();	
				return;
			} 

			if (currentState == AppState.ObjectSelection || currentState == AppState.Error) {
				updateCurrentState(AppState.Capturing);
			} else if (currentState == AppState.ObjectDetails) {
				updateCurrentState(AppState.ObjectSelection);
			}
		})
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
		if (!browser || cameraRunning) {
			return;
		}

		try {
			CameraPreview.start({
				parent: 'cameraPreview',
				position: 'rear',
				disableAudio: true,
				enableZoom: true,
				toBack: true,
				lockAndroidOrientation: true,	
				rotateWhenOrientationChanged: false
			});
			cameraRunning = true;
		} catch (error) {
			console.log("Starting Camera Preview Failed. Retrying later...")
			setTimeout(startCameraPreview, 250);
			cameraRunning = false;
		}
	}

	function stopCameraPreview() {
		if (!browser || !cameraRunning) {
			return;
		}

		CameraPreview.stop();
		cameraRunning = false;
	}

	async function captureImage() {
		const image = await CameraPreview.capture({
			quality: 90
		})

		await processImage(image.value);
	}

	async function enterGalleryImage() {
		const image = await Camera.getPhoto({
			resultType: CameraResultType.Base64,
			allowEditing: true,
			source: CameraSource.Photos
		});

		await processImage(image.base64String);
	}

	async function processImage(imageBase64: string | undefined | null) {
		if (imageBase64 == null || imageBase64.length == 0) {
			return;
		}

		userImage = imageBase64;
		updateCurrentState(AppState.Cropping);

		try {
			objectImages = await getImages({ image: imageBase64 });
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

<div class="h-full w-full  {currentState == AppState.ObjectDetails ? '' : 'py-2 px-3'}">
	{#if currentState == AppState.Capturing}
		<div class="w-full h-full -z-10" id="cameraPreview" />
		<div class="w-full absolute left-0 bottom-4 flex justify-center">
			<button on:click={captureImage} class="w-16 h-16 bg-gray-400 rounded-full"></button>
			<button on:click={enterGalleryImage} class="w-16 h-16 absolute right-4"><img src="{GalleryIcon}" alt="Pick from Gallery"></button>
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
		<Summary src="data:image/png;base64,{currentObjectImage ?? ''}"/>
	{:else if currentState == AppState.Error}
		<h2 class="font-bold text-lg text-red-700">An error occured</h2>
		<p>{errorMessage}</p>
	{/if}
</div>
