from django.contrib import admin

# Register your models here.
from .models import User, Article, Category, Leave

admin.site.register(Article)
admin.site.register(User)
admin.site.register(Leave)
admin.site.register(Category)
