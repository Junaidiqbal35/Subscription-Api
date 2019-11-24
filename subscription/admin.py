from django.contrib import admin

# Register your models here.
from .models import Membership, UserMembership, Subscription


class MembershipAdmin(admin.ModelAdmin):
    list_display = ('membership_type', 'price','active','interval')
    list_display_link = ('membership_type',)
    search_fields = ('membership_type',)


class UserMembershipAdmin(admin.ModelAdmin):
    list_display = ('user', 'membership')
    list_display_link = ('user',)
    search_fields = ('membership',)

    def membership(self, obj):
        return obj.membership.membership_type


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user_membership', 'user_membership_type', 'active', 'email', 'created_at',
                    'updated', 'expired_at')
    list_display_links = ('user_membership',)
    search_fields = ('created_at',)
    list_per_page = 25

    def user_membership_type(self, obj):
        return obj.user_membership.membership

    def email(self, obj):
        return obj.user_membership.user.email


admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(UserMembership, UserMembershipAdmin)
admin.site.register(Membership, MembershipAdmin)
