// ////////////////////////////////////////////////
// Required taskes
// gulp build
// // /////////////////////////////////////////////

var gulp = require('gulp');
var uglify = require('gulp-uglify');
var concat = require('gulp-concat');





// ////////////////////////////////////////////////
// Concat CSS 
// ///////////////////////////////////////////////

gulp.task('concatcss', function() {
    return gulp.src([
  		"assets/vendor/bootstrap/dist/css/bootstrap.min.css",
  		"assets/vendor/slick-carousel/slick/slick.css",
  		"assets/vendor/fancybox/dist/jquery.fancybox.min.css",
  		"assets/vendor/animate.css/animate.min.css"
    ])
      .pipe(concat('bundle.css'))
      .pipe(gulp.dest('assets/css/'));
});


// ////////////////////////////////////////////////
// Concat Scripts
// ///////////////////////////////////////////////

gulp.task('concatjs', function() {
  return gulp.src([		
		"assets/vendor/jquery/dist/jquery.min.js",
		"assets/vendor/popper.js/dist/popper.min.js",
		"assets/vendor/bootstrap/dist/js/bootstrap.min.js",
		"assets/vendor/slick-carousel/slick/slick.min.js",
		"assets/vendor/fancybox/dist/jquery.fancybox.min.js",
		"assets/vendor/imagesloaded/imagesloaded.pkgd.min.js",
		"assets/vendor/isotope/dist/isotope.pkgd.min.js",
		"assets/vendor/parallax.js/parallax.min.js",
		"assets/vendor/wow/dist/wow.min.js",
		"assets/vendor/vide/dist/jquery.vide.min.js",
		"assets/vendor/typed.js/lib/typed.min.js",
		"assets/vendor/appear-master/dist/appear.min.js",
		"assets/vendor/jquery.countdown/dist/jquery.countdown.min.js",
		"assets/js/smoothscroll.js"
  ])
    .pipe(concat('bundle.js'))
    .pipe(uglify())
    .pipe(gulp.dest('assets/js/'));
});









