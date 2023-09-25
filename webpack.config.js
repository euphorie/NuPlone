process.traceDeprecation = true;
const mf_config = require("@patternslib/dev/webpack/webpack.mf");
const package_json = require("./package.json");
const package_json_patternslib = require("@patternslib/patternslib/package.json");
const path = require("path");
const webpack_config =
    require("@patternslib/dev/webpack/webpack.config").config;

module.exports = () => {
    let config = {
        entry: {
            "oira.cms.min": path.resolve(__dirname, "index.js"),
        },
    };

    config = webpack_config({
        config: config,
        package_json: package_json,
    });
    config.output.path = path.resolve(
        __dirname,
        "plonetheme/nuplone/static/bundle",
    );

    config.plugins.push(
        mf_config({
            name: package_json.name,
            remote_entry: config.entry["bundle.min"],
            dependencies: {
                ...package_json_patternslib.dependencies,
                ...package_json.dependencies,
            },
        }),
    );

    if (process.env.NODE_ENV === "development") {
        config.devServer.static.directory = __dirname;
    }

    return config;
};
