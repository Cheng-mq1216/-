# 网络问答与资源共享平台
使用 Django

首次运行需要准备开发环境：
```bash
$ pip install -r requirements/development.txt
$ python manage.py migrate
$ python manage.py createsuperuser 
```

可以调用`python manage.py seed`生成一个管理员账户密码和一些随机的数据。

调用`python manage.py flush`删除数据库中的所有数据。

### 开发运行：
```bash
$ python manage.py runserver
```

### 部署：
自动化部署是一项复杂的流程。我们采取相对简单的一种方式：使用Docker进行部署。相关的文件置于`config`文件夹中。

我们将Django应用打包为一个容器。配套的静态Web服务器Nginx和数据库MySQL各自打包为一个容器，并使用`docker-compose.yml`实现多容器在单机上的编排。

我们需要在项目根目录下建立一个.env文件，包括：

* `SECRET_KEY` 密钥，可以随机生成
* `MYSQL_ROOT_PASSWORD` 数据库root账号密码
* `MYSQL_USER` 使用的登录账号，可以为root
* `MYSQL_PASSWORD` 登录的密码
* `MYSQL_DATABASE` 使用的数据库名，项目的配置为django
* `SERVER_NAME` 远程主机名称
* `SERVER_IPADDR` 远程主机ip地址

之后在本机上运行：
```
config/deploy.sh
```
即可。要求在远程主机上已配置docker-compose。并保持80端口未被占用。

远程主机上运行
```
docker-compose up -d
```
时会自动拉取所需依赖。数据库文件存放在`./data`中，静态文件存放在`./static`中。

首次部署时需要手动添加超级用户。在远程服务器项目根目录执行以下指令：
```
docker-compose exec web python manage.py createsuperuser
```

如果数据库中出现了迁移系统难以解决的问题，可以在项目根目录调用`config/reboot.sh`以重启数据库。注意，此时数据库中所有内容将会被删除，且需要重新添加超级用户。

### 未来的目标：

* 自动化部署：使用Jenkins
* 分布式编排：使用kubernates完成自动化部署。
* 单元测试：使用 Selenium 构建测试用例，并尝试采用测试驱动开发。
* 持续集成：每次 GitHub Commit 时自动运行测试，并拒绝未能通过测试的更改。
