# spring cloud

## 微服务拆分方法论

* X轴 水平复制

* Z轴 数据分区

  每个模块负责一块独立的数据区域

  * 先考虑业务功能，在考虑数据
  * 无状态服务

  如何裁缝数据

  * 每个微服务都有单独的数据存储
  * 依据服务的特点选择不同的结构的数据库类型
  * 难点在确定边界

* Y轴 功能解耦

  * 单一职责，松耦合、高内聚
  * 关注点分离 DDD领域驱动设计
    * 按职责
    * 按通用性
    * 按粒度级别

【4-3】 服务拆分分析



## 应用间通信

* RestTemplate

  ```
  new RestTemplate();
  restTemplate.getForObject("url",OBJECT.class)
  ```

  ```
  var serviceInstance loadBalanceClient.choose("serviId")
  serviceInstance.getHost()||.getPort()
  //然后通过 restTemplate 调用 
  ```

  ```
  //通过 @LoadBalanced  放到 RestTemplate 这个Bean 上
  //就可以通过  restTemplate.getForObject("http://${MODEL_NAME}/uri"，OBJCET.class)
  //来调用服务
  ```

  

* Feign

  在客户端 增加依赖  spring-cloud-starter-feign

  启动主类加注解 @ EnableFeignClients

  声明调用接口

  ```java
  @FeignClient
  public interface PRoducetClient{
  	@GetMapping("/msg")
  	String productMsg();
  }
  ```

  调用：

  ```
  @Autowired
  private ProductClient s;
  
  //调用
  s.productMsg();  //获取信息
  ```

  

[Ribbon](.....Eureka 就是整合了Ribon)

**spring cloud 升级之后，feign 这个组件的mvn名字更名为 openfeign**





## RabbitMQ & Docker

在docker  安装  RabbitMQ

```sh
docker pull rabbitmq:3.8.0-beta.5-management
```

运行 RabbitMQ

```sh
docker run -d --name rabbitmq3.7.7 -p 5672:5672 -p 15672:15672 -v `pwd`/data:/var/lib/rabbitmq --hostname myRabbit -e RABBITMQ_DEFAULT_VHOST=my_vhost  -e RABBITMQ_DEFAULT_USER=admin -e RABBITMQ_DEFAULT_PASS=admin df80af9ca0c9
```

> -d 后台运行容器；
>
> --name 指定容器名；
>
> -p 指定服务运行的端口（5672：应用访问端口；15672：控制台Web端口号）；
>
> -v 映射目录或文件；
>
> --hostname  主机名（RabbitMQ的一个重要注意事项是它根据所谓的 “节点名称” 存储数据，默认为主机名）；
>
> -e 指定环境变量；（RABBITMQ_DEFAULT_VHOST：默认虚拟机名；RABBITMQ_DEFAULT_USER：默认的用户名；RABBITMQ_DEFAULT_PASS：默认用户名的密码）

**如果不配置账户密码  则默认都是 guest**



#### MQ应用场景

* 异步处理
* 流量削峰
* 日志处理
* 应用解耦

#### 应用

依赖

spring-boot-starter-amqp

配置

````yml
spring: 
	rabbitmq:
		host:
		prot:5672
		password:
		username:
````

监听

```java
@Component
public class MqReceiver{
	
	//@RabbitListener(queues = "myQueue")
    @RabbitListener(queuesToDeclare = @Queue("myQueue"))
    //第二种方法自动创建队列
	public void process(String msessage){
		log.info("收到消息" + message)
	}
}
```
发送

```java
@Autowired
pirvate AmqpTemplate at;

public void send(){
    at.convertAndSend("队列名","消息");
}
```

消息分组

```java
@Component
public class MqReceiver{
	
	@RabbitListener(bindings = @QueueBingding(
    	exchange = @Exchange("myOrder")
        key = "fruit",
        value = @Queue("furitOrder")
    ))
	public void fruitProcess(String msessage){
		log.info("furit 收到消息" + message)
	}
    
    @RabbitListener(bindings = @QueueBingding(
        exchange = @Exchange("myOrder")
        key = "computer",
        value = @Queue("computerOrder")
    ))
	public void computerProcess(String msessage){
		log.info("收到消息" + message)
	}
}
//发送方法
at.convertAndSend("key","queue","msg")
//指定 发送的key  和 队列名称  服务队列会自动转发到key对应的 子队列 中
```



#### spring cloud stream

> 对消息队列进行进一步封装

引入

spirng-cloud-starter-stream-rabbit

定义 消息 接口

```java
public interface Streamclient{
    String INPUT = "INPUT";
    
    @INPUT(StreamClient.INPUT)
    SubscribableChannel input();
    
    @Output(SteamClient.INPUT)
    MessageChannel output();
}
    
```

监听方

```java
@Component
@EnableBinding(StreamClient.class)
public class StreamReveiver{
	
	@StreamListrener(StreamClient.INPUT)
	public void process(Object msg){
		log.info(msg);
	}
}
```

发送方

```java
//自动注入
@Autowired
private StreamClient sc;

//使用
sc.output().send(MessageBuilder.withPayload("msg").build());
```

防止多个项目实例产生 多个队列同时 发送消息的情况

加配置 ： spring.cloud.stream.bindings.myMessage.group: queueName

rabbitMQ 管理界面 数据显示格式默认是 Base64编码，将其更改为Json格式

加配置：spring.cloud.stream.bindings.myMessage.content-type: application/json

收到消息后，再执行返回 指定的队列消息

1. 同样的方式 定义 接受放的 input output 和指定的queue

2. 在接受方   方法上加注解

   ```
   @SendTo(StreamClient.INPUT222)
   //返回 值  作为消息 发送出去
   return "return msg";
   ```













## spring cloud 配置中心

引入依赖

spring-cloud-config-server

启动类上加注解

@EnableConfigServer

配置yml文件

```yml
spring: 
  cloud: 
  	config: 
      server:
        git: 
          url: ....
          username: ...
          password: ...
          basedir: 本地git配置存放目录
```

配置文件格式

/{name}-{profiles}.yml

/{lable}/{name}-{profiles}.yml

name 服务名

profiles 环境

lable 分支

。。。。。。。



#### spring cloud bus

> 自动更新配置

需要在Git仓库进行配置 自动发送接口 到服务器



改名application.yml  为 bootstrap.yml  会在 项目启动前就读取这个配置

所以一般 配置中心的配置 放入此文件中 ，从配置中心拉取的配置做为项目配置

## 服务网关

### 网关

* Nginx + Nua
* Kong
* Tyk
* Spring Cloud Zuul

### Zuul

过滤器类型

Pre  Post  Route  Error



#### 创建项目

添加主类注解 @EnableZuulProxy

默认访问路径  项目地址/服务地址/服务路径

#### 更改路由配置

```yml
zuul: 
	routes: 
	# 这个名字可以自定义
		losteracmerName: 
			path: /myProduct/**
			seviceId: product
	# 简洁写法
	product: /myProduct/** 
```

#### 看到所有路由

加配置

```yml
management: 
	security: 
		enabled: false
```

访问  /application/routes 就可以看到所有路由情况

#### 排除某个路由

```yml
zuul: 
	ingored-patterns: # 这里是一个set<string> 参数 可以用正则表达式
	  - /produt/...
	  - /order/...
```

> 如果使用了路由 cookies 不会被传递
>
> 加 sensitiveHeaders ： # 敏感头 过滤 默认过滤 cookies set-cookies Authority

#### 动态注入Zuul 配置注解

加入组件 @Component 或者直接在 启动类中加上

```java
@ConfigurationProperites("zuul")
@RefreshScope
public ZuulProperties zuulProperties(){
return new ZuulProperties();
}
//其实这个类在zuul中已经存在，这里只不过是把它暴露出去并且加上Scope刷新
```

#### 鉴权

新建网关服务

建立Filter

```java
@Component
//继承 ZuulFilter
public class TokenFilter extends ZuulFilter {
   @Override
   public String filterType() {
       return PRE_TYPE;
   }

   @Override
   public int filterOrder() {
       return PRE_DECORATION_FILTER_ORDER - 1; //为在默认返回值之前 进行过滤 ，需要 减一
   }

   @Override
   public boolean shouldFilter() {
       return true;
   }

   @Override
   public Object run() {
       //用 Zuul 提供的 import com.netflix.zuul.context.RequestContext; 获取Request
       RequestContext requestContext = RequestContext.getCurrentContext();
       HttpServletRequest request = requestContext.getRequest();

       //这里从url参数里获取, 也可以从cookie, header里获取
       String token = request.getParameter("token");
       if (StringUtils.isEmpty(token)) {
           requestContext.setSendZuulResponse(false);
           requestContext.setResponseStatusCode(HttpStatus.UNAUTHORIZED.value());
       }
       return null;
   }
}
```

服务器 返回 增加 token 头

```java
@Component
public class addResponseHeaderFilter extends ZuulFilter{
    @Override
    public String filterType() {
        return POST_TYPE;
    }

    @Override
    public int filterOrder() {
        return SEND_RESPONSE_FILTER_ORDER - 1;
    }

    @Override
    public boolean shouldFilter() {
        return true;
    }

    @Override
    public Object run() {
        RequestContext requestContext = RequestContext.getCurrentContext();
        HttpServletResponse response = requestContext.getResponse();
        response.setHeader("X-Foo", UUID.randomUUID().toString());
        return null;
    }
}
```

#### 限流

> **令牌桶 算法 ：**
>
> 服务器以一定的速率 往令牌桶中 放 令牌，如果桶存满了就丢弃 ，每个请求 都会从令牌桶中拿到一个令牌，如果没有拿到令牌 ，则拒绝访问

> **漏斗算法：**
>
> 请求都进入漏斗中，漏斗以恒定的速率往外出水，代表处理这些请求，当漏斗满的时候，对超出的请求进行丢弃或者加入队列处理

区别：漏斗算法能保证以恒定的速率处理请求，（CPU保持一种稳定的状态），而令牌桶算法则没有这样的保证，可能会出现请求突发的情况，只要令牌桶中有令牌，就能让一时间所有的请求都得到处理。比如秒杀的时候，就应该用令牌桶算法，保证尽可能多的请求被处理，而不让过分多的请求阻塞

谷歌 的 guawa.jar  开源了 令牌桶算法的实现

```java
public class RateLimitFilter extends ZuulFilter{

	private static final RateLimiter RATE_LIMITER = RateLimiter.create(100);

	/**
	 * 指定 过滤器类型
	 * We also support a "static" type for static responses see  StaticResponseFilter.
	 */
	@Override
	public String filterType() {
		return PRE_TYPE;
	}

	/**
	 * filterOrder() must also be defined for a filter. Filters may have the same  filterOrder if precedence is not
	 * important for a filter. filterOrders do not need to be sequential.
	 *
	 * @return the int order of a filter
	 */
	@Override
	public int filterOrder() {
		return SERVLET_DETECTION_FILTER_ORDER - 1;
	}

	/**
	 * 是否启用 run() 方法
	 */
	@Override
	public boolean shouldFilter() {
		return true;
	}

	/**
	 * 核心 过滤配置 
	 */
	@Override
	public Object run() {
		if (!RATE_LIMITER.tryAcquire()) {
            //如果没有拿到令牌 ，就抛出错误  自定义错误
			throw new RateLimitException();
		}

		return null;
	}
}

```

#### zuul 鉴权服务

网关中 对 访问的路径进行判断，不同的路径 对应 不同的鉴权 方案



#### 跨域访问

在网关 添加 配置类

```java
@Configuration
public class CorsConfig {

	@Bean
	public CorsFilter corsFilter() {
		final UrlBasedCorsConfigurationSource source = new UrlBasedCorsConfigurationSource();
		final CorsConfiguration config = new CorsConfiguration();

		config.setAllowCredentials(true);
		config.setAllowedOrigins(Arrays.asList("*")); //http:www.a.com
		config.setAllowedHeaders(Arrays.asList("*"));
		config.setAllowedMethods(Arrays.asList("*"));
		config.setMaxAge(300l);

		source.registerCorsConfiguration("/**", config);
		return new CorsFilter(source);
	}
}

```



## 服务容错和Hystrix

引入依赖

spring-cloud-starter-hystrix

@EanalbieCloudApplication 注解 包含了  SpringBootApplication，EnableCircuitBreaker

EnableDiscoveryClient

所以只要将注解@EanalbieCloudApplication 加到主类就可以了

* 服务降级

  * 优先核心服务，非核心服务不可用或者弱可用

  >  如果服务A调用服务B  ，B此时已经崩了，客户端就会看到500，此时应该给客户端一个友好的提示

  在controller方法上加注解  @HystrixCOmmand(fallbackMethod = "回调方法")

  然后写一个回调方法，会在服务不可用的时候（报错）调用这个方法。

  > 当然也可以在 controller类上加注解 DefaultProperties(defaultFallback = "methodName")

   超时时间 

  @HystrixCOmmand(@HystrixProperties(name = "execution.isolation.thread.timeoutInMIllisendconds" ,value="3000"))

* 服务熔断

  > 熔断开关状态： 打开，半开，关闭
  >
  > 如果一段时间请求中 访问失败超过一定次数 、比例，则熔断 打开 （过一定时间后恢复半开状态）
  >
  > 如果半开状态访问成功，则恢复熔断关闭状态
  >
  > 经过一段时间后10000 ，熔断器从打开进入半开状态，如果访问成功，则进入关闭

  配置 方法注解

  @HystrixCOmmand(@HystrixProperties(name = "circuitBreaker.enabled" ,value="true"))

  @HystrixCOmmand(@HystrixProperties(name = "circuitBreaker.requestvolumeThreshold" ,value="10"))

  @HystrixCOmmand(@HystrixProperties(name = "circuitBreaker.sleepWindowsInMilliseconds" ,value="10000"))

  @HystrixCOmmand(@HystrixProperties(name = "circuitBreaker.errorThresholdPercentage" ,value="60"))

* 依赖隔离
  
  * 线程池隔离
* 监控

yml配置

```yml
hystrix:
	command:
		default:
			execution:
				isolation:
					thread: 
						timeoutInMilliseconds:2000
		#自定义方法名
		selfDefine:
			execution:
				isolation:
					thread:
						timeoutInMilliseconds:3000
```



!需要在方法中加@HystrixCommand

可视化组件 

profix --- dashboard

主类加注解

@EnableHystrixDashboard

访问/hystrix   

！ 需要更改content-path:/



## 链路监控

导包

spring-cloud-starter-sleuth

利用zipkin 进行图形化展示每个服务到底用了多长时间

spring-cloud-sleuth-zipkin

> spring-cloud-starter-zipkin 包含了上述两个包

为了能利用zipkin观察调用情况

需要利用zipkin 图形化 zipkin server

官网 ： 利用docker

安装docker 启动后还需要配置

```yml
	zipkin:
		base-url: http://localhost:9411
	sleuth:
		sampler: 
			percentage: 1 # 请求抽样百分比
		
```

概念：[11-2 服务追踪]()



## 部署

 rancher 配置 

。。。。





## 技巧

### 快捷键

alt ctrl d  直接调到方法的实现 上

### JWT 鉴权

[jwt](https://www.cnblogs.com/haoliyou/p/9606082.html)

JsonWebT  

就是在请求中都加入一个token关键字，后台根据token来确定用户身份，token关键字的生成可以用UUID，并把token键值对保存到redis中，这样就可以实现分布式鉴权



将 某一包下的日志级别单独设置

```yml
logging: 
	level: 
		org......: debug
```




## 坑

idea 配置项目的时候没有 添加 spring-boot-start-web 的依赖，导致 eureka client 无法启动



两个Eureka 相互注册  一个client 注册 到 第二个启动的server上时，才会相互注册，,,,,并不是

本地测试 ：**不能用 localhost配端口，应该去改配置hosts文件**

在controller中 ，如果方法中用了@RequestBody  那么 在方法上的注解只能用@PostMapping而不能用@GetMapping ，get注解只能在  @RequestParam

spring MVC 在序列化/反序列化  的时候，需要有 无参构造参数和 get set 方法



## 疑问

### optional

这个有空复习一下....

### 多模块系统

pom格式需要注意的地方