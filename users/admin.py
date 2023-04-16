from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import User, Home, HouseholdMembership

admin.site.register(User, UserAdmin)


class HouseholdMembershipInline(admin.TabularInline):
    model = HouseholdMembership
    extra = 1


@admin.register(Home)
class HomeAdmin(admin.ModelAdmin):
    inlines = [HouseholdMembershipInline]
    list_display = ("name", "mqtt_topic", "owners")

    def owners(self, obj):
        return ", ".join(str(x.user) for x in obj.owners())
