from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from .models import Member

class CustomUserAdmin(DefaultUserAdmin):
    # Use the existing fieldsets and add custom fields where needed
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions', 'groups'),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        # Add any additional custom fields here if needed
    )

    # Optionally, you can override add_fieldsets to include custom fields on the add user form
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'first_name', 'last_name', 'email', 'groups'),
        }),
    )

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Member)
