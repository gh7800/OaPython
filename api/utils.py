from rest_framework.response import Response
from rest_framework import status


def success_response(data=None, message="操作成功", status_code=status.HTTP_200_OK):
    """成功响应"""
    response_data = {
        "code": status_code,
        "message": message,
        "data": data
    }
    return Response(response_data, status=status_code)


def error_response(error, message="操作失败", status_code=status.HTTP_400_BAD_REQUEST):
    """错误响应"""
    response_data = {
        "code": status_code,
        "message": message,
        "error": error
    }
    return Response(response_data, status=status_code)