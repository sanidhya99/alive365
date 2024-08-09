from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

class CustomUserAdmin(BaseUserAdmin):
    list_display = ('name','phone','email','dob','location','gender')
    list_filter = ('location','gender','dob')
    fieldsets = (
        ('User Credentials', {'fields': ('name','phone','location')},),
        ('Personal info', {'fields': ('email','gender','dob','blood_group','marital_status','height','weight','emergency_contact')},),
        ('Permissions', {'fields': ('is_superuser',)},),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide'),
                'fields': ('name','phone','location','email','gender','dob','blood_group','marital_status','height','weight','emergency_contact'),
            },
        ),
    )
    search_fields = ('email','name','phone')
    ordering = ('dob','location','gender')
    filter_horizontal = ()

admin.site.register(CustomUser,CustomUserAdmin)