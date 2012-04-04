# -*- coding: utf-8 -*-
"""Base app-registry classes.

..see:: inspired from pypi.python.org/pypi/django-appregister
"""
from collections import Mapping, Sized, Iterable, Container
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.importlib import import_module
from django.utils.module_loading import module_has_submodule
from functools import wraps

class AlreadyRegistered(Exception):
    pass

def discover(func):
    @wraps(func)
    def wrapper(registry, *args, **kwargs):
        registry._discover()
        return func(registry, *args, **kwargs)
    return wrapper

class BaseRegistry(Sized, Iterable, Container):

    # Autodiscovering statuses
    NOT_DISCOVERED = 0
    DISCOVERING = 1
    DISCOVERED = 2

    #: The type of datastructure that holds the data (set, dict...)
    registry_class = None
    #: If True, trying to re-register an element will not raise exception but element will not be registered a second time 
    ignore_duplicates = False
    #: name of apps' module to import when autodiscovering
    discover_module = None
    #: indicates if autodiscovery must be performed on first regitry access
    autoload = True
    
    def __init__(self):
        self._discover_status = self.NOT_DISCOVERED
        self._registry = self.create_registry()
        self.ignore_duplicates = self.ignore_duplicates or getattr(settings, 'REGISTRY_IGNORE_DUPLICATES', False) 

    @discover
    def __iter__(self):
        return iter(self._registry)
    
    def __len__(self):
        return len(self._registry)

    def __contains__(self, element):
        return element in self._registry

    def create_registry(self):
        return self.registry_class()

    def _discover(self):
        if self._discover_status == self.NOT_DISCOVERED and self.autoload:
            self.autodiscover()

    def autodiscover(self):
        if self._discover_status > self.NOT_DISCOVERED:
            raise RuntimeError(u"autodiscover has already been called")
        else:
            self._discover_status = self.DISCOVERING
        module = self.discover_module
        if not module:
            raise ImproperlyConfigured(u"%s _registry must specify 'discover_module'" % self.__class__.__name__)
        for app in settings.INSTALLED_APPS:
            try:
                import_module(".%s" % module, app)
            except ImportError:
                if module_has_submodule(import_module(app), module):
                    raise
                continue
        self._discover_status = self.DISCOVERED
    
    def register(self, element, *args, **kwargs):
        assert self._discover_status is not self.DISCOVERED
        if self.is_registered(element, *args, **kwargs):
            if not self.ignore_duplicates:
                raise AlreadyRegistered(u"%s already registered in %s _registry" % (
                                        element, self.__class__.__name__))
        else:
            self.validate(element, *args, **kwargs)    
            self.add(element, *args, **kwargs)
        return element
    
    def validate(self, element, *args, **kwargs):
        pass
        
    def is_registered(self, element, *args, **kwargs):
        return element in self._registry
    
    def add(self, element, *args, **kwargs):
        raise NotImplementedError
    
    def unregister(self, element):
        raise NotImplementedError

    
class Registry(BaseRegistry):
    
    registry_class = set
    
    def add(self, element):
        self._registry.add(element)
    
    def unregister(self, element):
        self._registry.remove(element)
        
class DictRegistry(Mapping, BaseRegistry):
    
    registry_class = dict
    
    @discover
    def __getitem__(self, key):
        return self._registry[key]
    
    def keys(self):
        return self._registry.keys()
    
    @discover
    def items(self):
        return self._registry.items()
    
    @discover
    def iteritems(self):
        for item in self._registry.iteritems():
            yield item
    
    @discover
    def values(self):
        return self._registry.values()
    
    @discover
    def itervalues(self):
        for v in self._registry.itervalues():
            yield v
    
    def get(self, key, default):
        return self._registry.get(key, default)
    
    def __eq__(self, other):
        return isinstance(other, DictRegistry) and other._registry == self._registry
        
    def __ne__(self, other):
        return not isinstance(other, DictRegistry) or other._registry != self._registry    
        
    def register(self, element, key=None):
        if key is None:
            try:
                key = self.get_key(element)
            except NotImplementedError:
                raise ImproperlyConfigured(u"%s _registry : provide a key or implement get_key()")
        return super(DictRegistry, self).register(element, key)
    
    def get_key(self, element):
        raise NotImplementedError
    
    def is_registered(self, element, key):
#        r = self._registry
        i = key in self._registry
        return i
        
    def add(self, element, key):
        self._registry[key] = element
        
    def unregister(self, key):
        del self._registry[key]
        
        
    
    
    
    
    