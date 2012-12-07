function reset() {
    $("#external form")[0].reset();
    $("em.message.warning").remove();
}

function hide() {
    var topDoc = window.frameElement.ownerDocument;
    $("#linkFrame", topDoc).hide();
}


function show(el) {
    var topDoc = window.frameElement.ownerDocument;

    if (el===undefined) {
        reset();
    } else {
        var topWindow = topDoc.defaultView!==undefined ? topDoc.defaultView : topDoc.parentWindow;
        topWindow.getSelection().selectAllChildren(el);
        $("input[name=form.widgets.new_window:list]").get(0).checked = (el.target==="_blank");
        $("input[name=form.widgets.URL]").val(el.href);
        $("input[name=form.widgets.title]").val(el.title);
    }

    $("#linkFrame", topDoc).show();
}


function removeLink() {
    var topDoc = window.frameElement.ownerDocument,
        topWindow = topDoc.defaultView!==undefined ? topDoc.defaultView : topDoc.parentWindow,
        selection = rangy.getSelection(topWindow),
        range, link, found;

    if (selection.rangeCount===0 || selection.isCollapsed)
        return;
    link = selection.anchorNode;
    found=false;
    while (link!==null && !found) {
        if (link.nodeType===Node.ELEMENT_NODE && link.tagName==="A")
            found=true;
        else
          link=link.parentNode;
    }
    if (!found)
        return;

    var $link = $(link);
    $link.replaceWith($link.contents());
}


function InsertURL(url, title, newwindow) {
    var topDoc = window.frameElement.ownerDocument,
        topWindow = topDoc.defaultView!==undefined ? topDoc.defaultView : topDoc.parentWindow,
        selection = rangy.getSelection(topWindow),
        range, link, found;

    if (selection.rangeCount===0)
        selection.addRange(range=rangy.createRange(topDoc));
    else
        range = selection.getRangeAt(0);

    if (range.collapsed || !range.canSurroundContents()) {
          link = topDoc.createElement("A");
          link.appendChild(topDoc.createTextNode(title || url));
          range.insertNode(link);
    } else {
      // Try to find a parent link
        link = range.startContainer;
        found=false;
        while (link!==null && !found) {
            if (link.nodeType===Node.ELEMENT_NODE && link.tagName==="A")
                found=true;
            else
              link=link.parentNode;
        }
        if (!found) {
            link = topDoc.createElement("A");
            range.surroundContents(link);
        }
    }
    if (url.indexOf(":")===-1 && url[0]!=="/")
        url = "http://"+url;
    link.href = url;
    link.target = newwindow ? "_blank" : "";
    link.title = title || "";
}

$("button.cancel").live("click", hide);

$("button.save").live("click", function() {
    var form = this.form,
        link = form["form.widgets.URL"].value,
        title = form["form.widgets.title"].value,
        newwindow = form["form.widgets.new_window:list"].checked;
    InsertURL(link, title, newwindow);
    hide();
});
