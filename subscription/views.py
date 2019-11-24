import datetime
from django.contrib import messages
from django.core.mail import send_mail, EmailMultiAlternatives
from django.shortcuts import render

# Create your views here.
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.decorators import permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView, mixins, CreateAPIView, RetrieveUpdateDestroyAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from .models import Membership, UserMembership, Subscription
from .serializers import MembershipSerializer, UserMembershipSerializer, SubscriptionSerializer, SubscriptionReminder


@permission_classes([IsAdminUser])
class MembershipView(ListAPIView):
    queryset = Membership.objects.all()
    serializer_class = MembershipSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filter_fields = ('id',)
    search_fields = ('membership_type', 'slug')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@permission_classes([IsAdminUser])
class MembershipCreate(CreateAPIView):
    serializer_class = MembershipSerializer
    queryset = Membership.objects.all()

    def create(self, request, *args, **kwargs):
        try:
            price = request.data.get('price')
            if price == 0.0:
                pass
            elif price is not None and float(price) < 0.0:
                raise ValidationError({'price': 'Must be above $0.0'})

        except ValueError:
            raise ValidationError({'price': 'A valid number is required'})

        return super().create(request, *args, **kwargs)


@permission_classes([IsAdminUser])
class UserMembershipView(ListAPIView):
    queryset = UserMembership.objects.all()
    serializer_class = UserMembershipSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filter_fields = ('id',)
    search_fields = ('user', 'membership')

    # this method return request and help to get full url
    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}


@permission_classes([IsAuthenticated])
class SubscriptionView(ListAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer


@permission_classes([IsAuthenticated])
class SubscriptionRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    lookup_field = 'pk'
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer


@permission_classes([IsAdminUser])
class ReminderSubscriberView(ListAPIView):
    queryset = Subscription.objects.filter(expired_at__lte=timezone.now())
    serializer_class = SubscriptionReminder
    lookup_fields = 'expired_at'

    def get_queryset(self):
        queryset = Subscription.objects.filter(expired_at__lte=timezone.now())
        return queryset

    receivers = []

    for expired_user in queryset:
        receivers.append(expired_user.user_membership.user.email)

    msg = EmailMultiAlternatives('subscription expired', 'your subscription is expired ', 'mc130202861@vu.edu.pk',
                                 bcc=receivers)

    #msg.send() ..bug


@permission_classes([IsAuthenticated])
class UserMembershipRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    serializer_class = UserMembershipSerializer
    queryset = UserMembership.objects.all()
    lookup_field = 'id'

    def delete(self, request, *args, **kwargs):
        try:
            user_membership_id = request.data.get('id')
            response = super().delete(request, *args, *kwargs)
            if response.status_code == 204:
                from django.core.cache import cache
                cache.delete('user_membership_data {}'.format(user_membership_id))
                print(cache)
            return response
        except UserMembership.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        try:
            if response.status_code == 200:
                from django.core.cache import cache
                user_membership_data = response.data
                cache.set('user_membership_data {}'.format(['id']),
                          {'user': user_membership_data['user'], 'membership': user_membership_data['membership']})

            return response
        except UserMembership.DoestNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    # this method return request and help to get full url
    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}
