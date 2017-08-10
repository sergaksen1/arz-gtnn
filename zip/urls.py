from django.conf.urls import url
from .views import hello, cat, add

urlpatterns = [
    url(r'^$', hello),
    url(r'^cat/$', cat, name='cat'),
    url(r'^add/$', add, name='add'),
]