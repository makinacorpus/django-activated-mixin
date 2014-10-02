from django.test import Client, TestCase
from django.contrib.auth.models import User

from activated_mixin.tests.models import ModelTest, SubModelTest


class MixinTestCase(TestCase):
    def test_object_creation(self):
        """ Test a simple object creation. """
        SubModelTest.objects.create()
        submodel = SubModelTest.objects.last()
        self.assertEqual(SubModelTest.objects.all().count(), 1)
        self.assertEqual(SubModelTest.actives.all().count(), 1)
        self.assertTrue(submodel.activated)
        self.assertEqual(
            SubModelTest.objects.all().count(),
            SubModelTest.actives.all().count()
        )

    def test_unlinked_object_deletion(self):
        """ Test deletion of an object which is NOT linked to another. """
        SubModelTest.objects.create()
        submodel = SubModelTest.objects.last()
        self.assertEqual(SubModelTest.objects.all().count(), 1)
        self.assertEqual(SubModelTest.actives.all().count(), 1)
        self.assertTrue(submodel.activated)
        submodel.delete()
        self.assertEqual(SubModelTest.objects.all().count(), 0)
        self.assertEqual(SubModelTest.actives.all().count(), 0)

    def test_linked_object_deletion(self):
        """ Test deletion of an object which is linked to another. """
        SubModelTest.objects.create()
        submodel = SubModelTest.objects.last()
        self.assertEqual(SubModelTest.objects.all().count(), 1)
        self.assertEqual(SubModelTest.actives.all().count(), 1)
        self.assertTrue(submodel.activated)
        ModelTest.objects.create(related=submodel)
        submodel.delete()
        self.assertEqual(SubModelTest.objects.all().count(), 1)
        self.assertEqual(SubModelTest.actives.all().count(), 0)
        self.assertFalse(submodel.activated)


class AdminTestCase(TestCase):
    def setUp(self):
        User.objects.create_superuser('admin', '', 'password')
        self.c = Client()
        self.c.login(username="admin", password="password")

        SubModelTest.objects.create(identifier="inactive")
        self.submodel = SubModelTest.objects.last()
        self.submodel.activated = False
        self.submodel.save()
        SubModelTest.objects.create(identifier="active")
        self.submodel2 = SubModelTest.objects.last()

    def test_admin_listing(self):
        """ Test the admin view listing all objects. """
        response = self.c.get('/admin/tests/submodeltest/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            '<em style="color:#ff3e3e; font-weight:normal">inactive</em>',
            response.content.decode('utf8')
        )
        self.assertNotIn(
            '<em style="color:#ff3e3e; font-weight:normal">active</em>',
            response.content.decode('utf8')
        )
