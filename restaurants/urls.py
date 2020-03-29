from django.urls import include, path
from rest_framework import routers

from restaurants import views

router = routers.DefaultRouter()
router.register(r'restaurants', views.RestaurantViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('geo_restaurants.geojson', views.restaurants_geojson),
]