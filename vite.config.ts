import react from "@vitejs/plugin-react";
import { defineConfig, transformWithEsbuild } from "vite";
import federation from '@originjs/vite-plugin-federation'
import * as dotenv from 'dotenv';
import * as dotenvExpand from 'dotenv-expand';
import tsconfigPaths from 'vite-tsconfig-paths'

dotenvExpand.expand(dotenv.config())

/*
  custom plugin to transform js to jsx
*/
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
  build: {
    rollupOptions: {
      external: [],
    },
    modulePreload: false,
    target: 'esnext',
    minify: false,
    cssCodeSplit: false
  },
  plugins: [react(), jsToJsx(), tsconfigPaths(),federation({
    name: "common",
    filename: "remoteEntry.js",
    exposes: {
      './PdfAccessibleHtml': './src/pages/',
    },
    shared: ['react','react-dom']
  })],
  base: process.env.NODE_ENV == 'production' ? process.env.VITE_BASE_URL_PROD : process.env.VITE_BASE_URL,
  server: {
    host: "localhost",
    port: 4173,
  },
});