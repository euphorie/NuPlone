(function($) {
    function renumberElement(el, attr, i) {
        var $el = $(el),
            buf = $el.attr(attr);
        if (buf) {
            $el.attr(attr, buf.replace(/[0-9]+/, i));
        }
    }
 
    $(".multiWidget > button.add").live("click", function() {
	var $button = $(this),
	    url = $button.val(),
            index = $button.siblings("fieldset").length,
            $fragment;
	$.get(url, function(data, status) {
            $fragment=$(data);
            $("label, :input", $fragment).each(function() {
                renumberElement(this, "for", index);
                renumberElement(this, "id", index);
                renumberElement(this, "name", index);
            });
            $button.before($fragment);
	});
    });
})(jQuery);
