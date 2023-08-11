const { src, dest, watch, parallel } = require('gulp');
const sass = require('gulp-sass')(require('sass'));
const autoprefixer = require('autoprefixer');
const postcss = require('gulp-postcss')
const sourcemaps = require('gulp-sourcemaps')
const cssnano = require('cssnano');
const terser = require('gulp-terser-js');
const rename = require('gulp-rename');
const imagemin = require('gulp-imagemin');
const cache = require('gulp-cache');
const webp = require('gulp-webp');
const avif = require('gulp-avif');
const webpack = require('webpack-stream');
const tap = require('gulp-tap');

const paths = {
    scss: 'src/scss/**/*.scss',
    js: 'src/js/**/*.js',
    images: 'src/img/**/*.{jpg,png}',
    images_svg: 'src/img/**/*.svg'
};


function compile_css() {
    return src(paths.scss)
        .pipe(sourcemaps.init())
        .pipe(sass())
        .pipe(postcss([autoprefixer(), cssnano()]))
        .pipe(sourcemaps.write('.'))
        .pipe(rename(path=>
            {
                const appName = path.dirname; // path.dirname returns the relative path to the first glob (**) specified in the src path. As scss folder childs are Django app names, we keep them in order to build the correct route. Example: If the path is ./src/scss/foo, path.dirname value is foo
                path.dirname += "/static/"+appName+"/css" // Follow Django's phylosophy of namespacing the static files through the app name
            }    
        ))
        .pipe(dest("./"));
}

function export_js() {
    return src(paths.js)
        .pipe(tap(file=> // As we are using webpack, the dirname is lost. And we also need to specify the app.js of each Django app, so we use gulp-tap to access individually each file passed through the pipeline
            {
                const match = /\/src\/js\/[a-z_]+/.exec(file.dirname);
                const appName = match[0].substring(7);
                const entry_route = './src/js/'+appName+'/app.js';
                webpack(
                {
                    mode:'production',
                    entry:entry_route
                })
                .pipe(sourcemaps.init())
                .pipe(terser())
                .pipe(sourcemaps.write('.'))
                .pipe(rename(path=>
                    {
                        path.dirname += appName+"/static/"+appName+"/js"
                    }
                ))
                .pipe(dest('./'))
            }
        ));
}

function images(done) {
    src(paths.images)
        .pipe(cache(imagemin({ optimizationLevel: 3 })))
        .pipe(rename(path=>
            {
                const appName = path.dirname;
                path.dirname += "/static/"+appName+"/img"
            }
        ))
        .pipe(dest('./'));
    src(paths.images_svg)
        .pipe(cache(imagemin({optimizationLevel:3})))
        .pipe(rename(path=>
            {
                const appName = path.dirname;
                path.dirname += "/static/"+appName+"/img"
            }
        ))
        .pipe(dest("./"));
    done();
}

function webpversion(done) {
    const options = 
    {
        quality:80
    }
    src(paths.images)
        .pipe(webp(options))
        .pipe(rename(path=>
            {
                const appName = path.dirname;
                path.dirname += "/static/"+appName+"/img"
            }
        ))
        .pipe(dest('./'));
    done();
}

function avifversion (done)
{
    const options = {
        quality:80
    }
    src(paths.images)
        .pipe(avif(options))
        .pipe(rename(path=>
            {
                const appName = path.dirname;
                path.dirname += "/static/"+appName+"/img"
            }
        ))
        .pipe(dest("./"));
    done();
}


function dev() {
    watch(paths.scss, compile_css);
    watch(paths.js, export_js);
}

exports.compile_css = compile_css;
exports.export_js = export_js;
exports.dev = dev;
exports.improve_images = parallel(images,webpversion,avifversion); 