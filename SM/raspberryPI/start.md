https://www.raspberrypi.com/documentation

* 树莓派的各种系统有什么区别？

todo：

先连接个蓝牙键盘

[(1条消息) 树莓派链接蓝牙键盘_树莓派连接蓝牙键盘_Sazer的博客-CSDN博客](https://blog.csdn.net/Sazer/article/details/123462740)

可以配置树莓派自动连接WiFi

[无屏幕和键盘配置树莓派WiFi和SSH | 树莓派实验室 (nxez.com)](https://shumeipai.nxez.com/2017/09/13/raspberry-pi-network-configuration-before-boot.html)

[Pi Dashboard (Pi 仪表盘) - MAKE 趣无尽 (quwj.com)](https://make.quwj.com/project/10)

或者使用docker安装

```bash
sudo docker run -d --name docker-pi-dashboard -e 'LISTEN=1024' --net=host ecat/docker-pi-dashboard
```

安装dashboard，查看树莓派的各种状况


## 解决源问题


必须要用这个清华源：[debian | 镜像站使用帮助 | 清华大学开源软件镜像站 | Tsinghua Open Source Mirror](https://mirrors.tuna.tsinghua.edu.cn/help/debian/)


```
gpg --keyserver  keyserver.ubuntu.com --recv-keys E77FC0EC34276B4B
gpg --export --armor E77FC0EC34276B4B | sudo apt-key add -

# 另一种方法
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys E77FC0EC34276B4B


```


```
# 默认注释了源码镜像以提高 apt update 速度，如有需要可自行取消注释
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bullseye main contrib non-free
# deb-src https://mirrors.tuna.tsinghua.edu.cn/debian/ bullseye main contrib non-free

deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bullseye-updates main contrib non-free
# deb-src https://mirrors.tuna.tsinghua.edu.cn/debian/ bullseye-updates main contrib non-free

deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bullseye-backports main contrib non-free
# deb-src https://mirrors.tuna.tsinghua.edu.cn/debian/ bullseye-backports main contrib non-free

# deb https://mirrors.tuna.tsinghua.edu.cn/debian-security bullseye-security main contrib non-free
# # deb-src https://mirrors.tuna.tsinghua.edu.cn/debian-security bullseye-security main contrib non-free

deb https://security.debian.org/debian-security bullseye-security main contrib non-free
# deb-src https://security.debian.org/debian-security bullseye-security main contrib non-free
```


安装aptitude

apt install aptitude


安装官方指定的包：

aptitude install apparmor jq wget curl udisks2 libglib2.0-bin network-manager dbus lsb-release systemd-journal-remote systemd-resolved 


安装docker 

curl -fsSL get.docker.com | sh


配置NetworkMananger

systemctl enable NetworkManager
systemctl is-enabled NetworkManager

nmcli device wifi connect Avengerss password qwertYUIOP


grub 配置：

apt install --reinstall grub2-common


## 杂项


解决树莓派安装openwrt后无法上国内网站的问题

1.LAN口取消桥接；
2.防火墙添加"iptables -t nat -I POSTROUTING -o eth0 -j MASQUERADE"，重启防火墙，立马就能访问了，以上两项步骤缺一不可。


sshfs 可以透过 ssh 连接挂载文件系统。f


查看PI4B 版本

```shell
dmesg | grep 'Machine model'
```

