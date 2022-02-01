// postcss.config.js

const path = require("path");

module.exports = (ctx) => ({
  plugins: [
    require("tailwindcss")(path.resolve(__dirname, "tailwind.config.js")),
    require("autoprefixer"),
    process.env.FLASK_ENV === "production" &&
      require("@fullhuman/postcss-purgecss")({
        content: [path.resolve(__dirname, "app/templates/*.html")],
        defaultExtractor: (content) => content.match(/[\w-/:]+(?<!:)/g) || [],
      }),
  ],
});
