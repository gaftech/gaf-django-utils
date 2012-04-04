# -*- coding: utf-8 -*-
"""A simple breadcrumbs helper that I use to generate breadcrumbs from views."""

from django.utils.encoding import StrAndUnicode, force_unicode
from django.utils.translation import ugettext as _
from django.utils.safestring import mark_safe
from django.utils.text import capfirst

class Breadcrumb(StrAndUnicode):
    """A single breadcrumb element that knows how to display itself as html.
    """
    def __init__(self, name, url=None):
        """
        :param str name: the display name
        :param str: the url or None to only display name
        """
        self.name = name
        self.url = url
        
    def __unicode__(self):
        return force_unicode(self.render())
    
    def render(self):
        name = capfirst(force_unicode(self.name))
        if self.url is None:
            return name
        else:
            return '<a href="%s">%s</a>' % (self.url, name)
        
class Breadcrumbs(StrAndUnicode, list):
    """A list of :class:`Breadcrumb` elements that knows how to display itself as html."""
    
    def __unicode__(self):
        return force_unicode(self.render())
    
    def grow(self, *elements):
        """Returns a new :class:`Breadcrumbs` instance, appending to itself the given :class:`Breadcrumb` elements."""
        bs = Breadcrumbs(self)
        bs.extend(elements)
        return bs
        
    def render(self, sep=' > '):
        return mark_safe(sep.join(force_unicode(b) for b in self))

home_breadcrumbs = Breadcrumbs([
    Breadcrumb(_('Home'), '/'),
])
