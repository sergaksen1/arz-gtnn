from django.contrib import admin
from gtnn_atc.models import MVZ, Address, Route, Purpose, Need, Car


class need_admin(admin.ModelAdmin):
    list_display = ('id', 'status', 'need_start_date', 'latest_date', 'address', 'route', 'need_type', 'dep', 'need_create_date', 'author')


admin.site.register(Car)
admin.site.register(MVZ)
admin.site.register(Address)
admin.site.register(Route)
admin.site.register(Purpose)
admin.site.register(Need, need_admin)