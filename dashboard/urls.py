from django.urls import path
from .views import *

urlpatterns = [
    path("logout/",logout_view,name="logout"),
    path("accounts/login/", custom_login_view, name="login_admin"),
    path("",index,name="index"),
    
    ############  USERS
    path('users/', users, name="users"),
    path('change/password/<int:uid>/', changepassword_view, name="change_password"),
    path('reset/password/<int:uid>/', rest_password_view, name="reset_password"),
    path('users/filtered/',  users_filtered, name="users_filtered"),
    path('ajax_datatable/projects/filter/', UserProfileDatatableView.as_view(), name="ajax_datatable_users_filter_list"),
    path('users/add/', createUser, name="add_user"),
    path('users/<int:uid>/edit/', createUser, name="edit_user"),
    path('users/<int:uid>/password/', set_password_user, name="set_password_user"),
    path('users/<int:uid>/edit/active/', userState, name="user_edit_active"),
    
    ####### Specialization's url 
    path('specialization/', specialization, name="specialization"),
    path('specialization/filtered/',  specializations_filtered, name="specializations_filtered"),
    path('ajax_datatable/specialization/filter/', SpecializationsDatatableView.as_view(), name="ajax_datatable_specializations_filter_list"),
    path('hospital/add/', add_specialization_edit, name="add_specialization"),
    path('hospital/<int:sid>/edit/', add_specialization_edit, name="edit_specialization"),
    
    ####### Specialization's url 
    path('specialization/', specialization, name="qualification"),
    path('specialization/filtered/',  specializations_filtered, name="qualification_filtered"),
    path('ajax_datatable/specialization/filter/', SpecializationsDatatableView.as_view(), name="ajax_datatable_qualifications_filter_list"),
    path('hospital/add/', add_specialization_edit, name="add_qualification"),
    path('hospital/<int:sid>/edit/', add_qualification_edit, name="edit_qualification"),
    
    
    ####### qualification's url 
    path('qualification/', qualification, name="qualification"),
    path('qualification/filtered/',  qualifications_filtered, name="qualifications_filtered"),
    path('ajax_datatable/qualification/filter/', QualificationsDatatableView.as_view(), name="ajax_datatable_qualifications_filter_list"),
    path('qualification/add/', add_qualification_edit, name="add_qualification"),
    path('qualification/<int:sid>/edit/', add_specialization_edit, name="edit_qualification"),
    
    ############  hospital's url 
    path('hospitals/', hospital, name="hospitals"),
    path('hospital/filtered/',  hospitals_filtered, name="hospitals_filtered"),
    path('ajax_datatable/hospital/filter/', HospitalsDatatableView.as_view(), name="ajax_datatable_hospitals_filter_list"),
    path('hospital/add/', add_hospital_edit, name="add_hospital"),
    path('hospital/<int:hid>/detail/', hospital_detail, name="hospital_detail"),
    path('hospital/<int:hid>/edit/', add_hospital_edit, name="edit_hospital"),
    path('add/hospital/<int:hid>/image/', additional_hospital_img, name="add_hospital_img"),
    path('edit/hospital/<int:hid>/image/<int:pid>/', additional_hospital_img, name="edit_hospital_img"),
]