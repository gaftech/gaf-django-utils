########################
Dynamic Type Field (DTF)
########################

Quick start
***********

.. automodule:: gafutils.db.fields.dynamic_type


Associating fields
******************

Associating types and field names
---------------------------------
:class:`DynamicTypeField` constructor can be given a `field_map`
argument, a dict witch keys are valid type identifiers and values are the
:class:`Field` instances names.

If `field_map` is not given, it will be created. Then, each type identifier
is associated to a field named like `<dtf name>_<type identifier>`.
See example above.

Auto-created fields
-------------------
By default, the  :class:`DynamicTypeField` will add to the model it belongs the
appropriate :class:`Field` instances.
The :attr:`type_map` describes which :class:`Field` class will be used for each
type : it's a dictionary where keys are type identifiers and values are 
:class:`django.db.models.Field` classes.

The default map (:data:`dynamic_type.TYPE_MAP`) associates the following strings and fields :

 * 'int' : :class:`models.IntegerField`
 * 'float' : :class:`models.FloatField`
 * 'bool' : :class:`models.NullBooleanField`
 * 'str' : :class:`models.TextField`

The :attr:`DynamicTypeField.type_map_override` class attribute can override/extend this map.

Limiting the handled types
--------------------------
:class:`DynamicTypeField` constructor takes two arguments to limit the handled
types, i.e. the associated :class:`Field` instances :

 * `types` is a list of types to handle
 * `exclude_types` is a list of types to exclude, even if they are in the `types` list.
   
If `field_map` is specified, it also limit the handled types. Note that
`types` and `exclude_types` still applies.


Retrieving the value type
*************************
There are two ways to tell the :class:`DynamicTypeField` which model field
holds the value :

`type_callback`
---------------
Specify a `type_callback` in the :class:`DynamicTypeField` constructor arguments. this
will be a callable that takes the model instance as argument an returns
a valid type identifier, i.e. a string that is a key of the :class:`DynamicTypeField`
instance :attr:`type_map`.

`get_FOO_type`, `FOO_type`
--------------------------
The model instance can define a :attr:`FOO_type` attribute or a :meth:`get_FOO_type` method
that will indicate the current type identifier. 

Type searching order
--------------------
The :class:`DynamicTypeField` will proceed in this order to to retrieve the current type :
 * Call the `type_callback` if set
 * Call the model instance `get_FOO_type` method if it exists
 * Use the model instance `FOO_type` attribute if it exists
 * Raise an :exc:`ImproperlyConfigured` exception if the above methods failed


Accessing the fields
********************
The :class:`DynamicTypeField` adds to the model a descriptor : a :class:`DynamicTypeFieldDescriptor` instance.
When called from a model instance, this descriptor acts as a getter/setter pointing to
the proper model attribute. If it is called as a getter from the model class, it 
returns the :class:`DynamicTypeField` instance, from which you can access the associated
:class:`Field` instances, using the :meth:`DynamicTypeField.get_fields`, etc. methods.


:mod:`dynamic_type` module API
******************************

.. autoclass:: gafutils.db.fields.dynamic_type.DynamicTypeField
   :members:
   :undoc-members:
   :show-inheritance:
   
.. autoclass:: gafutils.db.fields.dynamic_type.DynamicTypeFieldDescriptor
   :members:
   :undoc-members:
   :show-inheritance:
.. 
   .. automodule:: gafutils.db.fields.dynamic_type
       :members:
       :undoc-members:
       :show-inheritance: