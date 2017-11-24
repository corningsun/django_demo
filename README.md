# django_demo

django 示例项目，增加了基于 jwt 的 token 验证功能。

## 环境依赖
* python2
* pip

## 项目安装

1. `git clone .../django_demo.git`
2. `cd django_demo`
3. `pip install -r requirements.txt`
4. `python manage.py runserver 0.0.0.0:8000`

## 数据库相关
默认sqlite数据，如果需要使用其他数据库，可以修改`demo/settings.py/DATABASES`

```python
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'django_demo',
#         'USER': 'root',
#         'PASSWORD': '19890720',
#         'HOST': '127.0.0.1',
#         'PORT': '3306',
#     },
# }
```

> 切换新的数据库后，注意需要执行 `python manage.py migrate`

## 接口测试

[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/a610be1c75f39c7e167c)

### 登陆
请求

http://127.0.0.1:8000/demo/privilege/login/

Post 参数

```json
{
	"username": "demo",
	"password": "demo",
	"remember": "True"
}
```

返回

```json
{
    "info": {
        "username": "demo",
        "token": "eyJhbGciOiJIUzI1NiJ9.eyJpYXQiOiIyMDE3LTExLTIzIDA5OjA4OjAxIiwicm9sZSI6MSwicmVtZW1iZXIiOiJUcnVlIiwiZnJvbV91c2VyIjoxfQ.BKGCGOTKoKr88so0t88HlyBGSUQIe6V-3ZJICpoBGFw",
        "userId": 1
    },
    "message": "success",
    "code": 200
}
```
### hello
 
请求

`hello/(?P<name>\w+)/`

http://127.0.0.1:8000/demo/hello/world/

返回

```json
{
    "info": "Hello world",
    "message": "success",
    "code": 200
}
```
