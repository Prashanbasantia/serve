# Index App urls file

from django.urls import path
from Index_App import index_views

urlpatterns = [
    path('', index_views.home, name='home'),
    path('login/', index_views.login, name='login'),
    path('logout/', index_views.logout, name='logout'),
    path('signup/', index_views.signup, name='signup'),
    path('create_user_account/', index_views.create_user_account, name='create_user_account'),
    path('aboutus/', index_views.aboutus, name='aboutus'),
    path('contactus/', index_views.contactus, name='contactus'),
    path('pricing/', index_views.pricing, name='pricing'),
    path('faq/', index_views.faq, name='faq'),
    path('service/', index_views.service, name='service'),
    path('service/<str:id>', index_views.service_details, name='service_details'),
    # authenticate  View 
    path('account/', index_views.account, name='account'),
]