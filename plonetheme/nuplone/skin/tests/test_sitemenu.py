import unittest2 as unittest
import zope.component
from zope.interface import alsoProvides
from plone.testing import z2
from plone.app.testing import login
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from plonetheme.nuplone.skin.interfaces import NuPloneSkin
from plonetheme.nuplone.testing import NUPLONE_FUNCTIONAL_TESTING

class SiteMenuTests(unittest.TestCase):
    layer = NUPLONE_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.request = self.portal.REQUEST
        alsoProvides(self.request, NuPloneSkin)
        z2.login(self.layer['app']['acl_users'], SITE_OWNER_NAME)

        # Create two folders
        self.portal.invokeFactory("Folder", "source_folder")
        self.source_folder = self.portal['source_folder']

        self.portal.invokeFactory("Folder", "dest_folder")
        self.dest_folder = self.portal['dest_folder']

        # Create an object to be copied
        self.source_folder.invokeFactory("Document", "doc")

    def testActions(self):
        login(self.portal, TEST_USER_NAME)
        setRoles(self.portal, TEST_USER_ID, ('Contributor',))
        # Copy the object
        cp = self.source_folder.manage_copyObjects(ids=['doc'])
        self.request['__cp'] = cp

        # We cannot paste the object in the site root
        v = zope.component.getMultiAdapter(
                                (self.portal, self.request), name="sitemenu")
        self.assertIsNone(v.organise())

        # We can however paste the object in each of the folders
        for folder in [self.source_folder, self.dest_folder]:
            v = zope.component.getMultiAdapter(
                                (folder, self.request), name="sitemenu")
            menu = v.organise()
            self.assertIsNotNone(menu)
            children_titles = [i['title'] for i in menu['children']]
            self.assertTrue('menu_paste' in children_titles)

        # Now when we give the user the Viewer role, they cannot paste anymore
        # so we should not see "Paste" as an available action.
        setRoles(self.portal, TEST_USER_ID, ('Viewer',))
        for folder in [self.source_folder, self.dest_folder]:
            v = zope.component.getMultiAdapter(
                                (folder, self.request), name="sitemenu")
            menu = v.organise()
            self.assertIsNotNone(menu)
            children_titles = [i['title'] for i in menu['children']]
            self.assertFalse('menu_paste' in children_titles)
