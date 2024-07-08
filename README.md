# ustc-database-lab

一个面向教师的教学科研登记系统的愚蠢的实现。

## 运行

### 通过 `docker`

运行以下指令，并通过 http://localhost:8000/ 查看效果。

```console
$ docker compose up -d
```

### 手动配置

如下创建数据库和用户，或者修改 [`config/settings.py`](config/settings.py) 中的 `DATABASES` 变量以使用其他数据库配置。

```mysql
CREATE DATABASE 'teacher_app';
CREATE USER 'teacher_app'@'localhost' IDENTIFIED BY 'teacher_app';
GRANT ALL PRIVILEGES ON teacher_app.* TO 'teacher_app'@'localhost';
```

运行以下指令，并通过 http://localhost:8000/ 查看效果。

```console
$ pip install -r requirements.txt
$ ./manage.py migrate
$ ./manage.py runserver
```
