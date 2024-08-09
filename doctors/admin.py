from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


class DoctorCategoryAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Field', {'fields': ('name',)}),
        ('Doctors', {'fields': ('doctors',)}),
    )
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide'),
                'fields': ('name', 'doctors'),
            },
        ),
    )
    list_display = ('name',)
    search_fields = ('name',)


class DoctorAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Basic Info', {'fields': ('name', 'email','phone')}),
        ('Professional Details', {'fields': ('category','qualification','qualification_doc','identity_doc','experience')}),
        ('General Details', {'fields': ('time_slot','price','location')}),
    )
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide'),
                'fields': ('name','phone','email',
                    'dob','location','gender','category','price','time_slot','qualification','experience','qualification_doc','identity_doc'),
            },
        ),
    )
    list_display = ('name','phone','email',
                    'dob','location','gender','category','price','time_slot','qualification','experience')
    list_filter = ('location','gender','price','time_slot','qualification','experience')
    search_fields = ('name', 'email','phone')
    ordering = ('location','price','time_slot','dob','category','qualification','experience')


admin.site.register(DoctorCategory, DoctorCategoryAdmin)
admin.site.register(Doctors, DoctorAdmin)