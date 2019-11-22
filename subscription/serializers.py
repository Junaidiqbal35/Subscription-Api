import datetime

from rest_framework import serializers
from .models import Membership, UserMembership, Subscription


class MembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membership
        fields = ('id', 'slug', 'membership_type', 'price')


class SubscriptionSerializer(serializers.ModelSerializer):
    expired_at = serializers.DateTimeField(
        input_formats=['%I:%M %p %d %B %Y'], format=None, allow_null=True,
        help_text='Accepted format is "12:01 PM 16 April 2019" (Add a Gap of 30 days)',
        style={'input_type': 'text', 'placeholder': '12:01 AM 28 July 2019'}, )

    class Meta:
        model = Subscription
        fields = ('user_membership', 'created_at', 'expired_at')

    """"
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['user_membership'] = instance.user_membership.membership.membership_type
        return data
    """


class UserMembershipSerializer(serializers.ModelSerializer):
    plan = SubscriptionSerializer(many=True, read_only=False)
    url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = UserMembership
        fields = ('url', 'user', 'membership', 'plan')

    def create(self, validated_data):
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

    def get_url(self, obj):
        # request added to get complete "http://127.0.0.1:8000/api/subscription/users/4/"
        request = self.context.get("request")
        return obj.get_api_url(request=request)
