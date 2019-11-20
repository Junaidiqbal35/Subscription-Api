from django.contrib import admin

# Register your models here.
from .models import Membership, UserMembership, Subscription

admin.site.register(Membership)
admin.site.register(UserMembership)


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user_membership', 'active', 'created_at')
    list_display_links = ('user_membership',)
    # search_fields = ('subscription', 'user')
    list_per_page = 25


admin.site.register(Subscription, SubscriptionAdmin)
