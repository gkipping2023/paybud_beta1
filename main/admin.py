from django.contrib import admin
from .models import Users, Logbook, Aircraft_Type, User, PilotRank
# Register your models here.

admin.site.register(User)
admin.site.register(Users)
admin.site.register(Logbook)
admin.site.register(Aircraft_Type)
admin.site.register(PilotRank)