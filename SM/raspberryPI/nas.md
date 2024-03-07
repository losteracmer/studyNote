# NAS


## 挂盘

u盘刚插上的时候在 /dev/sda1 下

```shell
mount -o rw /dev/sda1 /home/~/usbdisk
```

> -o 表示选项， rw是读写，　这种写法是root用户有读写权限
>/dev/sda1 是要mount的设备
>/home/~/usbdisk 是要mount到的目录

给普通用户开读写权限

```shell
mount -o uid=pi,gid=pi /dev/sda1 /home/~/usbdisk
```

取消挂载
```shell
umount /home/~/usbdisk
```
> 取消挂载过程中u盘不能被使用


可以安装usbmount自动挂载
```shell
apt-get install usbmount
```
> 将会自动挂载到/media/usb0下

