"""Core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path,include
from django.conf.urls.static import static
from Core import settings

urlpatterns = [ 
    path('',include("Index_App.urls")),
    path('admin/',include("Admin_App.urls")),
    path('vender/',include("Vender_App.urls")),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

# handler404 = 'Admin_App.admin_views.handler404'
# handler500 = 'Admin_App.admin_views.handler500'
# handler403 = 'Admin_App.admin_views.handler403'
# handler400 = 'Admin_App.admin_views.handler400'