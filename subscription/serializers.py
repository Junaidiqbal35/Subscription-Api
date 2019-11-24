import datetime

from rest_framework import serializers
from .models import Membership, UserMembership, Subscription
from django.utils.translation import gettext_lazy as _


class MembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membership
        fields = ('id', 'slug', 'membership_type', 'interval', 'active', 'price')


# for expired date
def get_deadline():
    return datetime.datetime.today() + datetime.timedelta(days=30)


class SubscriptionSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only=True)
    email = serializers.SerializerMethodField(read_only=True)

    # user_membership = serializers.SerializerMethodField(read_only=True)
    # updated = serializers.SerializerMethodField(read_only=True)
    # expired_at = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Subscription
        fields = ('name', 'user_membership', 'email', 'expired_at')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['user_membership'] = instance.user_membership.membership.membership_type
        return data

    def get_email(self, instance):
        return instance.user_membership.user.email

    def get_name(self, instance):
        return instance.user_membership.user.username


class SubscriptionReminder(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only=True)
    email = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Subscription
        fields = ('name', 'email', 'user_membership', 'created_at', 'expired_at')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['user_membership'] = instance.user_membership.membership.membership_type
        return data

    def get_email(self, instance):
        return instance.user_membership.user.email

    def get_name(self, instance):
        return instance.user_membership.user.username


class UserMembershipSerializer(serializers.ModelSerializer):
    plan = SubscriptionSerializer(many=True, read_only=False)
    # user_plan = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = UserMembership
        fields = ('url', 'user', 'membership', 'plan')

    def update(self, instance, validated_data):
        subscriptions_data = validated_data.pop('plan')
        user_memberships = UserMembership.objects.create(**validated_data)
        for subscription_data in subscriptions_data:
            Subscription.objects.create(user_membership=user_memberships, **subscription_data)
        return user_memberships

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['user'] = instance.user.username
        data['membership'] = instance.membership.membership_type
        return data

    """
    def get_user_plan(self, instance):
        plan = Subscription.objects.filter(user_membership=instance)
        return SubscriptionSerializer(plan, many=True).data
    """

    def get_url(self, obj):
        # request added to get complete "http://127.0.0.1:8000/api/subscription/users/4/"
        request = self.context.get("request")
        return obj.get_api_url(request=request)
