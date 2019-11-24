from django.urls import path
from .views import MembershipView, MembershipCreate, UserMembershipView, SubscriptionView, \
    UserMembershipRetrieveUpdateDestroy, ReminderSubscriberView, SubscriptionRetrieveUpdateDestroy
app_name = 'subscription'
urlpatterns = [
    path('membership/', MembershipView.as_view()),
    path('membership/add/', MembershipCreate.as_view()),
    path('users/', UserMembershipView.as_view(), name='user-membership-list'),
    path('subscriber/', SubscriptionView.as_view()),
    path('update/<int:pk>/', SubscriptionRetrieveUpdateDestroy.as_view()),
    path('reminder/', ReminderSubscriberView.as_view()),
    path('users/<int:id>/', UserMembershipRetrieveUpdateDestroy.as_view(), name='user-membership'),
]