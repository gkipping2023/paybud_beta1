from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Users, Logbook, Aircraft_Type, User, PilotRank, Airports

class CustomUserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('cmp_id', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Pilot Info', {'fields': ('position', 'custom_disc_1', 'custom_disc_1_name', 
                                   'custom_disc_2', 'custom_disc_2_name',
                                   'custom_disc_3', 'custom_disc_3_name',
                                   'custom_disc_4', 'custom_disc_4_name',
                                   'custom_disc_5', 'custom_disc_5_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('cmp_id', 'password1', 'password2'),
        }),
    )
    list_display = ('cmp_id', 'email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('cmp_id', 'email', 'first_name', 'last_name')
    ordering = ('cmp_id',)

admin.site.register(User, CustomUserAdmin)
admin.site.register(Users)
admin.site.register(Logbook)
admin.site.register(Aircraft_Type)
admin.site.register(PilotRank)
admin.site.register(Airports)