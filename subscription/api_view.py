from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import ValidationError
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView, mixins, CreateAPIView, RetrieveUpdateDestroyAPIView

from .models import Membership, UserMembership, Subscription
from .serializers import MembershipSerializer, UserMembershipSerializer, SubscriptionSerializer


class MembershipView(ListAPIView):
    queryset = Membership.objects.all()
    serializer_class = MembershipSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filter_fields = ('id',)
    search_fields = ('membership_type', 'slug')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


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


class UserMembershipView(ListAPIView):
    queryset = UserMembership.objects.all()
    serializer_class = UserMembershipSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filter_fields = ('id',)
    search_fields = ('user', 'membership')

    # this method return request and help to get full url
    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}


class SubscriptionView(mixins.CreateModelMixin, ListAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class UserMembershipRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    serializer_class = UserMembershipSerializer
    queryset = UserMembership.objects.all()
    lookup_field = 'id'

    def delete(self, request, *args, **kwargs):
        user_membership_id = request.data.get('id')
        response = super().delete(request, *args, *kwargs)
        if response.status_code == 204:
            from django.core.cache import cache
            cache.delete('user_membership_data {}'.format(user_membership_id))
            print(cache)
        return response

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        if response.status_code == 200:
            from django.core.cache import cache
            user_membership_data = response.data
            cache.set('user_membership_data {}'.format(['id']),
                      {'user': user_membership_data['user'], 'membership': user_membership_data['membership']})
        return response

    # this method return request and help to get full url
    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}



