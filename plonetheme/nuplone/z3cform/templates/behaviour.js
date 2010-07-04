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
            var $wrapper = $("#frameWrapper"),
                $controls;

            if (!$wrapper.length) {
                $wrapper=$("<p/>").attr("id", "frameWrapper").appendTo(document.body);
            }

            function triggerActive() {
                try {
                    $("#tinyControls").get(0).contentWindow.activate(ed);
                } catch(e) {
                }
            }

            $controls = $("#tinyControls");
            if (!$controls.length) {
                $("<iframe/>")
                    .attr("id", "tinyControls")
                    .attr("src", plone.context_url+"/@@tiny-controls")
                    .css("position", "absolute")
                    .css("top", "0px")
                    .css("left", "0px")
                    .css("z-index", "1100")
                    .appendTo($wrapper)
                    .load(triggerActive);
            } else {
                triggerActive();
            }

            if (!$("body").hasClass("edit")) {
                $("body").addClass("edit");
            }

            $controls = $("#linkFrame");
            if (!$controls.length) {
                $("<iframe/>")
                    .attr("id", "linkFrame")
                    .attr("src", plone.context_url+"/@@edit-link")
                    .attr("frameborder", "0")
                    .css("z-index", "1100")
                    .css("height", "250px")
                    .css("width", "510px")
                    .css("margin-left", "-255px")
                    .css("left", "50%")
                    .css("position", "absolute")
                    .css("top", "70px")
                    .css("-webkit-box-shadow", "0 0 15px rgba(0,0,0,0.5)")
                    .css("-moz-box-shadow", "0 0 15px rgba(0,0,0,0.5)")
                    .css("box-shadow", "0 0 15px rgba(0,0,0,0.5)")
                    .css("display", "none")
                    .appendTo($wrapper);
            }
        }

	function onTinyDeactivate(ed) {
            try {
                $("#tinyControls").get(0).contentWindow.deactivate(ed);
            } catch(e) {
            }
	}

        function onTinySetup(ed) {
            ed.onDblClick.add(function(ed, e) {
                if (e.target.nodeName.toLowerCase()=="a") {
                    $("#linkFrame").get(0).contentWindow.show(e.target);
                }
            });

	    ed.onActivate.add(onTinyActivate);
	    ed.onDeactivate.add(onTinyDeactivate);
        }

        $(":input").live("focus", function() {
                tinymce.EditorManager._setActive(null);
                onTinyDeactivate();
        });

        tinyMCE.init({mode: "none",
                      theme: "dummy",
                      plugins: "linefield",
                      element_format: "xhtml",
                      fix_list_elements: true,
                      fix_table_elements: true,
                      entity_encoding: "raw",
                      content_editable: true,
                      forced_root_block: null,
                      setup: onTinySetup
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

        $(".rich:not(:input)").each(function() {
            var $el = $(this),
                $component = $el.closest(".richInput");

            if (!$component.length) {
                return;
            }

            function update() {
                if (mapal.hasContent($el)) {
                    $component.removeClass("empty");
                } else {
                    $component.addClass("empty");
                }
            }

            update();

            $el.bind("focus", function() {
                    $component.data("mapal.timer.rich", setInterval(update, 100));
                })
                .bind("blur", function() {
                    update();
                    clearInterval($component.data("mapal.timer.rich"));
                });
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

