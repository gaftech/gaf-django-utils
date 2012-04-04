# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.db.models.query import QuerySet

class PolymorphicQuerySet(QuerySet):
    
    _polymorphic = False
    
    def select_polymorphic(self):
        new_qs = self._clone()
        new_qs._polymorphic = True
        return new_qs
    
    def _clone(self, *args, **kwargs):
        kwargs['_polymorphic'] = self._polymorphic
        return super(PolymorphicQuerySet, self)._clone(*args, **kwargs)
    

    def iterator(self):
        
        if self._polymorphic:
            it = self.iter_polymorphic()
        else:
            it = super(PolymorphicQuerySet, self).iterator()
        for obj in it:
            yield obj

    def iter_polymorphic(self):
        
        results = tuple(self.values_list('pk', 'polymorphic_ctype_id'))
        pks = [r[0] for r in results]
        ctypes = ContentType.objects.in_bulk(set(r[1] for r in results))
        children = {}
        for pk, ctype_id in results:
            if pk not in children:
                ctype = ctypes[ctype_id]
                model = ctype.model_class()
                for obj in model._default_manager.filter(pk__in=pks):
                    assert obj.pk not in children
                    children[obj.pk] = obj
            yield children[pk]


class PolymorphicManager(models.Manager):
    
    use_for_related_fields = True
    
    def get_query_set(self):
        return PolymorphicQuerySet(self.model)

    def select_polymorphic(self, *args, **kwargs):
        return self.get_query_set().select_polymorphic(*args, **kwargs)


class PolymorphicModel(models.Model):
    
    class Meta:
        abstract = True
    
    objects = PolymorphicManager()
    
    polymorphic_ctype = models.ForeignKey(ContentType, editable=False) 
    
    def save(self, *args, **kwargs):
        if not self.polymorphic_ctype_id:
            self.polymorphic_ctype = ContentType.objects.get_for_model(self)
        super(PolymorphicModel, self).save(*args, **kwargs)
        
    def cast(self):
        return self.polymorphic_ctype.get_object_for_this_type(pk=self.pk)
    
    