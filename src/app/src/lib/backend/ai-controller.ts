interface SourceImage {
	image: string;
}

async function getImages(content: SourceImage): Promise<any> {
	const response = await fetch('this is endpoint url', {
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

export default getImages;
