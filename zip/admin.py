from django.contrib import admin
from .models import Zip_types, Zip_locations, Zip_systems

class Zip_types_admin (admin.ModelAdmin):
    list_display = ('zipType_name', 'zipType_desc')

class Zip_locations_admin (admin.ModelAdmin):
    list_display = ('Loc_name',)

class Zip_systems_admin (admin.ModelAdmin):
    list_display = ('Sys_name',)


admin.site.register(Zip_types, Zip_types_admin)
admin.site.register(Zip_locations, Zip_locations_admin)
admin.site.register(Zip_systems, Zip_systems_admin)