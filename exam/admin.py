from django.contrib import admin
from .models import Property, UserProfile,Request

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('title', 'deal_type', 'price', 'rooms', 'area', 'user', 'created_at')
    list_filter = ('deal_type', 'rooms', 'created_at')
    search_fields = ('title', 'description', 'address')

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')
    list_filter = ('role',)
    search_fields = ('user__username',)

admin.site.register(Request)