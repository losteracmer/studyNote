# OpenWRT

## install in raspberry pi

[blog](https://www.cfmem.com/2021/08/docker-openwrt.html)

* 配置网卡混淆

```shell
ip link set eth0 promisc on
```

* 创建docker网络

```shell
docker network create -d macvlan --subnet=192.168.31.0/24 --gateway=192.168.31.1 -o parent=eth0 macnet

# or 如果网关是 192.168.1.1
docker network create -d macvlan --subnet=192.168.1.0/24 --gateway=192.168.1.1 -o parent=eth0 macnet
```


* 运行docker容器

```shell
docker run --restart always --name openwrt -d --network macnet --privileged registry.cn-shanghai.aliyuncs.com/suling/openwrt:rpi4 /sbin/init
```

* 设置容器IP 

```shell
# 进入容器
docker exec -it openwrt bash
```

编辑 /etc/config/netwrok
```
config interface 'lan'
        option type 'bridge'
        option ifname 'eth0'
        option proto 'static'
        option netmask '255.255.255.0'
        option ip6assign '60'
        option ipaddr '192.168.1.222'
        option gateway '192.168.1.1'
        option dns '192.168.1.1'
```
> 其中 option ipaddr 是你的 openwrt 的地址，注意不要与局域网其它设备冲突 

```shell
# 重启容器网络
/etc/init.d/network restart 
```

* 配置OpenWrt


进入[V2free](https://w1.v2ai.top/user)机场，登录后进入[配置页](https://w1.v2ai.top/doc/#/Router/OpenWRT)，复制第一个V2ray地址

http://192.168.1.222 默认密码是 password。 进入【服务】【SSR plus】【服务节点管理】将订阅网址进行粘贴。点击 【更新所有订阅服务节点】后保存。回到【客户端】，选择主服务器(US)后保存&应用


* 配置客户端

手机：
将wifi的网络设置改为静态，配置网关（和dns）为刚刚的wrt地址。

## 解决和宿主机无法联网的问题

> 原因是部署 openWRT 系统时使用到了 docker 的 macvlan 模式，这个模式通俗一点讲就是在一张物理网卡上虚拟出两个虚拟网卡，具有不同的MAC地址，可以让宿主机和docker同时接入网络并且使用不同的ip，此时 docker 可以直接和同一网络下的其他设备直接通信，相当的方便，但是这种模式有一个问题，宿主机和容器是没办法直接进行网络通信的，如宿主机ping容器的ip，尽管他们属于同一网段，但是也是ping不通的，反过来也是。因为该模式在设计的时候，为了安全禁止了宿主机与容器的直接通信，不过解决的方法其实也很简单——宿主机虽然没办法直接和容器内的 macvlan 接口通信，但是只要在宿主机上再建立一个 macvlan，然后修改路由，使数据经由该 macvlan 传输到容器内的 macvlan 即可，macvlan 之间是可以互相通信的。

* 创建mac vlan网卡

```shell
ip link add mynet link eth0 type macvlan mode bridge
# 31.100需要是同一个网段
ip addr add 192.168.1.100 dev mynet
ip link set mynet up
# 添加路由，走到OpenWRT内的网络走mynet网卡
ip route add 192.168.1.200 dev mynet
```

* 重启时自动执行

```shell
# 写入到 /etc/rc.local中

chmod a+x /etc/rc.local

## 让宿主机的网关改为OpenWRT，因为这样Metrix是0，所以相比其它默认路由优先级更高

ip route add default dev mynet via 192.168.1.222
```

> 删除指令：`route del default via mynet`


## install in router xiaomi AC2100
> [主要参考](https://www.bilibili.com/read/cv18237601/)


[固件下载地址](https://openwrt.org/zh/toh/views/toh_fwdownload?dataflt%5BModel*%7E%5D=AC2100)
> 包含kernel 和 rootfs两个

[低包下载地址](https://downloads.openwrt.org/releases/22.03.5/targets/ramips/mt7621/)

1. 首先要回退版本到一个'漏洞'版本


[红米AC2100](http://cdn.cnbj1.fds.api.mi-img.com/xiaoqiang/rom/rm2100/miwifi_rm2100_firmware_d6234_2.0.7.bin)

[小米AC2100](http://cdn.cnbj1.fds.api.mi-img.com/xiaoqiang/rom/r2100/miwifi_r2100_firmware_4b519_2.0.722.bin)


登录路由器后台，指定包刷回。


2. 打开路由器ssh登录

刷完后登录后台，从浏览器栏获取stok，并替换下面的链接中的<stok>

* 这一步是打开ssh登录权限
```http
http://192.168.31.1/cgi-bin/luci/;stok=<stok>/api/misystem/set_config_iotdev?bssid=Xiaomi&user_id=longdike&ssid=-h%3B%20nvram%20set%20ssh_en%3D1%3B%20nvram%20commit%3B%20sed%20-i%20's%2Fchannel%3D.*%2Fchannel%3D%5C%22debug%5C%22%2Fg'%20%2Fetc%2Finit.d%2Fdropbear%3B%20%2Fetc%2Finit.d%2Fdropbear%20start%3B
```

* 这一步将root密码设为admin
```http
http://192.168.31.1/cgi-bin/luci/;stok=<stok>/api/misystem/set_config_iotdev?bssid=Xiaomi&user_id=longdike&ssid=-h%3B%20echo%20-e%20'admin%5Cnadmin'%20%7C%20passwd%20root%3B
```

3. 刷入breed固件

* 将下载好的breed固件传入路由器

```shell
scp -O ./breed-mt7621-xiaomi-r3g.bin root@192.168.31.1:/tmp/breed-mt7621-xiaomi-r3g.bin
```
> -O的作用是使用费 sftp 的方式传文件，不加可能会遇到 ash: /usr/libexec/sftp-server: not found 错误


* 刷入


breed传到路由器之后，我们在路由器 SSH 会话里面执行一下命令

```shell
mtd -r write /tmp/breed-mt7621-xiaomi-r3g.bin Bootloader
```

* 进入不死后台

拔掉路由器电源，按住reset同时接上电源等双黄灯闪烁后松开, 浏览器输入 192.168.1.1 即可进入breed
> 注意这里一定得插着网线，刚开始路由器不会发布WiFi信号，如果是win的话，也要把网卡中的DHCP打开，不要自己设置IP，否则进不去


进入界面之后我们打开环境变量编辑 ，添加字段 新增字段”xiaomi.r3g.bootfw”,值设置为2 。 

在【固件更新】将kernel & rootfs 选中，刷进去，重启

* 进入openwrt后台

在系统-备份恢复中将 sysupgrade.bin 再刷进去

4. 设置中文

在System-software中，先 update lists，搜索 luci-i18n-base-zh-cn，安装


### 另一种方式

直接登录SSH进行刷机，不需要安装breed，只需三个文件：

openwrt-ramips-mt7621-xiaomi_mi-router-ac2100-squashfs-kernel1.bin

openwrt-ramips-mt7621-xiaomi_mi-router-ac2100-squashfs-rootfs0.bin

openwrt-ramips-mt7621-xiaomi_mi-router-ac2100-squashfs-sysupgrade.bin

先刷入前面两个文件，之后用sysupgrade.bin更新一下即可。

重启后，通过winscp登录192.168.31.1用户为root密码为admin。先把openwrt的两个rom文件（xxx-kernel1.bin和xxx-rootfs0.bin）上传到路由器tmp目录。

再用putty登录192.168.31.1进行刷机操作，输入如下命令进行刷机：

nvram set uart_en=1&&nvram set bootdelay=5&&nvram set flag_try_sys1_failed=1&&nvram commit

mtd write /tmp/xxx-kernel1.bin kernel1

mtd -r write /tmp/xxx-rootfs0.bin rootfs0

注意上面rom文件的文件名，把xxx替换成你自己用的rom文件名。

刷完后将重启，之后便是openwrt路由的设置了，最后用sysupgrade.bin更新一下即可。 