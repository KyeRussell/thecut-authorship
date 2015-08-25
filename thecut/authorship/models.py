# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django.db import models
from thecut.authorship import settings
import warnings


class Authorship(models.Model):
    """Abstract model to track when an instance was created/updated and by
    whom."""

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    """:py:class:`datetime` for when this object was first created."""

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, editable=False,
                                   related_name='+', on_delete=models.PROTECT)
    """User who first created this object (required)."""

    updated_at = models.DateTimeField(auto_now=True, editable=False)
    """:py:class:`datetime` for when this object was last saved."""

    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, editable=False,
                                   related_name='+', on_delete=models.PROTECT)
    """User who last saved this object (required)."""

    class Meta(object):
        abstract = True

    def save(self, user=None, **kwargs):
        update_fields = kwargs.pop('update_fields', None)

        if update_fields and 'updated_at' not in update_fields:
            update_fields.append('updated_at')

        if not self.pk:
            if update_fields and 'created_at' not in update_fields:
                update_fields.append('created_at')

        if user is not None:

            self.updated_by = user
            if update_fields and 'updated_by' not in update_fields:
                update_fields.append('updated_by')

            if not self.pk:
                self.created_by = user
                if update_fields and 'created_by' not in update_fields:
                    update_fields.append('created_by')

        kwargs.update({'update_fields': update_fields})
        return super(Authorship, self).save(**kwargs)


class AbstractAuthorshipModel(Authorship):
    """AbstractAuthorshipModel is deprecated. Use Authorship model instead."""
    # Renamed for consistency with publishing models.

    class Meta(Authorship.Meta):
        abstract = True

    def __init__(self, *args, **kwargs):
        warnings.warn('AbstractAuthorshipModel is deprecated - use Authorship '
                      'model instead.', DeprecationWarning, stacklevel=2)
        return super(AbstractAuthorshipModel, self).__init__(*args, **kwargs)
