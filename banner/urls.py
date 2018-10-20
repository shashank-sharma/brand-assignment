from django.conf.urls import url
from .views import home, banner, booking_edit, price_edit

urlpatterns = [
    url(r'^(?P<banner_id>[0-9]+)$', banner),
    url(r'^(?P<banner_id>[0-9]+)/booking/(?P<booking_id>[0-9]+)$', booking_edit),
    url(r'^(?P<banner_id>[0-9]+)/booking/add$', booking_edit),
    url(r'^(?P<banner_id>[0-9]+)/price/(?P<booking_id>[0-9]+)$', price_edit),
    url(r'^(?P<banner_id>[0-9]+)/price/add$', price_edit),
    url(r'', home),
]