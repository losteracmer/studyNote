

# HA installation in raspberry PI

## supervisor




* 替换源

```shell
sudo cp /etc/apt/sources.list /etc/apt/sources.list.bak
sudo cp /etc/apt/sources.list.d/raspi.list /etc/apt/sources.list.d/raspi.list.bak

echo "# 默认注释了源码镜像以提高 apt update 速度，如有需要可自行取消注释
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bullseye main contrib non-free
# deb-src https://mirrors.tuna.tsinghua.edu.cn/debian/ bullseye main contrib non-free

deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bullseye-updates main contrib non-free
# deb-src https://mirrors.tuna.tsinghua.edu.cn/debian/ bullseye-updates main contrib non-free

deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bullseye-backports main contrib non-free
# deb-src https://mirrors.tuna.tsinghua.edu.cn/debian/ bullseye-backports main contrib non-free

# deb https://mirrors.tuna.tsinghua.edu.cn/debian-security bullseye-security main contrib non-free
# # deb-src https://mirrors.tuna.tsinghua.edu.cn/debian-security bullseye-security main contrib non-free

deb https://security.debian.org/debian-security bullseye-security main contrib non-free
# deb-src https://security.debian.org/debian-security bullseye-security main contrib non-free" > /etc/apt/sources.list

echo "deb http://ftp.de.debian.org/debian bullseye-backports main" > /etc/apt/sources.list.d/raspi.list

apt update
apt upgrade -y
```

最新的树莓派Debian版本是`bookworm,`参考 [清华源]([raspberrypi | 镜像站使用帮助 | 清华大学开源软件镜像站 | Tsinghua Open Source Mirror](https://mirrors.tuna.tsinghua.edu.cn/help/raspberrypi/))。

```shell
echo "# 默认注释了源码镜像以提高 apt update 速度，如有需要可自行取消注释
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm main contrib non-free
# deb-src https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm main contrib non-free

deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm-updates main contrib non-free
# deb-src https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm-updates main contrib non-free

deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm-backports main contrib non-free
# deb-src https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm-backports main contrib non-free

# deb https://mirrors.tuna.tsinghua.edu.cn/debian-security bookworm-security main contrib non-free
# # deb-src https://mirrors.tuna.tsinghua.edu.cn/debian-security bookworm-security main contrib non-free

deb https://security.debian.org/debian-security bookworm-security main contrib non-free
# deb-src https://security.debian.org/debian-security bookworm-security main contrib non-free" > /etc/apt/sources.list

echo "deb https://mirrors.tuna.tsinghua.edu.cn/raspberrypi/ bookworm main" > /etc/apt/sources.list.d/raspi.list

apt update
apt upgrade -y
```







* 换pip源

临时使用： 
可以在使用pip的时候在后面加上-i参数，指定pip源 
eg: pip install scrapy -i https://pypi.tuna.tsinghua.edu.cn/simple

永久修改： 
修改 ~/.pip/pip.conf (没有就创建一个)， 内容如下：

```[global]
mkdir ~/.pip
echo "index-url = https://pypi.tuna.tsinghua.edu.cn/simple" > pip.conf
```




* 添加NetworkMananger配置

```shell
echo "[connection]
wifi.mac-address-randomization=1

[device]
wifi.scan-rand-mac-address=no
" >> /etc/NetworkManager/conf.d/100-disable-wifi-mac-randomization.conf
```


* 禁用ModemManager

```shell
# 停止ModemManager
sudo systemctl stop ModemManager
# 禁止ModemManager开机自启
sudo systemctl disable ModemManager

```


* 启用NetworkManager


特殊情况下通过添加配置的方式让Network manager连接网络
在/etc/NetworkManager/system-connections/路径下添加一个xxx.nmconnection(名字无所谓) 


```conf
[connection]
id=Avengers_5G
uuid=281ba4b3-0e73-47cd-bc7a-9f95cb32bc16
type=wifi
interface-name=wlan0
permissions=

[wifi]
mac-address-blacklist=
mode=infrastructure
ssid=Avengers_5G

[wifi-security]
auth-alg=open
key-mgmt=wpa-psk
psk=qwertYUIOP

[ipv4]
dns-search=
method=auto

[ipv6]
addr-gen-mode=stable-privacy
dns-search=
method=auto

[proxy]
```

> 实测，并不行，还是得通过写一个脚本，sleep一段时间后执行 nmcli命令来保证 启动networkManager 后自动连接WiFi，例如：
>
> (树莓派 bookworm 已经不存在断WiFi问题了)
>
> ```
> sleep 30;
> echo `date`
> nmcli device wifi connect Avengers_5G password qwertYUIOP
> ```

```shell
systemctl enable NetworkManager
systemctl start NetworkManager
```


* 安装依赖

```
apt install vim apparmor jq wget curl udisks2 libglib2.0-bin network-manager dbus lsb-release systemd-journal-remote -y
```

* 安装systemd-resolved
> systemd-resolved是一个bullseye-backports下的最新包，依赖的包都有oldstable版本，apt默认不会命中依赖，需要特殊指定。
> 由于systemd-resolved 是一个非默认的 target_release， 但是可以通过 -t 制定发行版

```shell
apt -t bullseye-backports install systemd-resolved
```

```
apt -t bookworm-backports install systemd-resolved
```



* 添加boot配置

```
echo " apparmor=1 security=apparmor" >> /boot/cmdline.txt
```

* 安装OS-Agent

```
wget https://github.com/home-assistant/os-agent/releases/download/1.5.1/os-agent_1.5.1_linux_aarch64.deb
dpkg -i os-agent_1.5.1_linux_aarch64.deb
```



* 安装docker

```
curl -fsSL get.docker.com | sh
```

* docker换源

```shell
echo "
{
  \"registry-mirrors\": [\"https://md4nbj2f.mirror.aliyuncs.com\"]
}
" > /etc/docker/daemon.json 

#重载配置文件
sudo systemctl daemon-reload   

# 重启docker  
sudo systemctl restart docker  
```



* 解决Cgroup v1 问题

```
echo " systemd.unified_cgroup_hierarchy=false" >> /etc/default/grub
echo " systemd.unified_cgroup_hierarchy=false" >> /boot/cmdline.txt
apt install grub2-common -y
mkdir /boot/grub
```

* 连接一次wifi (可选)

```shell
nmcli device wifi connect Avengers_5G password qwertYUIOP
ifconfig
```



* 重启一下

```shell
reboot
```


* 安装supervisored

```
wget https://github.com/home-assistant/supervised-installer/releases/latest/download/homeassistant-supervised.deb
dpkg -i homeassistant-supervised.deb
```

> 安装过程可能出现如下网络问题：
> ```
> [info] Waiting for checkonline.home-assistant.io - network interface might be down...
> PING checkonline.home-assistant.io (104.26.4.238) 56(84) bytes of data.
> ```
> 不知道为什么这个地址国内无法访问，不过还好只是一个ping检查，在本地hosts中添加如下会避开这个检查
> ```shell
> echo "127.0.0.1 checkonline.home-assistant.io" >> /etc/hosts
> ```



## core

* 安装Python编译依赖

```shell
sudo apt-get install -y python3 python3-dev python3-venv python3-pip bluez libffi-dev libssl-dev libjpeg-dev zlib1g-dev autoconf build-essential libopenjp2-7 libtiff5 libturbojpeg0-dev tzdata ffmpeg liblapack3 liblapack-dev libatlas-base-dev
```



* 安装Python 3.11

```shell
wget https://www.python.org/ftp/python/3.11.0/Python-3.11.0.tgz
tar -xf Python-3.11.0.tgz
cd Python-3.11.0
```



* 安装botocore(解决和urllib冲突的问题)

```
pip3.11 install git+https://github.com/boto/botocore
```



* 编译Python3.11

```
./configure --enable-shared --prefix=/usr/local LDFLAGS="-Wl,-rpath /usr/local/lib"
make -j4
sudo make altinstall
```



* [安装ha core]([Raspberry Pi - Home Assistant (home-assistant.io)](https://www.home-assistant.io/installation/raspberrypi#install-home-assistant-core))

```
sudo apt-get install -y python3 python3-dev python3-venv python3-pip bluez libffi-dev libssl-dev libjpeg-dev zlib1g-dev autoconf build-essential libopenjp2-7 libtiff5 libturbojpeg0-dev tzdata ffmpeg liblapack3 liblapack-dev libatlas-base-dev

sudo useradd -rm homeassistant -G dialout,gpio,i2c

sudo mkdir /srv/homeassistant
sudo chown homeassistant:homeassistant /srv/homeassistant

sudo -u homeassistant -H -s
cd /srv/homeassistant
python3.11 -m venv .
source bin/activate

python3.11 -m pip install wheel

pip3.11 install homeassistant==2023.9.2
```



* 启动hass

```
sudo -u homeassistant -H -s
cd /srv/homeassistant
source bin/activate
hass
```





## Android平台

### aidlux(android)

[在AidLux平台安装HomeAssistant并集成HACS- AidLux开发者社区](https://community.aidlux.com/postDetail/854)

不成功，遇到了解决不了的问题，在评论区。


### Alpine Term(android)

一个自带docker的安卓虚拟linux系统，基于qemu。在这上边使用docker安装可以跑。但是性能很差。

```shell
docker run -d \
  --name homeassistant \
  --privileged \
  --restart=unless-stopped \
  -e TZ=Asia/Shanghai \
  -v ~/.homeassistant:/config \
  --network=host \
  ghcr.io/home-assistant/home-assistant:stable
``$$`

```

