import registry from "@patternslib/patternslib/src/core/registry";

// Pattern imports
import "@patternslib/pat-redactor/src/pat-redactor";
import "redactor/src/redactor.css";

// Jquery UI
// Includes: core.js, widget.js, mouse.js, position.js, draggable.js, droppable.js, resizable.js, selectable.js, sortable.js, accordion.js, autocomplete.js, button.js, datepicker.js, dialog.js, menu.js, progressbar.js, selectmenu.js, slider.js, spinner.js, tabs.js, tooltip.js
import "jquery-ui-dist/jquery-ui";
import "jquery-ui-dist/jquery-ui.css";
import "jquery-ui-dist/jquery-ui.theme.css";

// Other dependencies
import "./resources/scripts/behaviour";
import "./resources/scripts/editlink";
import "./resources/scripts/ordering";
import "./resources/scripts/z3cform";

registry.init();
