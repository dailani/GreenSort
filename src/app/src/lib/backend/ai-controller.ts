interface SourceImage {
	image: string;
}

export async function getImages(content: SourceImage) {
	const response = await fetch('https://greensort-backend-okzie2k6iq-uc.a.run.app/getItems', {
		method: 'POST',
		body: JSON.stringify({ image: content.image }),
		headers: { 'Content-Type': 'application/json; charset=UTF-8' }
	});

	if (!response.ok) {
		throw new Error(response.statusText);
	}

	const data = await response.json();
	return data;
}

interface CroppedImages {
	image: string;
}
export interface ImageMaterials {
	material: string[];
	things: string[];
}

export async function getMaterial(content: CroppedImages) {
	const response = await fetch('https://greensort-backend-okzie2k6iq-uc.a.run.app/getMaterial', {
		method: 'POST',
		body: JSON.stringify({ images: [content.image] }),
		headers: { 'Content-Type': 'application/json; charset=UTF-8' }
	});

	if (!response.ok) {
		throw new Error(response.statusText);
	}

	const data = await response.json();
	return data[0] as ImageMaterials;
}
