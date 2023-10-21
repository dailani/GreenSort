<script lang="ts">
	import LoadingSpinner from '$lib/components/LoadingSpinner.svelte';

	export let src: string;
	export let title: string;
</script>

<div class="w-full h-full flex justify-center items-center">
	<img {src} alt="" class="opacity-60 blur-sm" />
	<div class="absolute w-full h-full flex flex-col gap-6 justify-center items-center z-30 top-0">
		<p class="font-bold text-lg">{title}</p>
		<div class="h-32 w-32">
			<LoadingSpinner />
		</div>
	</div>
</div>
