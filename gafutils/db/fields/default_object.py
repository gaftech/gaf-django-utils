# -*- coding: utf-8 -*-
"""The :mod:`default_object` module is usefull if you need a db table with a default row.

It provides a model field and signal listeners to ensure
that it always exists one and only one row set as the default one.

Example
-------
    
    The :class:`Picture` model from gafutils' test app.
    
        .. literalinclude:: ../gafutils/tests/project/gafutils_testapp/models.py
           :pyobject: Picture
    
    Then, from a prompt:
    
        >>> from gafutils.tests.project.gafutils_testapp.models import Picture
        >>>
        >>> pic1 = Picture.objects.create(name='pic1')
        >>> pic2 = Picture.objects.create(name='pic2')
        >>>
        >>> list(Picture.objects.all())
        [<Picture: [DEFAULT] pic1>, <Picture: pic2>]
        >>>
        >>> pic2.is_default = True
        >>> pic2.save()
        >>>
        >>> list(Picture.objects.all())
        [<Picture: pic1>, <Picture: [DEFAULT] pic2>]

"""

from django.core.exceptions import SuspiciousOperation
from django.db import models
from django.db.models.signals import pre_save, pre_delete
from django.dispatch.dispatcher import receiver

class DefaultObjectField(models.BooleanField):
    """Boolean field that sets a default object for a given model.
    
    One and only one row in the db table must have this value set to ``True``.
    """
    __metaclass__ = models.SubfieldBase

    def contribute_to_class(self, cls, name):
        super(DefaultObjectField, self).contribute_to_class(cls, name)
        
        cls._default_object_fields = \
            getattr(cls, '_default_object_fields', set()).union((name,))

try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([
        (
         (DefaultObjectField,), [], {}
        ),
    ], ["^gafutils\.db\.fields\."])

except ImportError:
    pass    

@receiver(pre_save)
def pre_save_callback(sender, **kwargs):
    instance = kwargs['instance']
    default_object_fields = getattr(instance, '_default_object_fields', ())
    for fname in default_object_fields: # Check for unique field value
        field = instance._meta.get_field_by_name(fname)[0]
        qs = field.model._default_manager.filter(**{fname: True})
        if instance.pk is not None:
            qs = qs.exclude(pk=instance.pk)
        exists = qs.exists()
        if getattr(instance, fname):
            # This object is or will become the default one
            if exists:
                # Another default object exists, set it normal 
                qs.update(**{fname: False})
        elif not exists:
            # No default object exists, force this one as default
            setattr(instance, fname, True)
    
@receiver(pre_delete)
def pre_delete_callback(sender, **kwargs):
    instance = kwargs['instance']
    default_object_fields = getattr(instance, '_default_object_fields', ())
    for fname in default_object_fields:
        if getattr(instance, fname):
            raise SuspiciousOperation(
                u"Can't delete default %s object" % instance._meta)
