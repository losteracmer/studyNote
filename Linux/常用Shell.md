# 常用shell

### 将错误输出重定向到null

```shell
command > /dev/null 2>&1
```



### 一条命令停止进程

```shell
ps -ef | grep clb_detecter | awk '{print $2}' | xargs kill -9
```

