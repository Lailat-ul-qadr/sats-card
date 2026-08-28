/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,jsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Core dark surfaces
        bg: "#07080C",
        surface: "#12141C",
        elevated: "#1A1D27",
        line: "#23262F",

        // Text
        ink: "#F3F4F7",
        "ink-soft": "#A7ADBB",
        "ink-muted": "#6E7383",

        // Legacy tokens kept for compatibility, remapped to new theme
        cream: "#07080C",
        clay: "#C8FF4D",
        muted: {
          green: "#34D399",
          brown: "#A7ADBB",
          slate: "#A7ADBB",
        },
        accent: {
          gold: "#FFB020",
          rust: "#FF5D5D",
        },

        // Bold "lightning" accents
        amber: {
          DEFAULT: "#FFB020",
          soft: "#FFD37A",
          dim: "#8A5E12",
        },
        lime: {
          DEFAULT: "#C8FF4D",
          soft: "#E1FFA0",
          dim: "#6B8A1F",
        },
        success: "#34D399",
        danger: "#FF5D5D",
        warning: "#FFC53D",
        info: "#5CC9F5",
      },
      fontFamily: {
        display: ["'Space Grotesk'", "sans-serif"],
        sans: ["Manrope", "sans-serif"],
        serif: ["'Space Grotesk'", "sans-serif"],
        mono: ["'JetBrains Mono'", "monospace"],
      },
      boxShadow: {
        "glow-amber": "0 0 50px -5px rgba(255,176,32,0.45)",
        "glow-amber-sm": "0 0 24px -6px rgba(255,176,32,0.5)",
        "glow-lime": "0 0 50px -5px rgba(200,255,77,0.35)",
        card: "0 30px 80px -25px rgba(0,0,0,0.7)",
        "inner-line": "inset 0 0 0 1px rgba(255,255,255,0.06)",
      },
      backgroundImage: {
        "grid-lines":
          "linear-gradient(rgba(255,255,255,0.045) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.045) 1px, transparent 1px)",
        "amber-lime": "linear-gradient(135deg, #FFB020 0%, #C8FF4D 100%)",
        "amber-lime-soft": "linear-gradient(135deg, rgba(255,176,32,0.15) 0%, rgba(200,255,77,0.12) 100%)",
      },
      backgroundSize: {
        grid: "40px 40px",
      },
      animation: {
        fadeIn: "fadeIn 0.6s ease-in-out",
        slideUp: "slideUp 0.5s ease-out",
        pulseSoft: "pulseSoft 2.4s cubic-bezier(0.4, 0, 0.6, 1) infinite",
        glowPulse: "glowPulse 3s ease-in-out infinite",
        bolt: "bolt 1.6s ease-in-out infinite",
        marquee: "marquee 22s linear infinite",
        float: "float 5s ease-in-out infinite",
      },
      keyframes: {
        fadeIn: {
          "0%": { opacity: "0" },
          "100%": { opacity: "1" },
        },
        slideUp: {
          "0%": { transform: "translateY(20px)", opacity: "0" },
          "100%": { transform: "translateY(0)", opacity: "1" },
        },
        pulseSoft: {
          "0%, 100%": { opacity: "1" },
          "50%": { opacity: "0.5" },
        },
        glowPulse: {
          "0%, 100%": { boxShadow: "0 0 30px -8px rgba(255,176,32,0.4)" },
          "50%": { boxShadow: "0 0 55px -6px rgba(200,255,77,0.45)" },
        },
        bolt: {
          "0%, 100%": { opacity: "1", filter: "drop-shadow(0 0 6px rgba(255,176,32,0.7))" },
          "50%": { opacity: "0.6", filter: "drop-shadow(0 0 2px rgba(255,176,32,0.3))" },
        },
        marquee: {
          "0%": { transform: "translateX(0)" },
          "100%": { transform: "translateX(-50%)" },
        },
        float: {
          "0%, 100%": { transform: "translateY(0px)" },
          "50%": { transform: "translateY(-8px)" },
        },
      },
    },
  },
  plugins: [],
}
