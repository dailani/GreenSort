<script lang="ts">
	import LoadingSpinner from '$lib/components/LoadingSpinner.svelte';

	export let src: string;
</script>

<div class="w-full h-full flex justify-center items-center">
	<img {src} alt="" class="opacity-60 blur-sm" />
	<div class="absolute w-full h-full flex justify-center items-center z-30 top-0">
		<div class="h-20 w-20">
			<LoadingSpinner />
		</div>
	</div>
</div>
