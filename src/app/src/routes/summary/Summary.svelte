
<script lang="ts">
    	
	export let src: string;
    export let onBack: () => void;
    export let materials: ImageMaterials;

    
	interface ImageMaterials {
	materials: string[];
	things: string[];
}
</script>

<div class=" flex flex-col bg-[#7A3E3E] px-4 py-2 rounded-b-[48px] gap-3 items-center ">

    <p class="text-center text-sm text-neutral-300">This is the summary of the the specific item</p>
    <button on:click={onBack} class="text-white font-bold border-solid border-2 border-white rounded-2xl w-fit px-2 py-1 " >Back</button>

</div>

<div class="flex flex-col px-4 gap-y-4  py-5">
    <div class="flex flex-col  bg-white rounded-md shadow-md gap-x-5  ">
        <div class=" object-cover">
            <img {src} alt="" class="w-full max-h-52 object-cover" />
        </div>
          <div class="flex flex-col py-1 px-2  bg-[#47A992] shadow-sm rounded-b-md">
            <div class="flex flex-col p-2 items-center">
                <div class="text-md items-center text-white "> This item consists of</div>
                <div class=" text-2xl text-white font-bold flex flex-wrap text-clip">{materials == null ? 'Not Found' : materials.material}</div>

            </div>
            <div class=" flex flex-col items-center gap-2 py-[7px] text-white">
                <div>      
                <div class="text-md items-center text-white ">Carbon Credit</div>
                    <div class="text-2xl font-mono font-bold text-center">0.5</div>
                </div>
              
            </div>
        </div>
    </div>
    <div class=" bg-[#47A992] rounded-md shadow-md text-white">
        <div>
            <div class="flex flex-row justify-between p-2">
                <div class="text-xl font-bold">Recycling Details</div>
                <div class="text-xl font-bold"></div>
            </div>
            <div class="flex flex-col gap-y-2 p-2">
                <div class="flex flex-row justify-between">
                    <div class="text-xl">Recycle</div>
                    <div class="text-xl">Yes</div>
                </div>
                <div class="flex flex-row justify-between">
                    <div class="text-xl">Reuse</div>
                    <div class="text-xl">Yes</div>
                </div>
                <div class="flex flex-row justify-between">
                    <div class="text-xl">Reduce</div>
                    <div class="text-xl">Yes</div>
                </div>
            </div>
        </div>
        <div class="">
            how to
        </div>
        <div class=""> 
            where
        </div>
    </div>
</div>