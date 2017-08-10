from django.conf.urls import url

from gtnn_atc import views
from gtnn_atc.views import PersonalAutocomplete

urlpatterns = [
                url(r'^need/pl_add/$', views.pl_add, name='pl_add'),
                url(r'^need/personal-autocomplete/$', PersonalAutocomplete, name='personal-autocomplete'),
                url(r'^need/purpose/add/$', views.purp_add, name='purp_add'),
                url(r'^need/car/add/$', views.car_add, name='car_add'),
                url(r'^need/personal/(?P<pk>[0-9]+)/$', views.personal, name='personal'),
                url(r'^need/personal/(?P<pk>[0-9]+)/edit/$', views.personal_edit, name='personal_edit'),
                url(r'^need/route/add/$', views.route_add, name='route_add'),
                url(r'^need/address/add/$', views.address_add, name='address_add'),
                url(r'^need/only_our/$', views.only_our, name='only_our'),
                url(r'^need/word/(\d+)/$', views.word, name='word'),
                url(r'^need/copy/(\d+)/$', views.need_copy, name='need_copy'),
                url(r'^need/add/(\d+)/$', views.need_add, name='need_add'),
                url(r'^need/(?P<pk>[0-9]+)/edit/$', views.need_edit, name='need_edit'),
                url(r'^need/del/(\d+)/$', views.need_del, name='need_del'),
                url(r'^report_dep/$', views.atc_report_dep, name='report_dep'),
                url(r'^need/$', views.need_index, name='need'),
                url(r'^$', views.atc_index, name='index'),
                ]