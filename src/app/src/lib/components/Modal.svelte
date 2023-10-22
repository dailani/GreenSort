<!-- src/components/Modal.svelte -->

<script>
	export let isOpen;
</script>

<div
	class="fixed inset-0 flex items-center justify-center z-50"
	style="display: {isOpen ? 'block' : 'none'};"
	role="dialog"
	aria-modal="true"
>
	<div
		class="fixed inset-0 bg-white opacity-90"
		on:click={() => (isOpen = false)}
		style="tabindex: 0;"
	/>
	<div
		class="w-full max-w-4xl p-6 transform translate-y-0 translate-y-full bg-white rounded-lg p-4"
		style="transform: {isOpen ? 'translateY(0)' : 'translateY(100%)'};"
	>
		<div class="bg-white rounded-lg p-4">
			<slot />
		</div>
	</div>
</div>
