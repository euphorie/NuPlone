import unittest2 as unittest
import transaction
import zope.component
from zope.interface import alsoProvides
from plone.app.testing import login
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from plonetheme.nuplone.skin.interfaces import NuPloneSkin
from plonetheme.nuplone.testing import NUPLONE_FUNCTIONAL_TESTING

class SiteMenuTests(unittest.TestCase):
    layer = NUPLONE_FUNCTIONAL_TESTING

    def testActions(self):
        portal = self.layer["portal"]
        request = portal.REQUEST
        alsoProvides(request, NuPloneSkin)

        login(portal, TEST_USER_NAME)
        setRoles(portal, TEST_USER_ID, ('Manager',))

        # Create two folders
        portal.invokeFactory("Folder", "folder1")
        folder1 = portal['folder1']
        transaction.commit()

        portal.invokeFactory("Folder", "folder2")
        folder2 = portal['folder2']
        transaction.commit()

        # Create an object to be copied
        folder1.invokeFactory("Document", "doc1")
        transaction.commit()

        # Copy the object
        cp = folder1.manage_copyObjects(ids=['doc1'])
        request['__cp'] = cp

        # We cannot paste the object in the site root
        v = zope.component.getMultiAdapter((portal, request), name="sitemenu")
        self.assertIsNone(v.organise())

        # We can however paste the object in each of the folders
        for folder in [folder1, folder2]:
            v = zope.component.getMultiAdapter((folder1, request), name="sitemenu")
            menu = v.organise()
            self.assertIsNotNone(menu)
            children_titles = [i['title'] for i in menu['children']]
            self.assertTrue('menu_paste' in children_titles)
