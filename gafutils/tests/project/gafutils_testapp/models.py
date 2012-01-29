# -*- coding: utf-8 -*-
from django.db import models
from gafutils.db.fields import DefaultObjectField
from gafutils.db.fields import dynamic_type



# Test models for : DefaultObjectField
# -----------------------------------------------------------------------------

class Picture(models.Model):
    name = models.CharField(max_length=40)
    is_default = DefaultObjectField()

class LargePicture(Picture):
    pass

class SmallPicture(Picture):
    is_small_default = DefaultObjectField()

class TinyPicture(SmallPicture):
    pass

# Test models for : DynamicTypeField
# -----------------------------------------------------------------------------
class ValueHolder(models.Model):
    
    value = dynamic_type.DynamicTypeField()
    
    def get_value_type(self):
        return self.value_type
    
class IntValueHolder(ValueHolder):
    value_type = 'int'
    
class FieldMapValueHolder(models.Model):
    
    i_value = models.IntegerField()
    b_value = models.BooleanField() 
    value = dynamic_type.DynamicTypeField(create_fields=False, field_map = {
        dynamic_type.INTEGER: 'i_value',
        dynamic_type.BOOLEAN: 'b_value',
    })
    
    
    
    
    