# Docker

## 安装

```
bcdedit /set hypervisorlaunchtype auto
将windows 这个打开 ，并启用 Hyper-V,但是这个会和VM冲突
```



## 守护进程

user <--->  Docker CLI   <====>   Docker 守护进程

> docker 是 C/S模式

### remote api

restful 风格连接

### 连接方式 socket

```
unix:///var/run/docker.sock
tcp://host:port
fd://docketfd
```

```
nc -U /var/run/docker.sock
GET /info HTTP/1.1
```

### 运行状态

```
ps | grep docker
```

修改守护守护进程配置文件

```
vim /etc/default/docker
```

### 远程访问

```
修改 docker配置文件，添加
-H tcp://ip:port
重启服务
访问：http://ip:port/info
```

客户端访问

```
docker -H tcp://ip:port info
```

添加环境变量 

```
export DOCKER_HOST="tcp://ip:port"
就可以不用再加-H选项 
```



## Docker的启动于停止

```
systemctl start docker
```

```
systemctl stop docker
```

```
systemctl restart docker
```

```
systemctl status docker
```

开机启动

```
systemctl enable docker
```

查看docker信息

```
docker inf
```


帮助文档

```
docker --help
```

## 镜像命令

#### 镜像列表

```
docker images
```

#### 搜索镜像

```
docker search 镜像名称
```

#### 拉取镜像

```
docker pull
```

#### 删除镜像

```
docker rmi 镜像id
```

#### 删除所有镜像

```
docker rmi `docker images -q`
```
#### 查看日志

```
docker logs
```
## 容器命令

#### 查看容器

-a 不管是否运行

```
docker ps
```

#### 创建容器

-i 运行容器

-t 交互式运行，进入命令行

--name 为容器命名

-v 目录映射

-d 守护方式运行 （创建后不会自动登录容器，而是在后台）

-p 表示端口映射

> docker run -di --name=sst -p 8080:80  //通过宿主机8080访问容器80端口

```
docker run -it
```

> docker run -it --name=mycentos centos:7 /bin/bash

#### 启动容器

```
docker start Cid
```

#### 停止容器

```
docker stop Cid
```

```
docker kill Cid
```

#### 删除容器

-v 删除容器的同时删除数据卷（如果数据卷被使用则不会被删除）

```
docker rm Cname/Cid
```

####  执行容器命令

```
docker exec [comman]
```

#### 附加容器 

> 从后台转至前台

```
docker attach Cname
```



#### 文件拷贝

```
docker cp [文件] Cname:[容器路径]
```

支持反向copy

### 目录挂载:数据卷

> docker 数据卷 是经过特殊设计的目录，可以绕过联合文件系统（UFS），为一个或者多个容器服务，其设计目的在于数据的永久化，它独立于docker的生命周期。

创建容器  添加 -v 参数  宿主机目录:容器目录

```
docekr run -di -v /usr/local:/usr/local --name=mycentos centOS:7
```

多级目录权限问题  加参数 --privileged=true

使用docker inpect 可以查看  Volumes 配置

```
Volumes:{"/data":"/data"}
VolumesRW:{
"/data":true
}
```



#### 权限设置

```
docker run -di -v /usr/local:/usr/local:ro(read only) --name=mycentos centOS:7
```

#### 数据卷容器

挂载方法

```
docker run --volumes-from CnameWithHaveVolume
```

新的容器就会挂载和指定容器同样的数据卷



### 查看容器信息

```
docker inspect Cid
```

可以查看容器各种信息

--format='{{.NetworkSettings.IPAddress}}' 可以指定查看项

## Docker 网络

linux 虚拟网桥的特点

* 可以设置ip
* 相当于拥有一块隐藏的虚拟网卡

网桥管理工具

```
apt-get install bridge-utils
```

显示网桥

```
sudo brctl show
```

创建网桥

```
brctl addbr eth3
ifconfig eth3 IP 
```

设置docker 配置

```sh
vim /etc/default/docker
添加
DOCKER_OPTS="-b=eth3"
```

### 容器互联

每次启动容器，docker的ip都会改变

```sh
docker run --link=sst:aliasName ubuntu
docker ping aliasName
实际上是在hosts中添加了aliasName 的地址映射
映射地址会自动在重启后修改
```

#### 拒绝容器互联

```sh
修改默认守护进程配置
DOCKER_OPTS="--icc=false"
```

#### 特定互联

```sh
--icc=false --iptables=true
--link
仅仅允许link配置的容器进行访问
```

查看iptables

```
iptables -L -n
```

查看 ip_forword  （是否进行流量转发）

```
sudo sysctl net.opv4.all.forwording
```



## 应用部署

### mysql

1.拉取镜像

```
docker pull centos/mysql-57-centos7
```

2.创建容器

```
docker run -di --name=sst -p 33306:3306 -e MYSQQL_ROOT_PASSWORD=123456 Cname
```

3.可以用33306远程登录mysql

### Tomcat

拉取镜像

```
docker pull tomcat:7-jre7
```

创建容器

```
docker run -di --name=mytomcat -p 8088:8080 -v /usr/local:/usr/tomcat Cname
```

### Nginx

拉取镜像

```
docker pull nginx
```

创建容器

```
docker run -di ---name=myngnix -p 80:80 nignx
```

### Redis

拉取镜像

```
docker pull redis
```

创建容器

``` 
docker run -di --name=myredis -p 6379:6379 redis
```



## 备份与迁移

将现有容器保存为镜像

```
docker commit old_Cname new_Cname
```

保存镜像为文件

```
docker save -o fileName.tar Iname
```

文件恢复镜像

```
docker load -i fileName.tar
```

## DockerFile

docker 是由一些列命令和参数构成的脚本，这些命令应用于基础镜像

### 常用命令

| 命令                                | 作用                                                         |
| ----------------------------------- | ------------------------------------------------------------ |
| FROM image_name:tag                 | 定义使用那些基础镜像构建流程恩                               |
| MAINTAINER user_name                | 声明镜像的创建者                                             |
| ENV key value                       | 设置环境变量（可以写多条）                                   |
| RUN command                         | 核心部分                                                     |
| ADD source_dir/file dest_dir/file   | 将宿主机的文件复制到容器内，如果是一个压缩文件，将会自动解压 |
| COPY sorcery_dir/file dest_dir/file | 同上，只不过不解压                                           |
| WORKDIR path_dir                    | 设置工作目录                                                 |

### Demo

```
FROM centos:7
MAINTAINER sst
WORKDIR /usr
RUN mkdir /usr/local/java
ADD your_file.gz
ENV JAVA_HOME=/usr/local/jaa/jdk1.8.0_171
ENV JRE_HOME $JAVA_HOME/jre
ENV CLASSPATH $JAVA_HOME/bin/dt.jar:$JAVA_HOME/lib/tools.jar:$JAR_HOME/lib:$CLASSPATH
ENV PATH$JAVA_HOME/bin:$PATH

```

#### 构建

```
docker build -t='Cname' .
```

## 私有仓库

### 创建私有仓库

1.  拉取私有仓库镜像

```
docker pull registry
```

2. 启动私有仓库

```
docker run -di --name=registry -p 5000:5000 registry
```

   3.访问仓库

```
http://Chost:5000/v2/_catalog
```

如果能看到{"repositories:[]"} 表示成功

4. 让docker 信任本地仓库

```json
修改 deamon.json
{
“registry-mirrors":["https://docker.mirros.ustc.edu.cn"],
"insecure-registries":["192.168.184.141:5000"]
}
```

### 上传私有仓库

1. 打标签

```
docker tag Coldname CnewName
```

2. 上传

```
docker push 私服地址:port/Cname
```

要先开启registry 私服


## docker 跨主机连接

### 网桥

> 配置复杂，不适合生产环境

### open vSwitch

> 高质量，多层虚拟交换机，使用开源Apache2.0 协议，主要C实现

使用GRE隧道进行连接

> gre: 通用路由协议封装。隧道技术是一种可通过使用互联网的基础设施在网络之间产地数据的方式。隧道协议将其它协议的数据帧或包重新封装然后通过隧道发送。  

安装方式：

```
apt-get install openvswitch-switch
```

### weave

会在docker 中开启一个weave容器





















































