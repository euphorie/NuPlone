/**
 * $Id: editor_template_src.js 920 2008-09-09 14:05:33Z spocke $
 *
 * This file is meant to showcase how to create a simple theme. The advanced
 * theme is more suitable for production use.
 *
 * @author Moxiecode
 * @copyright Copyright © 2004-2008, Moxiecode Systems AB, All rights reserved.
 */

(function() {
	var DOM = tinymce.DOM;

	tinymce.create('tinymce.themes.DummyTheme', {
		init : function(ed, url) {
			var t = this,  s = ed.settings;

			t.editor = ed;
		},

		renderUI : function(o) {
			return { deltaHeight: 0 }
		},

		getInfo : function() {
			return {
				longname : 'Dummy theme',
				author : 'Me',
				authorurl : 'http://tinymce.moxiecode.com',
				version : tinymce.majorVersion + "." + tinymce.minorVersion
			}
		}
	});

	tinymce.ThemeManager.add('dummy', tinymce.themes.DummyTheme);
})();
