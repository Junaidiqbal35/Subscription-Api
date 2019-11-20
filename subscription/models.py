from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.utils import timezone

MEMBERSHIP_CHOICES = (
    ('Enterprise', 'ent'),
    ('Professional', 'pro'),
    ('Free', 'free')
)


class Membership(models.Model):
    DISCOUNT_RATE = 0.10
    slug = models.SlugField()
    membership_type = models.CharField(
        choices=MEMBERSHIP_CHOICES,
        default='Free',
        max_length=30)
    price = models.FloatField()

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
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    membership = models.ForeignKey(Membership, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.user.username


class Subscription(models.Model):
    user_membership = models.ForeignKey(UserMembership,related_name='plan', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    active = models.BooleanField(default=True)

    def __str__(self):
        return self.user_membership.user.username
