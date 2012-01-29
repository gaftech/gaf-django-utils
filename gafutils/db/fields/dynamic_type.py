# -*- coding: utf-8 -*-
"""
The :mod:`dynamic_type` defines a :class:`DynamicTypeField` *pseudo database field* that points to an appropriate
:class:`Field` instance, depending on a type which is given at runtime.
 
It can add *real* :class:`Field` instances to the model class. It also adds 
a descriptor (a setter/getter) in charge of setting/getting the appropriate field value. 

Example
-------
    >>> from django.db import models
    >>> from gafutils.db.fields.dynamic_type import DynamicTypeField
    >>>
    >>> class ValueHolder(models.Model):
    ...    value = DynamicTypeField()
    >>>
    >>> value_holder = ValueHolder(value_int=123, value_str='abc')
    >>> value_holder.value_type = 'str'
    >>> value_holder.value_int, value_holder.value_str, value_holder.value
    (123, 'abc', 'abc')
    >>> value_holder.value_type = 'int'
    >>> value_holder.value_int, value_holder.value_str, value_holder.value
    (123, 'abc', 123)
"""


from django.db import models
from django.core.exceptions import ImproperlyConfigured
from django.utils.functional import curry

# Default type identifiers
BOOLEAN = 'bool'
STRING = 'str'
INTEGER = 'int'
FLOAT = 'float'

#: Default type map
TYPE_MAP = {
    BOOLEAN: models.NullBooleanField,
    STRING:  models.TextField,
    INTEGER:  models.IntegerField,
    FLOAT: models.FloatField,
}

ALL_TYPES = TYPE_MAP.keys()

class DynamicTypeFieldDescriptor(object):
    """
    Used by :class:`.DynamicTypeField` to make its value available as a model attribute.
    """

    def __init__(self, field):
        self.field = field
    
    def __get__(self,  instance, instance_type=None):
        if instance is None:
            return self.field
        return self.field.get_value(instance)

    def __set__(self, instance, value):
        return self.field.set_value(instance, value)

class DynamicTypeField(object):
    
    type_map_override = None
    
    def __init__(self, types=None, exclude_types=None, type_callback=None,
                 create_fields=True, field_map=None, **field_options):
        """
        :param types: A list of type identifiers (type map keys) that limits the handled value types.
        :param excluded_types: A list of type identifiers to exclude (even if in `types`).
        :param type_callback:
            A callable that takes a model instance attribute and returns the
            current value type identifier.
        :param boolean create_fields:
            If `True`, associated fields will be created and added to the model.
            By default, will be `False` if field_map is given and `True` otherwise.
        :param dict field_map:
            A mapping between type identifiers and field names that will override
            the default field names. If given, it limits the handled types. 
        :param fields_options:
            If fields are created, there options will be passed to their constructors.
        """
        
        self.type_map = TYPE_MAP.copy()
        self.type_map.update(self.type_map_override or {})
        
        #: <type identifier> -> <field name> mapping
        self.fields = {}

        if field_map is None:
            field_map = dict( (type_id, None) for type_id in self.type_map.iterkeys() )
        
        for type_id, fname in field_map.iteritems():
            if exclude_types is not None and type_id in exclude_types:
                continue
            if types is not None and type_id not in exclude_types:
                continue
            self.fields[type_id] = fname

        self.type_callback = type_callback

        self.auto_create_fields = create_fields
        
        field_defaults = {
            'null': True,
        }
        field_defaults.update(field_options)
        self.field_options = field_defaults
    
    def contribute_to_class(self, cls, name):
        """Adds a value accessor to the class and eventually creates the db fields. 
        """
        self.name = name
        self.model = cls
        setattr(cls, name, DynamicTypeFieldDescriptor(self))
        for type_id, fname in self.fields.items():
            if fname is None:
                fname = self.construct_field_name(type_id)
                self.fields[type_id] = fname
            if self.auto_create_fields:
                field = self.create_field(type_id)
                field.contribute_to_class(cls, fname)

    def construct_field_name(self, type_id):
        """Returns the default db field name for the given type identifier"""
        return '%s_%s' % (self.name, type_id)

    def create_field(self, type_id, **kwargs):
        """Creates a Field instance for then given `type_id`.
        
        Can be used as a hook for inserting kwargs
        
        :param str type_id: a valid type identifier
        :param kwargs:
            Will be merged with self.field_options and passed to the field constructor
        """
        field_class = self.type_map[type_id]
        opts = self.field_options.copy()
        opts.update(kwargs)
        return field_class(**opts)

    def get_type_id(self, instance):
        """Returns the current type identifier, depending on the :class:`models.Model` instance.
        
        This method uses our `type_callback` or the instance :attr:`FOO_type` / :meth:`get_FOO_type`.
        """
        key = None
        if self.type_callback is not None:
            key = callable(instance)
        else:
            try:
                key = getattr(instance, 'get_%s_type' % self.name)()
            except AttributeError:
                try:
                    key = getattr(instance, '%s_type' % self.name)
                except AttributeError:
                    raise ImproperlyConfigured(
                        u"""%s field must define a `type_callback` attribute """
                        u"""or %s instance must define a  get_%s_type method """
                        u"""or a value_%s attribute.""" % (
                        self.__class__.__name__, instance.__class__.__name__,
                        self.name, self.name)
                    )
        if key not in self.fields:
            raise ValueError(u"%s is not a valid type identifier" % key)
        
        return key

    def get_value(self, instance):
        """Returns the current field value, depending on our type callback."""
        return getattr(instance, self.get_field_name(instance))
    
    def set_value(self, instance, value):
        """Sets the appropriate field value""" 
        setattr(instance, self.get_field_name(instance), value)

    def get_field(self, instance):
        """Returns the current :class:`models.Field` instance"""
        return self.get_field_by_name(self.get_field_name(instance))[0]

    def get_field_name(self, instance):
        """Returns the current db field name"""
        return self.fields[self.get_type_id(instance)]

    def get_fields(self):
        """Returns the list of associated :class:`models.Field` instances"""
        return [self.get_field_by_name(name) for name in self.get_field_names()]    
    
    def get_field_names(self):
        """Returns the list of handled db field names"""
        return self.fields.values()

    def get_field_by_name(self, name):
        """Returns the :class:`models.Field` instance with the given name"""
        return self.model._meta.get_field_by_name(name)[0]

