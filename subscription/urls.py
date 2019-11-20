from django.urls import path
from .api_view import MembershipView, UserMembershipView, SubscriptionView
urlpatterns = [
    path('api/membership/', MembershipView.as_view()),
    path('api/users/', UserMembershipView.as_view()),
    path('api/subscription/', SubscriptionView.as_view()),
]