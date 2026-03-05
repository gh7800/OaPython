from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    """自定义用户模型"""
    # 扩展字段
    # department = models.ForeignKey('departments.Department', on_delete=models.SET_NULL, null=True, blank=True)
    position = models.CharField(max_length=50, blank=True, verbose_name='职位')
    phone = models.CharField(max_length=20, blank=True, verbose_name='电话')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name='头像')

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '用户管理'
