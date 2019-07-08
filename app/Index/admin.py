from django.contrib import admin

# Register your models here.
from .models import Users,Articles,Category,Leave

admin.site.register(Articles)
admin.site.register(Users)
admin.site.register(Leave)
admin.site.register(Category)
