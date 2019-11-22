from django.contrib import admin

# Register your models here.
from .models import Membership, UserMembership, Subscription

admin.site.register(Membership)
admin.site.register(UserMembership)


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user_membership', 'user_membership_type', 'active', 'email', 'created_at','updated', 'expired_at')
    #list_display_links = ('user_membership',)
    #search_fields = ('user_membership',)
    list_per_page = 25

    def user_membership_type(self, obj):
        return obj.user_membership.membership

    def email(self, obj):
        return obj.user_membership.user.email



admin.site.register(Subscription, SubscriptionAdmin)
