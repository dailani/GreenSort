const debounceTimeouts = new Map<string, NodeJS.Timeout>();

export function debounce<T>(id: string, callback: () => Promise<T>, ms: number) {
	if (debounceTimeouts.has(id)) {
		clearTimeout(debounceTimeouts.get(id));
	}

	const timeout = setTimeout(callback, ms);
	debounceTimeouts.set(id, timeout);
}

export function debounceSync<T>(id: string, callback: () => T, ms: number) {
	if (debounceTimeouts.has(id)) {
		clearTimeout(debounceTimeouts.get(id));
	}

	const timeout = setTimeout(callback, ms);
	debounceTimeouts.set(id, timeout);
}
