<script lang="ts">
	import { getMaterial, type ImageMaterials } from '$lib/backend/ai-controller';
	import LoadingSpinner from '$lib/components/LoadingSpinner.svelte';
	import { createEventDispatcher, onMount } from 'svelte';

	export let objectImage: string;

	let materials: string[] | null = null;
	let things: string[] | null = null;

	const dispatcher = createEventDispatcher<{
		select: { objectImage: string; material: ImageMaterials };
	}>();

	onMount(async () => {
		const res = await getMaterial({
			image: objectImage
		});

		console.log(res);

		materials = res.material;
		things = res.things;
	});

	function selectObject() {
		if (materials == null || things == null) {
			return;
		}

		dispatcher('select', {
			objectImage: objectImage,
			material: {
				material: materials,
				things: things
			}
		});
	}
</script>

<button class="relative w-full max-h-96 bg-gray-300" on:click={selectObject}>
	<img src="data:image/png;base64,{objectImage}" class="rounded-lg w-full h-full -z-10" alt="" />

	<div class="absolute top-2 right-2">
		{#if materials == null || things == null}
			<div class="h-16">
				<LoadingSpinner />
			</div>
		{:else}
			<div class="flex flex-row gap-2">
				<p class="px-4 py-1 bg-yellow-400 rounded-lg">
					{materials[0]}
				</p>
				<p class="px-4 py-1 bg-orange-600 rounded-lg">
					{things[0]}
				</p>
			</div>
		{/if}
	</div>
</button>
