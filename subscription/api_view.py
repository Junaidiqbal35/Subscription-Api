from django_filters.rest_framework import DjangoFilterBackend
#from rest_framework.exceptions import ValidationError
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView, mixins


from .models import Membership, UserMembership, Subscription
from .serializers import MembershipSerializer, UserMembershipSerializer, SubscriptionSerializer


class MembershipView(mixins.CreateModelMixin, ListAPIView):
    queryset = Membership.objects.all()
    serializer_class = MembershipSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filter_fields = ('id',)
    search_fields = ('membership_type', 'slug')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class UserMembershipView(ListAPIView):
    queryset = UserMembership.objects.all()
    serializer_class = UserMembershipSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filter_fields = ('id',)
    search_fields = ('user', 'membership')


class SubscriptionView(ListAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    filter_backends = DjangoFilterBackend
    filter_fields = ('id',)
