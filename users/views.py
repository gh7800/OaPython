from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
import logging
from .models import CustomUser
from .serializers import UserSerializer, RegisterSerializer, LoginSerializer, CustomTokenObtainPairSerializer
from api.utils import success_response, error_response

# 配置日志
logger = logging.getLogger(__name__)

class CustomTokenObtainPairView(TokenObtainPairView):
    """自定义 TokenObtainPairView，使用自定义序列化器"""
    serializer_class = CustomTokenObtainPairSerializer
    
    def post(self, request, *args, **kwargs):
        """处理 POST 请求"""
        try:
            return super().post(request, *args, **kwargs)
        except Exception as e:
            # 处理认证错误
            from django.contrib.auth import authenticate
            username = request.data.get('username') or request.query_params.get('username')
            password = request.data.get('password') or request.query_params.get('password')
            
            # 检查用户是否存在
            from .models import CustomUser
            try:
                user = CustomUser.objects.get(username=username)
                # 用户存在但密码错误
                return error_response(error="密码错误", message="登录失败", status_code=401)
            except CustomUser.DoesNotExist:
                # 用户不存在
                return error_response(error="用户名不存在", message="登录失败", status_code=401)


class UserViewSet(ModelViewSet):
    """用户管理视图集"""
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=['post'], permission_classes=[AllowAny], authentication_classes=[])
    def register(self, request):
        """用户注册"""
        # 优先使用请求体数据，如果没有则使用查询参数
        data = request.data or request.query_params.dict()
        serializer = RegisterSerializer(data=data)
        if serializer.is_valid():
            user = serializer.save()
            user_data = UserSerializer(user).data
            return success_response(data=user_data, message="注册成功", status_code=status.HTTP_201_CREATED)
        return error_response(error=serializer.errors, message="注册失败", status_code=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], permission_classes=[AllowAny], authentication_classes=[])
    def login(self, request):
        """登录"""
        try:
            data = request.data or request.query_params.dict()
            logger.info(f"Login request received: {data}")

            # 简化登录逻辑，直接验证用户名和密码
            username = data.get('username')
            password = data.get('password')

            if not username or not password:
                return error_response(error="用户名和密码不能为空", message="登录失败", status_code=status.HTTP_400_BAD_REQUEST)

            # 验证用户
            from django.contrib.auth import authenticate
            user = authenticate(username=username, password=password)

            if not user:
                return error_response(error="用户名或密码错误", message="登录失败", status_code=status.HTTP_401_UNAUTHORIZED)

            # 暂时返回简单的成功信息
            return success_response(data={"user": username}, message="登录成功", status_code=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Login error: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())
            return error_response(error=f"服务器内部错误: {str(e)}", message="登录失败", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'], permission_classes=[AllowAny], authentication_classes=[])
    def test(self, request):
        """测试接口"""
        try:
            return Response({"message": "测试成功", "status": "ok"}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Test error: {str(e)}")
            return Response({"error": "服务器内部错误"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)