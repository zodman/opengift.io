var gulp = require('gulp');
var watch = require('gulp-watch');
var shell = require('gulp-shell');

var root_path = process.cwd();
var get_path = function(evt) {
    return evt.path.replace(root_path + '/', '')
        .replace('.robot','')
        .replace(/\//g,'.')
        .replace('.__init__','')
};


gulp.task('default', function() {
    //empty default task
});


gulp.task('watch', function () {
    gulp.watch('tests/**/*.robot').on('change', function(evt) {
        process.stdout.write('file changed\n');
        process.stdout.write('running tests\n');
        return gulp.src('').pipe(
            shell(['pybot -d reports --suite ' + get_path(evt) + ' tests'],
                {
                    ignoreErrors: true,
                    errorMessage: 'tests failed'
                })
        )

    });
});
//pybot --suite tests.bugs.directory_test tests
