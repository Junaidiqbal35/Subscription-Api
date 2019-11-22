from django.urls import path
from .api_view import MembershipView, MembershipCreate, UserMembershipView, SubscriptionView, \
    UserMembershipRetrieveUpdateDestroy
app_name = 'subscription'
urlpatterns = [
    path('membership/', MembershipView.as_view()),
    path('membership/new', MembershipCreate.as_view()),
    path('users/', UserMembershipView.as_view(), name='user-membership-list'),
    path('subscriber/', SubscriptionView.as_view()),
    path('users/<int:id>/', UserMembershipRetrieveUpdateDestroy.as_view(), name='user-membership'),
]