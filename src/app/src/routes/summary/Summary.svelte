
<script lang="ts">
	import type { ImageMaterials } from '$lib/backend/ai-controller';
	export let src: string;
    export let onBack: () => void;
    export let materials: ImageMaterials;
    export let category: string;

</script>

<div on:click={onBack} class=" flex flex-col bg-[#1c0418] px-4 py-2 rounded-b-[48px] items-center justify-center gap-[1px]">
    <p  class="text-neutral-100 text-sm  border-white rounded-2xl w-fit px-2 " >Back to image selection</p>
</div>

<div class="flex flex-col px-4 gap-y-4  py-5">
    <div class="flex flex-col  bg-white rounded-md shadow-md gap-x-5  ">
        <div class=" object-cover">
            <img {src} alt="" class="w-full max-h-82 object-cover" />
        </div>
          <div class="flex flex-col py-1 px-2  bg-[#16b78d] shadow-sm rounded-b-md">
            <div class="flex flex-col p-2 items-center">
                <div class="text-sm items-center text-white ">This item's material consists of</div>
                <div class=" text-2xl text-white font-bold flex flex-wrap text-clip">{materials == null ? 'Not Found' : materials.material}</div>
            </div>
        
        </div>
    </div>
    <div class="bg-[#16b78d] rounded-md shadow-md text-white py-2">
    
        <div class="text-md items-center text-white text-center text-2xl">Disposal Information</div>
            <div class="flex flex-col gap-y-2 p-2">
            <div class="flex flex-row justify-between">
                <div class="text-xl">Category</div>
                <div class="text-xl">{category}</div>
            </div>
            <div class="flex flex-row justify-between">
                <div class="text-xl">Reusable</div>
                <div class="text-xl">Yes</div>
            </div>
            <div class="flex flex-col p-2 items-center">
                <div class="text-md items-center text-white ">Recycle this item and save</div>
                <div class=" text-2xl text-white font-bold flex flex-wrap text-clip">+12</div>
                <div class=" text-2xl text-white font-bold flex flex-wrap text-clip">Carbon Credits</div>
            </div>
          
        </div>
    </div>

    <div class=" bg-[#1c0418] rounded-md shadow-md text-white py-2">
        <h1 class="font-bold text-md items-center text-white text-center text-2xl">How to Recycle</h1>
    </div>
    
</div>