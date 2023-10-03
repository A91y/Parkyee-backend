from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework.documentation import include_docs_urls
# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
#     TokenRefreshView,
# )

router = routers.DefaultRouter()
from . import views

router.register(r'parking', views.ParkingViewSet)
router.register(r'parkingavailability', views.ParkingAvailabilityViewSet)
router.register(r'parkingslot', views.ParkingSlotViewSet)
# router.register(r'parking/(?P<parking_id>\d+)/slots', views.ParkingSlotListView, basename='parking-slots')
router.register(r'parking/(?P<parking_id>\d+)/slots/(?P<unique_id>\w+)', views.ParkingSlotDetailView, basename='parking-slot-detail')
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('parking/<int:parking_id>/slots/', views.ParkingSlotListView.as_view({'get': 'list'}), name='parking-slots'),
    path('docs/', include_docs_urls(title='Parkyee API'))
]

# urlpatterns += [
#     path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
#     path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
#     path('me/', views.MeView.as_view(), name='me'),
# ]
