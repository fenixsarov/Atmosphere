/*
  Для запуска необходимо установить node.js http://nodejs.org
  после этого, запустить в папке проекта команду npm install (поставятся все зависимости)
  правда не помню нужно ли устанавливать gulp глобально, если он это напишет выполнить (npm install gulp -g)
  
  После всего этого, поисле изменения js кода в static/javascripts/src выполнить команду gulp compress 
  Compress это задача, описаная в файле gulpfile.js
*/

var gulp = require('gulp');
var minify = require('gulp-minify');
var concat = require('gulp-concat');
var imagemin = require('gulp-imagemin');

var js_src = [
  "static/javascripts/src/reserv_widget.js",
  "static/javascripts/src/main.js"
];
gulp.task('build_js', function () {
  return gulp.src(js_src)
    .pipe(concat('main.js'))
    .pipe(minify({
      'noSource': true,
      'ext': {
        'min': ".min.js"
      }
    }))
    .pipe(gulp.dest('static/javascripts'));
});

gulp.task('imagemin', function () {
  return gulp.src('static/images/graduations/*.jpg')
    .pipe(imagemin({
      verbose: true
    }))
    .pipe(gulp.dest('static/images/graduations/compressed'));
});

gulp.task('watch', function () {
  gulp.watch(js_src, ['build_js']);
});