from rest_framework import serializers
from .models import Membership, UserMembership, Subscription


class MembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membership
        fields = ('id', 'slug', 'membership_type', 'price')


class SubscriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscription
        fields = ('created_at',)


class UserMembershipSerializer(serializers.ModelSerializer):
    plan = SubscriptionSerializer(many=True, read_only=True)

    class Meta:
        model = UserMembership
        fields = ('user', 'membership', 'plan')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['user'] = instance.user.username
        data['membership'] = instance.membership.membership_type
        return data



