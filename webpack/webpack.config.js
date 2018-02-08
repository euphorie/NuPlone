const merge = require('webpack-merge');
const path = require('path');
const UglifyJsPlugin = require('webpack-uglify-js-plugin');

var baseConfig = require('./extra.config.js');


module.exports = merge(baseConfig, {
    entry: {
        "oira.cms": path.resolve(__dirname, "../bundle-config.js"),
        "oira.cms.min": path.resolve(__dirname, "../bundle-config.js"),
        "bundle": path.resolve(__dirname, "../bundle-config.js"),
        "bundle.min": path.resolve(__dirname, "../bundle-config.js")
    },
    output: {
        filename: "[name].js",
        path: path.resolve(__dirname, '../bundles')
    },


    plugins: [
        new UglifyJsPlugin({
            cacheFolder: path.resolve(__dirname, '../cache/'),
            debug: true,
            include: /\.min\.js$/,
            minimize: true,
            sourceMap: true,
            output: {
              comments: false
            },
            compressor: {
              warnings: false
            }
        }),
    ],
});


