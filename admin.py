from django.contrib import admin
from . models import Enquiry,Adminlogin,tbl_session,tbl_course,Student

# Register your models here.
admin.site.register(Enquiry)
admin.site.register(Adminlogin)
admin.site.register(tbl_session)
admin.site.register(tbl_course)
admin.site.register(Student)