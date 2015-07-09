// Easy ordering support for folders
$(document).ready(function() {
    $(".sortable").sortable({containment: "parent" });
});
$(".sortable").on("sortstop", function(e, ui) {
    var order = $.map($(".sortable > *"), function(e) { return e.id;} );
    $.post(plone.context_url+"/@@update-order", {order: order});
});
