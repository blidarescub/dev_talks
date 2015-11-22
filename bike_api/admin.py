from django.contrib import admin
from bike_api.models import (
    Users,
    Bikes,
    Location,
    Zone
)

# Register your models here.

class UsersAdmin(admin.ModelAdmin):
    pass

class BikesAdmin(admin.ModelAdmin):
    pass

class LocationAdmin(admin.ModelAdmin):
    pass

class ZoneAdmin(admin.ModelAdmin):
    pass

admin.site.register(Users, UsersAdmin)
admin.site.register(Bikes, BikesAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Zone, ZoneAdmin)
