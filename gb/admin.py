from django.contrib import admin
from gb.models import mesage
# Register your models here.
class mesage_admin (admin.ModelAdmin):
    list_display = ('tema', 'otzyv', 'ot_date')

admin.site.register(mesage, mesage_admin)