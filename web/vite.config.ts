import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";

export default defineConfig({
  // Use BASE path from env for GitHub Pages (e.g., /ai-recipe-helper/). Defaults to '/'.
  base: process.env.VITE_BASE || "/",
  plugins: [vue()],
  server: { port: 5173 }
});
