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
            $buttons = $fieldset.children("button.remove"),
            i;
        $counter = $(":input:first", $fieldset).val($fieldsets.length);

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

})(jQuery);

// Putting this in $(document).ready gives lots of "tinyMCE is not defined" errors
$(window).load(function() {
    tinyMCE.init({mode: "none",
		  theme: "dummy",
		  fix_list_elements: true,
		  entity_encoding: "raw",
		  content_editable: true
		 });
    $("textarea.rich").each(function() {
	var $textarea = $(this),
	    id = $textarea.attr("id"),
	    $div = $("<div/>");
	    
	$div
	    .attr("id", id)
	    .addClass("rich input")
	    .data("z3cform.name", $textarea.attr("name"))
	    .append($($textarea.val()));
	$textarea.replaceWith($div);

	tinyMCE.execCommand("mceAddControl", false, id);
    });
});
