# -*- coding: utf-8 -*-
from django.forms.widgets import CheckboxInput, Textarea
from django.conf import settings

class DefaultObjectAdminWidget(CheckboxInput):
    """Widget intended to select the default object in admin change list.
    """
    class Media:
        js = (
            'gafutils/js/DefaultObjectField.js',
        )
    
    
    def __init__(self, attrs=None, check_test=bool):
        
        _attrs = {
            'class': 'defaultObjectField',
        }
        _attrs.update(attrs or {})
        
        super(DefaultObjectAdminWidget, self).__init__(_attrs, check_test)
        
class JsonTextAreaWidget(Textarea):
    """
    To be used with django-extension JSONField. Displays json-formated string with indentation. 
    """
    
    def __init__(self, attrs=None, indent=4):
        super(JsonTextAreaWidget, self).__init__(attrs)
        self.indent = 4
        
    def render(self, name, value, attrs=None):
        if not isinstance(value, basestring):
            try:
                from django_extensions.db.fields.json import JSONEncoder
            except ImportError:
                from django.utils.simplejson import JSONEncoder
            kwargs = {
                "indent": self.indent,
            }
            value = JSONEncoder(**kwargs).encode(value)
        return super(JsonTextAreaWidget, self).render(name, value, attrs)
        
        
    
    