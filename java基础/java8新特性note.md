# java 8 新特性笔记







## 命令tips

```java
jps -l  //产看java进程号

jstate -gcutil 【PID】 【刷新时间】 【次数】  //? 

jconsole 打开java进程控制台
```



## 散

### 注解

* @functioninterface 注解  如果不是函数式接口就会报错

### 守护线程

​	 当主线程结束的时候，不管守护线程是否执行完成，整个进程都会停止

```java
ExecutorService pool = Executors.newFixedThreadPool(2, r -> {
    //工厂方法，将runable手动组合成Thread
    Thread t = new Thread(r);
    //将线程设置为守护线程
    t.setDaemon(true);
    return t;
});
```

### Join()

```java
goal.join()
主动放弃cup的执行权
将目标线程放入自己的线程中执行，等待目标线程执行完成后自己再次执行
如果执行 Thread.currentThread().join()
则线程就会进入无限执行，永远不会停
```



--------------------------------

### 采坑

* 如果定义两个相同的lambda(签名相同)，在调用的时候，编译器如果分不出是哪个，就会报错 ambiguous



## stream

* Stream.parallel() 并行执行流，得到的顺序可能会不同

* IntStream DoubleStream 

  ```java
  IntStream intStream = limit.mapToInt(Integer::intValue);
  Stream<Integer> boxed = intStream.boxed(); //将instream装箱成IntegerStream
  ```

* Stream.flatmap

  ```java
  Stream<String> stream = Stream.of("a a a", "b b b", "cc c", "ddd");
  // 扁平化  将flatmap产生的流，连接到一起形成新的流
  Stream<String> flatStream = stream.parallel().flatMap(str -> {
      return Stream.of(str.split(" "));
  });
  ```

* optional.flatMap

  ```java
          Optional<String> optional = Optional.ofNullable("abcd");
  
          Optional<String> opt2 = optional.map(d -> "1" + d).map(d -> "2" + d);
          opt2.ifPresent(System.out::println);//21abcd
  
          Optional<String> s = optional.flatMap(d -> Optional.of("1" + d)).flatMap(d -> Optional.of("2" + d));
          s.ifPresent(System.out::println); //21abcd
          //map 会主动将映射结果封装成一个新的optional，flatmap则是让调用者自己封装结果
  ```

### 收集结果

Stream.collect()



### 线程

* compelableFuture

   ```java
  CompletableFuture<String> future = new CompletableFuture<>();
          future.whenComplete((u,t)->{
              if (u != null) {
                  System.out.println("u = " + u);
                  System.out.println(u.getClass().getName());
              }
              if (t != null) {
                  System.out.println("t = " + t);
                  System.out.println(t.getClass().getName());
                  Optional.of(t).ifPresent(x -> x.printStackTrace());
              }
          });
          new Thread(()->{
              try {
                  Thread.sleep(1000);
                  future.complete("has complete");
              } catch (InterruptedException e) {
                  e.printStackTrace();
  
              }
          }).start();
  ```

  ```java
        AtomicBoolean finished = new AtomicBoolean(false);
          ExecutorService executor = Executors.newFixedThreadPool(2, r -> {
              Thread t = new Thread(r);
              t.setDaemon(false);
              return t;
          });
  
          //默认是守护线程
          CompletableFuture.supplyAsync(CompletableFutureInAction1::get, executor)
                  .whenComplete((v, t) -> {
                      Optional.of(v).ifPresent(System.out::println);
                      finished.set(true);
                  });
  ```
  
  ```java
  //对一些任务用流的方式处理成并行多线程，并且在所有任务完成后得到及时的结果
  List<Integer> productionIDs = Arrays.asList(1, 2, 3, 4, 5);
  List<Double> result = productionIDs
      .stream()
      .parallel()//实现并行处理，如果不加，测试显示为  串行处理
      .map(i -> CompletableFuture.supplyAsync(() -> queryProduction(i), executor)) //自定义线程池 queryProduction是一个等待任务
      .map(future -> future.thenApply(CompletableFutureInAction3::multiply))
      .map(CompletableFuture::join).collect(toList()); //join 不知道什么作用
  
  System.out.println(result);
  ```
  
  