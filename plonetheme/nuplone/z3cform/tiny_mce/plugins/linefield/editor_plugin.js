(function() {
	var active = false;

	tinymce.create('tinymce.plugins.LineFieldPlugin', {
		init : function(ed, url) {
			// Add a node change handler, selects the button in the UI when a image is selected

			function go(ed) {
				if (active)
					return;
				active = true;

				if (typeof ed.settings.on_activate=="function") 
					ed.settings.on_activate(ed);
			}

			ed.onClick.add(go);
			ed.onActivate.add(go);

			ed.onDeactivate.add(function() {
				active = false;
			});

			ed.onKeyPress.add(function(ed, e) {
				var ob = ed.dom.get(ed.id);
				if (e.keyCode==13 && ed.dom.hasClass(ob, "lineField")) {
					tinymce.dom.Event.prevent(e);
					return false;
				}
			});
		},

		createControl : function(n, cm) {
			return null;
		},

		getInfo : function() {
			return {
				longname : 'LineField plugin',
				author : 'Some author',
				authorurl : 'http://tinymce.moxiecode.com',
				infourl : 'http://wiki.moxiecode.com/index.php/TinyMCE:Plugins/linefield',
				version : "0.1"
			};
		}
	});

	// Register plugin
	tinymce.PluginManager.add('linefield', tinymce.plugins.LineFieldPlugin);
})();
