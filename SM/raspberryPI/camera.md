# camera

[树莓派 Raspberry Pi Bullseye Camera V2 相机 libcamera 用法，拍照，直播视频_学习溢出的博客-CSDN博客](https://blog.csdn.net/qq_41608408/article/details/126535572)

Raspberry Pi Camera in Bullseye
树莓派新系统 Debian Bullseye 将不再支持相机的库 picamera 和 raspicam。取而代之的是 Linux 框架 V4L2 和 libcamera。

libcamera
官方说之所以更新是因为libcamera可以提升画质，更好的适配摄像头，提供了动作检测、面部识别、物体识别、HDR等框架，最重要的是可以使用 opencv 和 tensorflow。

新功能有：

* libcamera-hello – 一个简单的“hello world”应用程序，它启动相机预览流并将其显示在屏幕上。

* libcamera-jpeg – 一个运行预览窗口然后捕获高分辨率静止图像的简单应用程序。
  ```###保存一张照片###
  libcamera-jpeg -o test.jpg
  ###保存一张照片并设置宽和高，延迟时间-t为3秒 3000毫秒###
  libcamera-jpeg -o test.jpg -t 3000 --width 1920 --height 1080
  
  libcamera-still – 一个更复杂的静态图像捕获应用程序，它模拟了raspistill的更多功能。
  ###保存一张静态图像###
  libcamera-still -o still.jpg
  ###保存为png格式 还可以是 bmp、rgb、yuv420格式###
  libcamera-still -e png -o still.png
  ###以MMDDhhmmss的日期格式为文件名保存一张jpg照片###
  libcamera-still --datetime
  
  libcamera-vid – 一段视频捕捉应用程序。
  ###保存一段视频 时间为10秒###
  libcamera-vid -t 10000 -o test.h264
  1
  2
  libcamera-raw – 用于直接从传感器捕获原始帧的基本应用程序
  ```

libcamera-detect –默认情况下不构建此应用程序，但如果用户在其 Raspberry Pi 上安装了 TensorFlow Lite，则可以构建它。当检测到某些对象时，它会捕获 JPEG 图像。

Streaming Video 直播视频
在树莓派上输入命令：
libcamera-vid -t 0 --inline --listen -o tcp://0.0.0.0:8888
1
在另一台电脑上打开 VLC 视频播放器 Media >> Open Network Stream.

输入视频流地址

tcp/h264://raspberrypi.local:8888
1
Reference
[1] https://www.raspberrypi.com/news/bullseye-camera-system/
[2] https://www.tomshardware.com/how-to/use-raspberry-pi-camera-with-bullseye



```
ffmpeg -f v4l2 -i /dev/video0 -pix_fmt yuv420p -c:v libx264 -preset ultrafast -tune zerolatency -f rtsp rtsp://sst:sst@0.0.0.0:8765/live
```

