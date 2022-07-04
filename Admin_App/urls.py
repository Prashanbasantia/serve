from django.urls import path
from Admin_App import admin_views

urlpatterns = [
    path('dashboard', admin_views.dashboard, name='dashboard'),
    path('service-category', admin_views.service_category, name='admin_service_category'),
    path('service', admin_views.service, name='admin_service'),
    path('vender', admin_views.vender, name='admin_vender'),
    path('fetch_area', admin_views.fetch_area, name='fetch_area'),
    path('fetch_service_price', admin_views.fetch_service_price, name='fetch_service_price'),
    path('city', admin_views.city, name='admin_city'),
    path('area', admin_views.area, name='admin_area'),
]