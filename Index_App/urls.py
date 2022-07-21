# Index App urls file

from django.urls import path
from Index_App import index_views

urlpatterns = [
    path('', index_views.home, name='home'),
    path('login/', index_views.login, name='login'),
    path('logout/', index_views.logout, name='logout'),
    path('signup/', index_views.signup, name='signup'),
    path('signup/vender/', index_views.signup_vender, name='signup_vender'),
    path('verify/signup/vender/', index_views.verify_signup_vender, name='verify_signup_vender'),
    path('create/user/account/', index_views.create_vender_account, name='create_vender_account'),
    path('create_user_account/', index_views.create_user_account, name='create_user_account'),
    path('aboutus/', index_views.aboutus, name='aboutus'),
    path('contactus/', index_views.contactus, name='contactus'),
    path('faq/', index_views.faq, name='faq'),
    path('service/', index_views.service, name='service'),
    path('service/<str:id>', index_views.service_details, name='service_details'),
    # authenticate  View 

    path('account/', index_views.account, name='account'),
    path('orders/', index_views.orders, name='orders'),
    path('profile/', index_views.profile, name='profile'),
    path('profile/change_password/', index_views.change_password, name='change_password'),
    path('profile/change_address/', index_views.change_address, name='change_address'),
    path('session_clear/', index_views.session_clear, name='session_clear'),
    path('service/order/<str:id>/', index_views.service_order, name='service_order'),
    path('service/order/info/<str:id>/', index_views.service_order_info, name='service_order_info'),
]