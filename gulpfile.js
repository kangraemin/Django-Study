const gulp = require("gulp");

const css = () => {
  const postCss = require("gulp-postcss");
  const sass = require("gulp-sass");
  const minify = require("gulp-csso");
  sass.compiler = require("node-sass");
  return gulp
    .src("assets/scss/styles.scss") // scss source file
    .pipe(sass().on("error", sass.logError)) // when error case and change scss file to css file 
    .pipe(postCss([ // It understand postcss ( tailwindcss / autoprefixer ) it transform tailwind rule like @tailwind ~ somthing to css ( browser only understand normal css )
      require("tailwindcss"),
      require("autoprefixer")
    ]))
    .pipe(minify()) // And minify it 
    .pipe(gulp.dest("static/css")); // and store result at static/css 
};

exports.default = css;