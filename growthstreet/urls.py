from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(
        r'^accounts/',
        include('registration.backends.default.urls')
    ),
    url(r'^loans/', include('loans.urls')),
]
