from django.conf.urls import url
from .views import gb, send


urlpatterns = [
    url(r'^send/', send),
    url(r'^', gb),
]