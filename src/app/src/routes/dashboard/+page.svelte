<!-- src/routes/index.svelte -->

<script>

    import Modal from '$lib/components/Modal.svelte'
    let showModal = false;
  
    function openModal() {
      showModal = true;
    }
  
    function closeModal() {
      showModal = false;
    }
  </script>
  
  <button on:click={openModal}>Open Modal</button>
  
  {#if showModal}
    <Modal {isOpen} on:click={closeModal}>
      <!-- Modal content goes here -->
      <p>This is your modal content.</p>
    </Modal>
  {/if}  