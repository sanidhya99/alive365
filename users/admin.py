from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Register your models here.
class AppointmentAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Basic Info', {'fields': ('doctor','patient','time_slot')}),
        ('Patient Details', {'fields': ('phone','age','gender','description')}),
    )
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide'),
                'fields': ('doctor','patient','phone','age','gender','description', 'time_slot'),
            },
        ),
    )
    list_display = ('doctor','patient','phone','age','gender','time_slot')
    list_filter = ('age','gender','time_slot')
    search_fields = ('phone',)
    ordering = ('age','gender','time_slot')

admin.site.register(Appointments,AppointmentAdmin)
