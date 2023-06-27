const { src, dest, watch, parallel } = require('gulp');
const sass = require('gulp-sass')(require('sass'));
const autoprefixer = require('autoprefixer');
const postcss = require('gulp-postcss')
const sourcemaps = require('gulp-sourcemaps')
const cssnano = require('cssnano');
const concat = require('gulp-concat');
const terser = require('gulp-terser-js');
const rename = require('gulp-rename');
// const imagemin = require('gulp-imagemin');
const cache = require('gulp-cache');
const webp = require('gulp-webp');
const avif = require('gulp-avif');

const paths = {
    scss: 'src/scss/**/*.scss',
    js: 'src/js/**/*.js',
    imagenes_jpg: 'src/img/**/*.jpg',
    imagenes_svg: 'src/img/**/*.svg'
};


function compile_css() {
    return src(paths.scss)
        .pipe(rename(path=>
            {
                const match = /\/scss\/[a-z_]+\//.exec(path.dirname);
                this.appName = match[0];
            }    
        ))
        .pipe(sourcemaps.init())
        .pipe(sass())
        .pipe(postcss([autoprefixer(), cssnano()]))
        .pipe(sourcemaps.write('.'))
        .pipe(dest(`./${this.appName}/static/${this.appName}/css`));
}

function export_js() {
    return src(paths.js)
      .pipe(sourcemaps.init())
      .pipe(concat('app.js'))
      .pipe(terser())
      .pipe(sourcemaps.write('.'))
      .pipe(dest('./public/build/js'))
}

function imagenes(done) {
    src(paths.imagenes_jpg)
        .pipe(cache(imagemin({ optimizationLevel: 3 })))
        .pipe(dest('./public/build/img'));
    src(paths.imagenes_svg)
        .pipe(cache(imagemin({optimizationLevel:3})))
        .pipe(dest("./public/build/img"));
    done();
}

function versionWebp(done) {
    const options = 
    {
        quality:80
    }
    src(paths.imagenes_jpg)
        .pipe(webp(options))
        .pipe(dest('./public/build/img'));
    done();
}

function versionAvif (done)
{
    const options = {
        quality:80
    }
    src(paths.imagenes_jpg)
        .pipe(avif(options))
        .pipe(dest("./public/build/img"));
    done();
}


function dev() {
    watch(paths.scss, compile_css);
    watch(paths.js, export_js);
}

exports.compile_css = compile_css;
exports.export_js = export_js;
exports.dev = dev;
exports.improve_images = parallel(imagenes,versionWebp,versionAvif); 