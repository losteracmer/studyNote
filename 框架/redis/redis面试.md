## Redis

### 线程模型

NIO 单线程

1> 文件事件处理器

IO多路复用

### Redis 于 memcached 的区别

数据结构 Redis 比较多

内存使用效率memcached更高

性能Redis只使用单核，而memcached可以使用多核，性能更高

memcached没有原生集群模式（能通过第三方插件实现），Redis支持cluster模式

