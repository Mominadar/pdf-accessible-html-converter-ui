import { defineConfig, transformWithEsbuild } from 'vite'
import react from '@vitejs/plugin-react'
import federation from '@originjs/vite-plugin-federation'
import tsconfigPaths from 'vite-tsconfig-paths'
import * as dotenv from 'dotenv';
import * as dotenvExpand from 'dotenv-expand';

dotenvExpand.expand(dotenv.config())

const jsToJsx = () => {
  return {
    name: "treat-js-files-as-jsx",
    async transform(code:string, id:string) {
      if (!id.match(/src\/.*\.js$/)) return null;

      // Use the exposed transform from vite, instead of directly
      // transforming with esbuild
      return transformWithEsbuild(code, id, {
        loader: "jsx",
        jsx: "automatic",
      });
    },
  };
};

export default defineConfig({
  plugins: [
    react(),
    jsToJsx(),
    tsconfigPaths(),
    federation({
      name: "remote_app",
      filename: "remoteEntry.js",
      // expose your module. This should be the main component of your project, 
      // not the one having <React.StrictMode> but the one with your actual logic
      // so exposing App.tsx not main.tsx
      exposes: {
         './PdfAccessibleHtml': './src/App' // left side name of module to expose can be your choice, right side is the path to the component
      },
      shared: ['react','react-dom']
    })
  ],
  base: process.env.NODE_ENV == 'production' ? process.env.VITE_BASE_URL_PROD : process.env.VITE_BASE_URL,
  build: {
    rollupOptions: {
      external:[],
    },
    modulePreload: false,
    target: 'esnext',
    minify: false,
    cssCodeSplit: false
  }
})
