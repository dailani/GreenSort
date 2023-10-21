interface SourceImage {
	image: string;
}

interface CropedImages {
	images: string[];
}

export async function getImages(content: SourceImage): Promise<any> {
	const response = await fetch('https://greensort-backend-okzie2k6iq-uc.a.run.app/upload', {
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

export async function getMaterial(content: CropedImages): Promise<any> {
	const response = await fetch('https://greensort-backend-okzie2k6iq-uc.a.run.app/getMaterial', {
		method: 'POST',
		body: JSON.stringify({ image: content.images }),
		headers: { 'Content-Type': 'application/json; charset=UTF-8' }
	});

	if (!response.ok) {
		throw new Error(response.statusText);
	}

	const data = await response.json();
	return data;
}
