
<script lang="ts">
    	
	export let src: string;
    export let onBack: () => void;
    export let materials: ImageMaterials;
    let trashcanImg = '$lib/static/trashcans.jpg'

    
	interface ImageMaterials {
	materials: string[];
	things: string[];
}
</script>

<div class=" flex flex-row bg-[#1c0418] px-4 py-2 rounded-b-[48px] gap-3 items-center justify-center">
    <button on:click={onBack} class="text-white font-bold border-solid border-2 border-white rounded-2xl w-fit px-2 py-1 " >Back</button>
    <div class=" text-2xl text-white font-bold flex flex-wrap text-clip">{materials == null ? 'Not Found' : materials.material}</div>
</div>

<div class="flex flex-col px-4 gap-y-4  py-5">
    <div class="flex flex-col  bg-white rounded-md shadow-md gap-x-5  ">
        <div class=" object-cover">
            <img {src} alt="" class="w-full max-h-72 object-cover" />
        </div>
          <div class="flex flex-col py-1 px-2  bg-[#16b78d] shadow-sm rounded-b-md">
            <div class="flex flex-col p-2 items-center">
                <div class="text-md items-center text-white ">Recycle this item and save</div>
                <div class=" text-2xl text-white font-bold flex flex-wrap text-clip">0.5</div>
                <div class=" text-2xl text-white font-bold flex flex-wrap text-clip">Carbon Credits</div>
            </div>
        </div>
    </div>
    <div class="bg-[#16b78d] rounded-md shadow-md text-white">
        <div class="text-md items-center text-white text-center text-2xl">Disposal Information</div>
            <div class="flex flex-col gap-y-2 p-2">
            <div class="flex flex-row justify-between">
                <div class="text-xl">Category</div>
                <div class="text-xl">Yes</div>
            </div>
            <div class="flex flex-row justify-between">
                <div class="text-xl">Reusable</div>
                <div class="text-xl">Yes</div>
            </div>
            <div class="flex flex-row justify-between">
                <div class="text-xl">Location</div>
                <div class="text-xl">small "redirect" icon</div>
            </div>
            <div>
                <img src={trashcanImg} alt="Recycling Trash Cans" class="">
            </div>
        </div>
    </div>
</div>