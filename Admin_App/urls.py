from django.urls import path
from Admin_App import admin_views

urlpatterns = [
    path('dashboard', admin_views.dashboard, name='admin_dashboard'),
    path('service-category', admin_views.service_category, name='admin_service_category'),
    path('update_service_category', admin_views.update_service_category, name='admin_update_service_category'),
    path('venders', admin_views.vender, name='admin_vender'),
    path('vender/<str:id>', admin_views.vender_details, name='admin_vender_details'),
    path('customers', admin_views.customer, name='admin_customer'),
    path('customer/<str:id>', admin_views.customer_details, name='admin_customer_details'),
    path('orders', admin_views.order, name='admin_order'),
    path('order/<str:id>', admin_views.order_details, name='admin_order_details'),
    path('vender/update/profile/<str:id>', admin_views.update_vender_profile, name='admin_update_vender_profile'),
    path('vender/update/service/<str:id>', admin_views.update_service_price, name='admin_update_service_price'),
    path('fetch_area', admin_views.fetch_area, name='fetch_area'),
    path('fetch_service_price', admin_views.fetch_service_price, name='fetch_service_price'),
    path('city', admin_views.city, name='admin_city'),
    path('area', admin_views.area, name='admin_area'),
    path('profile', admin_views.admin_profile, name='admin_profile'),
    path('update/password', admin_views.admin_update_password, name='admin_update_password'),
]
