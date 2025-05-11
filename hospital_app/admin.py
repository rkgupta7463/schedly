from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Hospital)
admin.site.register(HospitalImage)
admin.site.register(HospitalReview)