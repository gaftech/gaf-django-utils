# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.exceptions import SuspiciousOperation
from django.test import TestCase
from gafutils.tests.project.gafutils_testapp.models import Picture, TinyPicture, IntValueHolder, \
    ValueHolder, FieldMapValueHolder


class DynamicTypeFieldTest(TestCase):
    
    def test_set_int(self):
        obj = IntValueHolder.objects.create()
        obj = IntValueHolder.objects.get(pk=obj.pk)
        self.assertIs(obj.value, None)
        obj.value = 123
        obj.save()
        self.assertEqual(IntValueHolder.objects.get(pk=obj.pk).value, 123)
    
    def test_field_map(self):
        """Tests that the `field_map` argument is correctly handled"""
#        vh = FieldMapValueHolder()
        self.assertEqual(['i_value', 'b_value'], FieldMapValueHolder.value.get_field_names())
        
        
    

class DefaultObjectFieldTest(TestCase):

#    def test_first_object(self):
#        Picture.objects.all().delete()
#        self.assertFalse(Picture.objects.exists())  # Check that no picture already exists
#        Picture.objects.create()
#        self.assertTrue(Picture.objects.get().is_default)

    def test_default_value(self):
        pic1 = Picture.objects.create(is_default=True)
        pic2 = Picture.objects.create()
        self.assertTrue(Picture.objects.get(pk=pic1.pk).is_default)
        self.assertEqual(Picture.objects.filter(is_default=True).count(), 1)
        
    def test_set_true(self):
        the_one = Picture.objects.create(is_default=True)
        another = Picture.objects.create()
        another.is_default = True
        another.save()
        self.assertTrue(Picture.objects.get(pk=another.pk).is_default)
        self.assertEqual(Picture.objects.filter(is_default=True).count(), 1)
    
    def test_set_true_on_subclass(self):
        the_picture = Picture.objects.create(is_default=True)
        a_tiny_picture = TinyPicture.objects.create()
        a_tiny_picture.is_default = True
        a_tiny_picture.save()
        self.assertTrue(
            Picture.objects.get(pk=a_tiny_picture.pk).is_default)
        self.assertFalse(
            Picture.objects.get(pk=the_picture.pk).is_default)  
    
    def test_set_false(self):
        the_one = Picture.objects.create(is_default=True)
        the_one.is_default = False
        self.assertTrue(Picture.objects.get(pk=the_one.pk).is_default)

    def test_delete(self):
        """Deleting default object must raise an exception"""
        the_one = Picture.objects.create(is_default=True)
        another = Picture.objects.create()
        self.assertRaises(SuspiciousOperation, the_one.delete)
        self.assertEqual(Picture.objects.filter(is_default=True).count(), 1)
    
    def test_delete_multiple(self):
        the_one = Picture.objects.create(is_default=True)
        another = Picture.objects.create()
        self.assertRaises(SuspiciousOperation,
                          Picture.objects.all().delete)
        self.assertEqual(
            Picture.objects.filter(is_default=True).count(), 1)

