from django.urls import include, path
from api.v1.geo.urls import urlpatterns as geo_urls

urlpatterns = [
    path("geo/", include(geo_urls)),
]
