from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    # This adds the 'role' field to the user edit page
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role',)}),
    )
    # This adds the 'role' column to the list view
    list_display = ['username', 'email', 'role', 'is_staff']

# Register the model
admin.site.register(CustomUser, CustomUserAdmin)