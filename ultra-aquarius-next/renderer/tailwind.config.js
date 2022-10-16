const colors = require("tailwindcss/colors");

module.exports = {
  content: [
    "./renderer/pages/**/*.{js,ts,jsx,tsx}",
    "./renderer/layouts/**/*.{js,ts,jsx,tsx}",
    "./renderer/components/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    colors: {
      // use colors only specified
      white: colors.white,
      gray: colors.gray,
      red: colors.red,
      cyan: colors.cyan,
      transparent: colors.transparent,
    },
    extend: {
      animation: {
        "loop-right": "loopRight 4s linear infinite",
      },
      keyframes: {
        loopRight: {
          "0%": {
            left: "0%",
            transform: "TranslateX(-100%)",
          },
          "100%": {
            left: "100%",
            transform: "TranslateX(0%)",
          },
        },
      },
    },
  },
  plugins: [],
};
