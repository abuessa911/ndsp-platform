import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  root: new URL(".", import.meta.url).pathname,
  base: "/login/",
  plugins: [react()],
  build: {
    outDir: "../ui-dist",
    emptyOutDir: true,
    sourcemap: false
  }
});
