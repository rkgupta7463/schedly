from django.urls import path
from .views import *

urlpatterns = [
    path('book/appoinment/',book_appoinment,name="book_appoinment")
]

