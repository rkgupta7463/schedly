from django.urls import path
from .views import *


urlpatterns = [
    path('main/login/',login_view,name="main_login"),
    path('main/register/',register_user_view,name="main_register"),
    path('ajax/role-fields/', load_role_specific_fields, name='load_role_specific_fields'),

    path('main/logout/',logout_view,name="main_logout"),

    path('',index,name="home"),
    path('about-us/',about_us,name="about_us"),
    path('contact-us/',contact_us,name="contact_us"),
    path('services/',services,name="services"),
    path('doctor/',doctor_list,name="doctor"),
    path('department/',department_list,name="departments"),
]

