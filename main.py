#!/usr/bin/env python
"""
OA办公系统后端管理脚本
用于启动、管理和维护办公系统服务
"""

import os
import sys
import argparse
from django.core.management import execute_from_command_line


def setup_django():
    """设置Django环境"""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'oa_backend.settings')


def start_server(host='127.0.0.1', port=8000, debug=False):
    """启动Django开发服务器"""
    setup_django()
    
    if debug:
        os.environ.setdefault('DEBUG', 'True')
    
    print(f"🚀 启动OA办公系统后端服务...")
    print(f"📡 服务器地址: http://{host}:{port}")
    print(f"🔧 调试模式: {'开启' if debug else '关闭'}")
    
    execute_from_command_line(['manage.py', 'runserver', f'{host}:{port}'])


def migrate_database():
    """执行数据库迁移"""
    setup_django()
    print("🗄️ 执行数据库迁移...")
    execute_from_command_line(['manage.py', 'migrate'])


def create_superuser():
    """创建超级用户"""
    setup_django()
    print("👤 创建超级用户...")
    execute_from_command_line(['manage.py', 'createsuperuser'])


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='OA办公系统后端管理工具')
    parser.add_argument('--host', default='127.0.0.1', help='服务器主机地址')
    parser.add_argument('--port', type=int, default=8000, help='服务器端口')
    parser.add_argument('--debug', action='store_true', help='开启调试模式')
    parser.add_argument('--migrate', action='store_true', help='执行数据库迁移')
    parser.add_argument('--createsuperuser', action='store_true', help='创建超级用户')
    
    args = parser.parse_args()
    
    try:
        if args.migrate:
            migrate_database()
        elif args.createsuperuser:
            create_superuser()
        else:
            start_server(args.host, args.port, args.debug)
    except KeyboardInterrupt:
        print("\n👋 服务已停止")
        sys.exit(0)
    except Exception as e:
        print(f"❌ 错误: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()