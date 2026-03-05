from django.contrib import admin
from .models import CustomUser

@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    """用户管理后台配置"""
    list_display = ['username', 'email', 'first_name', 'last_name', 'position']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    list_filter = ['username']