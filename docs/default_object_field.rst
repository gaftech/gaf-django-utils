Default Object Field
####################

Quick start
***********

.. automodule:: gafutils.db.fields.default_object

Behaviour
*********

`pre_save` and `pre_delete` listener will try to ensure that there always exists a default row
in a db table, and try to do it silently.

Saving
======

Before a :class:`Model` instance belonging a :class:`DefaultObjectField` is saved, the following checks and db updates are made :

 * If the model instance is set as the default one (i.e. its :class:`DefaultObjectField` field value is set to `True`),
   and there already is another default row in the db table, the instance being saved will become the default.
 * If it is not set as the default one but there is no default row in the db table, its :class:`DefaultObjectField` field value
   will be forced to `True`.
   
Deleting
========

Trying to delete a model instance set as default will raise a :exc:`SuspiciousOperation`.

Multiple :class:`DefaultObjectField` s
**************************************

You can associate many :class:`DefaultObjectField` fields to a model, simply like this : ::
   
   class MyModel(models.Model):
      is_foo_default = DefaultObjectField()
      is_bar_default = DefaultObjectField()

This way, a model instance can be the default regarding some *bar* specifications, and another model instance
can be the default regarding some *foo* specifications. 

Inheritance
***********

For models belonging to an inheritance tree, the existence and uniqueness of the default row is checked 
at the :class:`DefaultObjectField` field table level. So, you can have default objects defined like this : ::
   
   class Vehicle(models.Model):
      vehicle_of_the_year = DefaultObjectField()
     
   class Car(Vehicle):
      car_of_the_year = DefaultObjectField()
   
   class Truck(Vehicle):
      truck_of_the_year = DefaultObjectField()
   
This way, you have one and only one *vehicle of the year* (which can be a car or a truck), 
one an only one *car of the year* and one and only one *truck of the year*.  

 

Admin change list widget
************************

The :class:`gafutils.forms.widgets.DefaultObjectAdminWidget` is a simple check box to be used
in an admin editable change list. It loads a javascript that ensures that, in a :class:`DefaultObjectField` column, at most one 
row is checked as the default.

