/** @type {import('tailwindcss').Config} */
export default {
	content: ['./src/**/*.{html,js,svelte,ts}'],
	theme: {
		extend: {
			translate: {
				'0': '0',
				'full': '100%',
			  },
		}
	},
	plugins: []
};