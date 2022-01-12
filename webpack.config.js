process.traceDeprecation = true;
const fs = require("fs");
const path = require("path");
const patternslib_config = require("@patternslib/patternslib/webpack/webpack.config.js");

module.exports = async (env, argv) => {
    let config = {
        entry: {
            "oira.cms.min": path.resolve(__dirname, "bundle-config.js"),
            "bundle-polyfills.min": path.resolve(__dirname, "node_modules/@patternslib/patternslib/src/polyfills.js"), // prettier-ignore
        },
    };

    config = patternslib_config(env, argv, config);
    config.output.path = path.resolve(__dirname, "bundles");

    if (process.env.NODE_ENV === "development") {
        // Make sure we're using only one patternslib instance.
        config.resolve.alias["@patternslib/patternslib"] = path.resolve(
            __dirname,
            "node_modules/@patternslib/patternslib"
        );
        // Make sure we're using only one jquery instance.
        config.resolve.alias["jquery"] = path.resolve(
            __dirname,
            "node_modules/jquery"
        );
    }

    return config;
};
