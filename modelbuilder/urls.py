from django.urls import path
from .views import *

from rest_framework import routers

app_name = 'modelbuilder'


router = routers.DefaultRouter()
router.register('', ModelBuilderViewset,basename='modeluilder')
# router.register('weather',WeatherView)
# router.register('location',LocationsView)
# router.register('crops',CropView)


urlpatterns = [
  
]

urlpatterns += router.urls
