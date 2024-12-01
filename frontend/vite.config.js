import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// https://vitejs.dev/config/
export default defineConfig({
  server: {
    proxy: {
      "/api": {
        target: "http://0.0.0.0:8000", // 後端服務的實際地址
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ""), // 去掉 `/api` 前綴 後端不用care
      },
    },
  },
  plugins: [react()],
});
