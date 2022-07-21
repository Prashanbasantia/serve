from django.urls import path
from Vender_App import vender_views

urlpatterns = [
    path('dashboard', vender_views.vender_dashboard, name='vender_dashboard'),
    path('service', vender_views.vender_service, name='vender_service'),
    path('order', vender_views.order, name='vender_order'),
    path('profile', vender_views.vender_profile, name='vender_profile'),
    path('update/password', vender_views.vender_update_password, name='vender_update_password'),
    path('update/service', vender_views.update_service_price, name='vender_update_service_price'),
]