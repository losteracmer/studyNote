# ETCD基础命令

## 数据操作CRUD

//todo


## 数据库操作

#### 1. 查看 etcd 节点空间占用

etcdctl --endpoints=127.0.0.1:2379 -w table --user=user:password endpoint status

在输出结果中，DB SIZE 字段显示了 etcd 节点占用的空间大小。

#### 2. etcd 数据压缩与清理

##### 2.1获取当前版本 revision

rev=$(etcdctl --endpoints=127.0.0.1:2379 -w json --user=user:password endpoint status | egrep -o '"revision":[0-9]*' | egrep -o '[0-9].*')

revision 是 etcd 全局修订编号，每次数据修改（put, del）都会导致 revision 加 1。etcd mvcc 机制，导致同一个 key，在多次变更后，会存在多个版本，实际上很多时候，我们只需要最新的那个版本，其他旧版本都是可以清除的，这样能够减少内存和磁盘空间占用。etcd 快照备份也会对应一个 revision 编号，相当于是备份某个特定 revision 编号时的快照。


##### 2.2 压缩所有旧版本

压缩旧版本，并不会立刻释放空间。

etcdctl --endpoints=127.0.0.1:2379 --user=user:password compact $rev

##### 2.3 整理多余的空间，释放空间

etcdctl --endpoints=127.0.0.1:2379 --user=user:password defrag
