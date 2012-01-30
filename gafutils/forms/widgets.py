# -*- coding: utf-8 -*-
from django.forms.widgets import CheckboxInput
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