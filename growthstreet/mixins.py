from __future__ import unicode_literals

from django.db import models


class GrowthStreetMixin(models.Model):
    created_on = models.DateTimeField(
        auto_now_add=True
    )
    deleted_on = models.DateTimeField(
        null=True,
        blank=True
    )
    updated_on = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        abstract = True
        app_label = 'growthstreet.mixins'
