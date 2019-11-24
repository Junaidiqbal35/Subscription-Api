import datetime
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _
from rest_framework.reverse import reverse as api_reverse
# use django hosts if you have --> sub domain for reverse
# Create your models here.

from django.utils import timezone

MEMBERSHIP_CHOICES = (
    ('Enterprise', 'enterprise'),
    ('Professional', 'professional'),
    ('Free', 'free'),
)
Plan_Interval = (
    ('Monthly', 'month'),
    ('Yearly', 'yearly'),
)


class Membership(models.Model):
    DISCOUNT_RATE = 0.10
    slug = models.SlugField(verbose_name=_("slug"))
    membership_type = models.CharField(
        verbose_name=_('Membership Type'),
        choices=MEMBERSHIP_CHOICES,
        default=_('Free'),
        max_length=30)
    price = models.FloatField(verbose_name=_("price"))
    active = models.BooleanField(default=True)
    interval = models.CharField(
        verbose_name=_('Plan Period'),
        choices=Plan_Interval,
        default=_('Monthly'),
        max_length=30
    )

    class Meta:
        verbose_name = _('Membership')
        verbose_name_plural = _('Memberships')

    def get_rounded_price(self):
        return round(self.price, 2)

    def current_price(self):
        if self.is_on_sale():
            discounted_price = self.price * (1 - self.DISCOUNT_RATE)
            return round(discounted_price, 2)
        return self.get_rounded_price()

    def __str__(self):
        return self.membership_type


class UserMembership(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=_("User Model"))
    membership = models.ForeignKey(Membership, on_delete=models.SET_NULL, null=True, verbose_name=_("Plan list"))

    def __str__(self):
        return self.membership.membership_type

    class Meta:
        verbose_name = _('User Membership')
        verbose_name_plural = _('User Memberships')

    def get_api_url(self, request=None):
        return api_reverse('subscription:user-membership', kwargs={'id': self.id}, request=request)


def get_deadline():
    return datetime.datetime.today() + datetime.timedelta(days=30)


class Subscription(models.Model):
    user_membership = models.ForeignKey(UserMembership, related_name='plan', on_delete=models.CASCADE,
                                        verbose_name=_("User MemberShip data"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("created_at"))
    updated = models.DateTimeField(auto_now=True, verbose_name=_("updated_at"))
    active = models.BooleanField(default=True)
    expired_at = models.DateTimeField(default=get_deadline(), verbose_name=_("billing_date"))
    """
    def save(self, *args, **kwargs):
        self.expired_at = datetime.datetime.now() + datetime.timedelta(30)
        super(Subscription, self).save(*args, **kwargs)  # Call the "real" save() method
    """

    class Meta:
        verbose_name = _('Subscription')
        verbose_name_plural = _('Subscriptions')

    @property
    def is_expired(self):
        if datetime.datetime.now() > self.expired_at:
            return True
        return False

    def __str__(self):
        return self.user_membership.membership.membership_type
