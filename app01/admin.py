from django.contrib import admin

# Register your models here.




from app01.models import *

admin.site.register(UserInfo)
admin.site.register(ClassList)
admin.site.register(Customer)
admin.site.register(Campuses)
admin.site.register(ConsultRecord)