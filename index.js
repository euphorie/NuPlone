// Webpack entry point for module federation.
import "@patternslib/dev/webpack/module_federation";
// The next import needs to be kept with brackets, otherwise we get this error:
// "Shared module is not available for eager consumption."
import("./bundle-config");

// Register Bootstrap and jQuery gloablly
async function register_global_libraries() {
    // Register jQuery globally
    const jquery = (await import("jquery")).default;
    window.jQuery = jquery;
    window.$ = jquery;
}
register_global_libraries();
