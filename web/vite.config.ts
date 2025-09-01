import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";

export default defineConfig({
  // Use BASE path from env for GitHub Pages (e.g., /ai-recipe-helper/). Defaults to '/'.
  base: process.env.VITE_BASE || "/",
  plugins: [vue()],
  // Expose dev server on LAN so phones on the same Wi‑Fi can connect.
  // - host: true binds to 0.0.0.0 instead of localhost (::1)
  // - strictPort: false lets Vite pick the next free port if the default is taken
  // - hmr: use the same host/port as the page URL (works across devices)
  server: {
    host: true,
    port: 5173,
    strictPort: false,
    hmr: { overlay: true }
  }
});
