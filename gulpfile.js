/**
  Для запуска необходимо установить node.js http://nodejs.org
  после этого, запустить в папке проекта команду npm install (поставятся все зависимости)
  правда не помню нужно ли устанавливать gulp глобально, если он это напишет выполнить (npm install gulp -g)
  
  Для запуска сборки js файлов из исходников, необходимо выполнить команду gulp build_js ( она выполнится единожды )
    каждый раз после изменения файлов в src нужно будет выполнять команду
  Для того, что бы происходило автоматическое собирание файлов при изменении необходимо выполнить gulp watch
*/

const gulp = require('gulp');
const minify = require('gulp-minify');
const concat = require('gulp-concat');
const imagemin = require('gulp-imagemin');

const js_src = [
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

gulp.task('watch', ['build_js'], function () {
  gulp.watch(js_src, ['build_js']);
});