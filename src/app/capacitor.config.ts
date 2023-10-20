import { CapacitorConfig } from '@capacitor/cli';

const config: CapacitorConfig = {
	appId: 'com.greensort.app',
	appName: 'GreenSort',
	webDir: 'build',
	server: {
		androidScheme: 'https'
	}
};

export default config;
