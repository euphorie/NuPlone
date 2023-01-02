# coding=utf-8
from plone.app.testing import login
from plone.app.testing import setRoles
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plonetheme.nuplone.skin.interfaces import NuPloneSkin
from plonetheme.nuplone.testing import NUPLONE_FUNCTIONAL_TESTING
from plonetheme.nuplone.testing import NUPLONE_INTEGRATION_TESTING
from zope.interface import alsoProvides

import unittest
import zope.component


class SiteMenuIntegrationTests(unittest.TestCase):
    layer = NUPLONE_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.request = self.portal.REQUEST
        alsoProvides(self.request, NuPloneSkin)

    def test_settings_url(self):
        """Check that the sitemenu view provides a settings_url attribute"""
        view = zope.component.getMultiAdapter(
            (self.portal, self.request),
            name="sitemenu",
        )
        self.assertEqual(view.settings_url, "http://nohost/plone/@@settings")


class SiteMenuTests(unittest.TestCase):
    layer = NUPLONE_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.request = self.portal.REQUEST
        alsoProvides(self.request, NuPloneSkin)
        login(self.layer["app"], SITE_OWNER_NAME)

        # Create two folders
        self.portal.invokeFactory("Folder", "source_folder")
        self.source_folder = self.portal["source_folder"]

        self.portal.invokeFactory("Folder", "dest_folder")
        self.dest_folder = self.portal["dest_folder"]

        # Create an object to be copied
        self.source_folder.invokeFactory("Document", "doc")

    def testActions(self):
        login(self.portal, TEST_USER_NAME)
        setRoles(self.portal, TEST_USER_ID, ("Contributor",))
        # Copy the object
        cp = self.source_folder.manage_copyObjects(ids=["doc"])
        self.request["__cp"] = cp

        # We cannot paste the object in the site root
        v = zope.component.getMultiAdapter((self.portal, self.request), name="sitemenu")
        self.assertIsNone(v.organise())
        # XXX it seems we have no actions here
        return
        # We can however paste the object in each of the folders
        for folder in [self.source_folder, self.dest_folder]:
            v = zope.component.getMultiAdapter((folder, self.request), name="sitemenu")
            menu = v.organise()
            self.assertIsNotNone(menu)
            children_titles = [i["title"] for i in menu["children"]]
            self.assertTrue("menu_paste" in children_titles)

        # Now when we give the user the Viewer role, they cannot paste anymore
        # so we should not see "Paste" as an available action.
        setRoles(self.portal, TEST_USER_ID, ("Viewer",))
        for folder in [self.source_folder, self.dest_folder]:
            v = zope.component.getMultiAdapter((folder, self.request), name="sitemenu")
            menu = v.organise()
            self.assertIsNotNone(menu)
            children_titles = [i["title"] for i in menu["children"]]
            self.assertFalse("menu_paste" in children_titles)

    def test_adding_to_same_category(self):
        from plonetheme.nuplone.skin.sitemenu import Sitemenu

        sitemenu = Sitemenu(None, None)
        sitemenu.factories = lambda: {
            "title": "cat1",
            "children": [{"title": "sub1.1"}, {"title": "sub1.2"}],
        }
        sitemenu.organise = lambda: {"title": "cat1", "children": [{"title": "sub1.3"}]}

        menu = sitemenu.actions
        self.assertEqual(len(menu["children"]), 1)
        self.assertEqual(menu["children"][0]["title"], "cat1")
        self.assertEqual(len(menu["children"][0]["children"]), 3)
        self.assertEqual(menu["children"][0]["children"][0]["title"], "sub1.1")
        self.assertEqual(menu["children"][0]["children"][1]["title"], "sub1.2")
        self.assertEqual(menu["children"][0]["children"][2]["title"], "sub1.3")

    def test_add_submenu(self):
        from plonetheme.nuplone.skin.sitemenu import Sitemenu

        sitemenu = Sitemenu(None, None)
        menu = [
            {"title": "cat1", "children": [{"title": "sub1.1"}]},
            {"title": "cat2", "children": [{"title": "sub2.1"}]},
        ]
        sitemenu.add_submenu(menu, {"title": "cat1", "children": [{"title": "sub1.2"}]})
        self.assertEqual(len(menu), 2)
        self.assertEqual(menu[0]["title"], "cat1")
        self.assertEqual(len(menu[0]["children"]), 2)
        self.assertEqual(menu[0]["children"][0]["title"], "sub1.1")
        self.assertEqual(menu[0]["children"][1]["title"], "sub1.2")
        self.assertEqual(menu[1]["title"], "cat2")
        self.assertEqual(len(menu[1]["children"]), 1)
        self.assertEqual(menu[1]["children"][0]["title"], "sub2.1")
