"""directory URL Configuration
"""
from django.conf.urls import url
from django.contrib import admin

from directory.views import address_by_key_value, address_by_key, address_list

urlpatterns = [
    url(r'^addresses/(?P<name>.+)/(?P<address>.+)/$',
        address_by_key_value),
    url(r'^addresses/(?P<name>.+)/$', address_by_key),
    url(r'^addresses/$', address_list),
    url(r'^admin/', admin.site.urls),
]
