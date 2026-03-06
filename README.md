## OaPython项目 Django框架

#### 1、Python语言基础
- 1.1 变量
- 1.2 数据类型

#### 2、Python数据类型
- 2.1整数 int
- 2.2浮点数 float
- 2.3字符串 str
- 2.4列表 list
- 2.5元组 tuple
- 2.6字典 dict
- 2.7集合 set

#### 3、虚拟环境

- 3.1激活虚拟环境 .venv\Scripts\activate
- 3.2退出虚拟环境 deactivate

#### 4、依赖管理

- 4.1添加依赖 uv add 包名 (例如: `uv add django`)
- 4.2查看依赖 uv list
- 4.3同步依赖 uv sync (根据pyproject.toml同步)

#### 5、运行项目

- 5.1运行项目 python main.py (例如: `python main.py`)
- 5.2运行项目 python main.py --port 8080 (例如: `python main.py --port 8080`)
- 5.3运行项目 python main.py --port 8080 --debug (例如: `python main.py --port 8080 --debug`)
- 5.4运行项目 python main.py --port 8080 --debug --host 0.0.0.0 (例如: `python main.py --port 8080 --debug --host 0.0.0.0`)

#### 6、项目框架

- 6.1项目框架
    - 6.1.1项目目录结构
    - 6.1.2项目文件结构

#### 7、项目配置

- 7.1超级管理员admin admin
- 7.2数据库配置 postgresql

#### 8、常用命令

- 8.1创建数据库 python manage.py migrate
- 8.2创建超级管理员 python manage.py createsuperuser (例如: `python manage.py createsuperuser`)
- 8.3添加django 应用 python manage.py startapp 应用名 (例如: `python manage.py startapp users`)
- 8.4添加应用并指定目录 python manage.py startapp users apps/users (例如: `python manage.py startapp users apps/users`)

#### 9、django框架

- 9.1安装django  ( uv install django) (例如: `uv install django`)
- 9.2生成迁移文件 python manage.py makemigrations users (例如: `python manage.py makemigrations users`)
- 9.3执行迁移 python manage.py migrate (例如: `python manage.py migrate`)
  
