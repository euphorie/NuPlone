==================
Javascript library
==================

The markup patterns are implemented by a javascript library. This library has
a few dependencies:

 * `jQuery <http://jquery.com/>`_, version 1.4 or later
 * `jQuery UI <http://jqueryui.com/>`_'s  autocomplete plugin, version 1.8 or later.
 * `jQuery Tools <http://flowplayer.org/tools/index.html>`_ overlay plugin


Initialisation
==============

Once the markup library has been loaded it sets up the behaviour for the
current DOM tree. Where possible `jQuery live events <http://api.jquery.com/live/>`_
are used so elements that added to the DOM at a later point in time are
automatically processed. Since this is not possible for all behaviours it
is important to call the `:obj:mapap.initContent` method when adding new DOM
elements.

Markup transformations
----------------------

In addition to configuring behaviour a few changes are also made to the DOM
to improve support for older browsers.

Currently only one transformation is done: since very few browsers can fully
style ``legend`` tags they are are automatically converted to ``<p
class="question>``, which all browsers do handle correctly.


API reference
=============

.. js:data:: mapal

   This is a global object which contains the state and all functions used
   by the markup pattern library.


.. js:function:: mapal.initContent(node)

   :param node: Root node for newly added content.

   This function must be called when new content is added to the DOM tree.
   It will perform any necessary markup transformations and setup behaviour
   for the new elements. This function is automatically called for the
   document when the markup pattern library is first loaded.


.. js:function:: mapal.registerWidthClass(class, minimum, maximum)

   :param string class: CSS class to register
   :param int minimum: minimum window width for this class
   :param int maximum: maximum window width for this class

   It can be useful to change the layout of a page depending on the width
   of the browser window. This method faciliates that by automatically
   adding a class to the ``body`` element to indicate the current width.
   If `minimum` or `maximum` is `null` there relevant limit is not checked.

   .. code-block:: javascript

      mapal.registerWidthClass("narrow", 0, 780);
      mapal.registerWidthClass("medium", 0, 1109);
      mapal.registerWidthClass("wide", 1110, null);


.. js:function:: mapal.renumber(container[, selector])

   :param jQuery-instance Parent of all nodes to be renumbered
   :param string selector: CSS selector for nodes to renumber. Defaults to ``fieldset,tr,dd``

   When adding or removing new elements to it may be necessary to adjust the
   number used in ``for``, ``id`` and ``name`` attributes to prevent conflicts.
   This is a very common requirement for forms where items can be a added to or
   removed form a list. The ``renumber`` function find all elements matching
   the given selector, and make sure the ``for``, ``id`` and ``name``
   attributes used inside them use the same index number.

   For example suppose a you added a new fieldset to a form and the DOM now
   looks like this:

   .. code-block:: html

      <form id="library">
        <fieldset>
          <label id="titleField1">Title <input name="title.1"/> </label>
          <label id="authorField1">Author <input name="title.1"/> </label>
        </fieldset>
        <fieldset>
          <label id="titleField1">Title <input name="title.1"/> </label>
          <label id="authorField1">Author <input name="title.1"/> </label>
        </fieldset>
      </form>

   There are now duplicate ids in the DOM as well as multiple input elements
   with the same name. If you now call ``mapal.renumber($("#library"))`` it
   will update the DOM to look like this:

   .. code-block:: html

      <form id="library">
        <fieldset>
          <label id="titleField1">Title <input name="title.1"/> </label>
          <label id="authorField1">Author <input name="title.1"/> </label>
        </fieldset>
        <fieldset>
          <label id="titleField2">Title <input name="title.2"/> </label>
          <label id="authorField2">Author <input name="title.2"/> </label>
        </fieldset>
      </form>


.. js:function:: mapal.hasContent(node)

   :param jQuery-instance node: node to check

   This method checks if a node has any user visible content. It ignores all
   whitespace generating elements and only checks for text and media content.

