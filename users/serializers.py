from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    """用户序列化器"""
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'position', 'phone', 'avatar']

class RegisterSerializer(serializers.ModelSerializer):
    """注册序列化器"""
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'password2', 'first_name', 'last_name', 'position', 'phone']
    
    def validate(self, attrs):
        """验证密码"""
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "两次密码输入不一致"})
        return attrs
    
    def create(self, validated_data):
        """创建用户"""
        validated_data.pop('password2')
        user = CustomUser.objects.create_user(**validated_data)
        return user

class LoginSerializer(serializers.ModelSerializer):
    """登录序列化器"""
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True, style={'input_type': 'password'})

    class Meta:
        model = CustomUser
        fields = ['username', 'password']

    def validate(self, attrs):
        """验证用户"""
        username = attrs.get('username')
        password = attrs.get('password')

        user = authenticate(username=username, password=password)
        if not user:
            raise serializers.ValidationError({"error": "用户名或密码错误"})

        # 生成 token
        refresh = RefreshToken.for_user(user)

        # 序列化用户信息，处理 avatar 字段
        user_data = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "position": user.position,
            "phone": user.phone,
            "avatar": user.avatar.url if user.avatar else None
        }

        return {
            "message": "登录成功",
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": user_data
        }


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """自定义 TokenObtainPairSerializer，支持从查询参数获取数据"""

    def validate(self, attrs):
        # 首先尝试从请求体获取数据
        if not attrs.get('username') or not attrs.get('password'):
            # 如果请求体中没有数据，尝试从查询参数获取
            request = self.context.get('request')
            if request:
                attrs['username'] = attrs.get('username') or request.query_params.get('username')
                attrs['password'] = attrs.get('password') or request.query_params.get('password')

        # 尝试验证用户
        try:
            # 调用父类的 validate 方法获取 token
            data = super().validate(attrs)

            # 添加用户信息
            user = self.user
            user_data = {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "position": user.position,
                "phone": user.phone,
                "avatar": user.avatar.url if user.avatar else None
            }

            # 构建符合 REST API 结构的响应
            response_data = {
                "code": 200,
                "message": "登录成功",
                "data": {
                    "access": data['access'],
                    "refresh": data['refresh'],
                    "user": user_data
                }
            }

            return response_data
        except Exception as e:
            # 直接抛出原始错误，让视图层面处理
            raise