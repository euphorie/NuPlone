(function($) {
    function renumberElement(el, attr, i) {
        var $el = $(el),
            buf = $el.attr(attr);
        if (buf) {
            $el.attr(attr, buf.replace(/[0-9]+/, i));
        }
    }

    function renumber($fieldset) {
        var $fieldsets = $fieldset.children("fieldset"),
            i;
        $(":input:first", $fieldset).val($fieldsets.length);

        for (i=0; i<$fieldsets.length; i++) {
            $("label, :input", $fieldsets[i]).each(function() {
                renumberElement(this, "for", i);
                renumberElement(this, "id", i);
                renumberElement(this, "name", i);
            });
        }
    }

 
    $(".multiWidget > button.add").live("click", function() {
        var $button = $(this),
            url = $button.val();
        $.get(url, function(data, status) {
            var $fragment=$(data);
            $button.before($fragment);
            renumber($button.parent());
        });
    });

    $(".multiWidget > fieldset > button.remove").live("click", function() {
        var $button = $(this),
            $fieldset = $button.parent(),
            $root = $fieldset.parent();

        $fieldset.remove();
        renumber($root);
    });

    $(window).load(function() {
        function onTinyActivate(ed) {
            var $controls = $("#tinyControls");
            if (!$controls.length) {
                var $wrapper = $("#frameWrapper");
                if (!$wrapper.length) {
                    $wrapper=$("<p/>").attr("id", "frameWrapper").appendTo(document.body);
                }
                $("<object/>")
                    .attr("id", "tinyControls")
                    .attr("type", "text/html")
                    .attr("data", plone.portal_url+"/@@tiny-controls")
                    .css("position", "absolute")
                    .css("top", "0px")
                    .css("left", "0px")
                    .css("z-index", "100")
                    .appendTo($wrapper);
            }
        }

        tinyMCE.init({mode: "none",
                      theme: "dummy",
                      plugins: "linefield",
                      element_format: "xhtml",
                      fix_list_elements: true,
                      fix_table_elements: true,
                      entity_encoding: "raw",
                      content_editable: true,
                      forced_root_block: null,
                      on_activate: onTinyActivate
                     });

        $("textarea.rich").each(function() {
            var $textarea = $(this),
                id = $textarea.attr("id"),
                $div = $("<div/>");
                
            $div
                .attr("id", id)
                .addClass("rich input")
                .data("z3cform.name", $textarea.attr("name"))
                .html($textarea.val());
            $textarea.replaceWith($div);

            tinyMCE.execCommand("mceAddControl", false, id);
        });
    });

    $("form").live("submit", function() {
        $("div.rich.input", this).each(function() {
            var $field = $(this),
                id = $field.attr("id"),
                value = tinyMCE.get(id).getContent(),
                name = $field.data("z3cform.name");
            if (name) {
                $("<input/>")
                    .attr("type", "hidden")
                    .attr("name", name)
                    .val(value)
                    .insertBefore($field);
            }
        });
        return true;
    });
})(jQuery);

