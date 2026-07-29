import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./app/**/*.{ts,tsx}",
    "./components/**/*.{ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        surface: {
          50: "#f6f7f9",
          100: "#e2e5ec",
          200: "#c5cad6",
          300: "#a2a9bc",
          400: "#7d869e",
          500: "#606a83",
          600: "#4b5368",
          700: "#3d4355",
          800: "#2d3240",
          900: "#1a1d26",
        },
        accent: {
          DEFAULT: "#4f8af7",
          hover: "#3a7af5",
          muted: "#7aa8fa",
        },
        success: "#48bb78",
        warning: "#ecc94b",
        danger: "#e53e3e",
        critical: "#c53030",
      },
      fontFamily: {
        mono: ["JetBrains Mono", "Fira Code", "monospace"],
        sans: ["Inter", "system-ui", "sans-serif"],
      },
    },
  },
  plugins: [],
};

export default config;
