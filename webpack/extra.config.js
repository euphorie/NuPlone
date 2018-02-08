const merge = require('webpack-merge');
const path = require('path');
const UglifyJsPlugin = require('webpack-uglify-js-plugin');

var baseConfig = require('../node_modules/patternslib/webpack/base.config.js');


module.exports = merge(baseConfig, {
    resolve: {
        // This line is important to supply the patternslib source files
        modules: [
                  path.resolve(__dirname, '../node_modules/patternslib/src'),
                  path.resolve(__dirname, '../src'),
                  'node_modules'
        ],
        alias: {
            "moment-locale-de": "moment/locale/de",

            "redactor$": "redactor/redactor",
            "redactor-alignment": "redactor/plugins/alignment/alignment",
            "redactor-clips": "redactor/plugins/clips/clips",
            "redactor-codemirror": "redactor/plugins/codemirror",
            "redactor-counter": "redactor/plugins/definedlinks",
            "redactor-definedlinks": "redactor/plugins/codemirror",
            "redactor-filemanager": "redactor/plugins/filemanager",
            "redactor-fullscreen": "redactor/plugins/fullscreen",
            "redactor-imagemanager": "redactor/plugins/imagemanager",
            "redactor-inlinestyle": "redactor/plugins/inlinestyle",
            "redactor-limiter": "redactor/plugins/limiter",
            "redactor-properties": "redactor/plugins/properties",
            "redactor-bufferbuttons": "redactor/plugins/bufferbuttons",
            "redactor-romanlisting": "redactor/plugins/romanlisting",
            "redactor-source": "redactor/plugins/source",
            "redactor-table": "redactor/plugins/table",
            "redactor-textdirection": "redactor/plugins/textdirection",
            "redactor-textexpander": "redactor/plugins/codemirror",
            "redactor-video": "redactor/plugins/video",
            "pat-content-mirror": "pat-content-mirror/src/pat-content-mirror",
            "pat-redactor$": "pat-redactor/src/pat-redactor",
            "pat-pluggable": "core/pluggable",
            "jquery.ui":  "nuplone_components/jquery-ui",
            "nuplone-behaviour":  "nuplone_components/behaviour",
            "nuplone-editlink":   "nuplone_components/editlink",
            "nuplone-ordering":   "nuplone_components/ordering",
            "nuplone-z3cform":    "nuplone_components/z3cform",
            "nuplone-css-browser-selector":  "nuplone_components/css_browser_selector"

        }

    }

});
