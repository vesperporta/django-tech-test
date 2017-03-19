from __future__ import unicode_literals

import re

from django.contrib.auth.models import User
from django.db import models
from django.dispatch import Signal

from growthstreet.fields import IntegerRangeField
from growthstreet.mixins import GrowthStreetMixin


loan_created_signal = Signal(providing_args=[])


class BusinessSectorMixin(models.Model):
    """
    Break this mixin out into constants package or supply a cached list from
    a DB select on possible options of Business Sector.
    """
    RETAIL = 0
    PROFESSIONAL_SERVICES = 1
    FOOD_DRINK = 2
    ENTERTAINMENT = 3

    SECTOR_CHOICES = (
        (RETAIL, 'Retail'),
        (PROFESSIONAL_SERVICES, 'Professional Services'),
        (FOOD_DRINK, 'Food & Drink'),
        (ENTERTAINMENT, 'Entertainment'),
    )

    business_sector = models.PositiveSmallIntegerField(
        choices=SECTOR_CHOICES,
        null=False,
        blank=False
    )

    class Meta:
        abstract = True


class CorporationDetails(GrowthStreetMixin, BusinessSectorMixin):
    id = models.AutoField(primary_key=True)
    company_name = models.TextField(blank=False, null=False)
    address = models.TextField(blank=False, null=False)
    corporation_number = models.TextField(unique=True, blank=False, null=False)


class Loan(GrowthStreetMixin):
    id = models.AutoField(primary_key=True)
    applicant = models.ForeignKey(
        User,
        related_name='loans_list+',
    )
    corporation = models.ForeignKey(
        CorporationDetails,
        related_name='loans',
    )
    amount = IntegerRangeField(
        min_value=10000,
        max_value=100000,
        blank=False,
        null=False
    )
    expiry = models.DurationField(
        null=False,
        blank=False
    )
    reason = models.TextField(blank=False, null=False)
    created_signal_sent = models.BooleanField(default=False)

    def _create_populate_related(self, *args, **kwargs):
        user_list = User.objects.get(email=kwargs['email'])
        if not user_list:
            uname = kwargs['email']
            uname = uname.split('@', 1)[0]
            uname = re.sub(r'[,.-_+=@]', '', uname)
            uname = uname.lower()
            self.applicant = User(username=uname, **kwargs)

    def _trigger_created_signal(self, *args, **kwargs):
        loan_created_signal.send(
            sender=self.__class__,
            loan=self,
            **kwargs
        )
        self.created_signal_sent = True

    def save(self, *args, **kwargs):
        if not self.created_signal_sent:  # New Loan
            self._create_populate_related(*args, **kwargs)
            self._trigger_created_signal(*args, **kwargs)
        super(Loan, self).save(*args, **kwargs)
