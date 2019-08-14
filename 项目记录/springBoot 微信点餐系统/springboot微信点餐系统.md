# springBoot微信点餐项目笔记

## 坑点

### 构建项目

```
关于错误： Caused by: org.hibernate.AnnotationException: No identifier specified for entity
因为根据hibernate规范 需要在实体类上加@Id，但是这个@Id注解有两个实现，注意看是不是javax.persistence.Id;
```

## 技巧

### api

```
BeanUtils.copyPoperties(obj1,ojb2)  //将第一个对象属性copy到第二个上	
如果obj1的属性是null也会被copy进obj2  这一点注意
```

```
@DynamicUpdate 在entity类上加，可以同步时间date的更新
```

```
@Transient 注解 标注 非数据库字段的 feild
```

```
/** 创建时间. */
@JsonSerialize(using = Date2LongSerializer.class)
private Date createTime;
对时间date参数进行json转换时的技巧，这样做转换的格式不会含有后面三个0
```

```
@JsonInclude(JsonInclude.Include.NON_NULL) 将此注解加到 json类上，如果是null的字段将不会解析到json中
全局配置
spring.jackson.default-property-includsion: non_null
! 如果一个字段 ，如果是必须值，可以设置初始值[] ,""
```

```
@Valid 注解 ：用于验证注解是否符合要求，直接加在变量user之前，在变量中添加验证信息的要求，当不符合要求时就会在方法中返回message 的错误提示信息。
```

参考:[博客](https://blog.csdn.net/weixin_38118016/article/details/80977207)

```
String.format(String format,Object ...objs)  格式化字符串，类似于 printf
```



#### redis

```java
redisTemplate.opsForValue().set(String.format(RedisConstant.TOKEN_PREFIX, token), openid, expire, TimeUnit.SECONDS);
```



#### 项目配置

在application.yml 中 添加配置

```yml
projectUrl:
  wechatMpAuthorize: http://sell.natapp4.cc
  wechatOpenAuthorize: http://sell.natapp4.cc
  sell: http://sell.natapp4.cc
```

编写配置类

```java
@Data
@ConfigurationProperties(prefix = "project-url")
@Component
public class ProjectUrlConfig {

    public String wechatMpAuthorize;

    public String wechatOpenAuthorize;

    public String sell;
}
//让 spring boot  自动注入 配置信息
```

#### 习惯

> 对于一些 用了不止一次的信息  如：状态信息  ，要写成  Enum  枚举类，枚举类中放入 代号和信息字段，方便日后对信息进行修改



#### 缓存

> * 直接在application启动类上加入
>
> ```java
> @EnableCaching
> ```
>
> * 在需要缓存的方法上加
>
> ```java
> @Cacheable(cacheNames="缓存名",key="???")
> //加上后，该方法的返回值将会被缓存，下次就不会访问此方法体
> ```
>
> * 在更新后，需要在更新后的方法上加入
>
> ```java
> @CachePut(CachName = "缓存名",key="???")
> //这是将“缓存名” 重新put
> ```
>
> * 清除缓存
>
> ```java
> @CacheEvict(cacheNames="缓存名",key"+"???")
> ```
>
> * 也可以在类上加注解
>
> ```
> @CacheConfig(cacheNames="缓存名")
> //这样可以省去方法中的cacheNames注解
> ```
>
> 

* 对象需要可以序列化 
* key 如果不填，默认就是方法的传入内容
  * key也可以动态改变  如： #sellerID(方法中的参数名)   -----skel表达式
  * condition  判断添加，如果为真则缓存，否则不缓存
  * unless 如果不 ；如果条件不成立，才缓存

```java

@Getter
public enum ResultEnum {

    SUCCESS(0, "成功"),
    PARAM_ERROR(1, "参数不正确"),
    PRODUCT_NOT_EXIST(10, "商品不存在"),
    PRODUCT_STOCK_ERROR(11, "商品库存不正确"),
    ORDER_NOT_EXIST(12, "订单不存在"),
    ORDERDETAIL_NOT_EXIST(13, "订单详情不存在"),
    ORDER_STATUS_ERROR(14, "订单状态不正确"),
    ORDER_UPDATE_FAIL(15, "订单更新失败"),
    ORDER_DETAIL_EMPTY(16, "订单详情为空"),
    ORDER_PAY_STATUS_ERROR(17, "订单支付状态不正确"),
    CART_EMPTY(18, "购物车为空"),
    ORDER_OWNER_ERROR(19, "该订单不属于当前用户"),
    WECHAT_MP_ERROR(20, "微信公众账号方面错误"),
    WXPAY_NOTIFY_MONEY_VERIFY_ERROR(21, "微信支付异步通知金额校验不通过"),
    ORDER_CANCEL_SUCCESS(22, "订单取消成功"),
    ORDER_FINISH_SUCCESS(23, "订单完结成功"),
    PRODUCT_STATUS_ERROR(24, "商品状态不正确"),
    LOGIN_FAIL(25, "登录失败, 登录信息不正确"),
    LOGOUT_SUCCESS(26, "登出成功"),
    ;

    private Integer code;

    private String message;

    ResultEnum(Integer code, String message) {
        this.code = code;
        this.message = message;
    }
}
```



#### 登录认证

##### 声明切面类

```java
@Aspect
@Component
@Slf4j
public class SellerAuthorizeAspect {
    @Autowired
    private StringRedisTemplate redisTemplate;
//!! 在这里做 对于  登录 登出 url的排除操作  
    @Pointcut("execution(public * com.supersst.controller.Seller*.*(..))" +
    "&& !execution(public * com.supersst.controller.SellerUserController.*(..))")
    public void verify() {}

    @Before("verify()")
    public void doVerify() {
        System.out.println("==============进入切入点");
        ServletRequestAttributes attributes = (ServletRequestAttributes) RequestContextHolder.getRequestAttributes();
        HttpServletRequest request = attributes.getRequest();

        //查询cookie
        Cookie cookie = CookieUtil.get(request, CookieConstant.TOKEN);
        if (cookie == null) {
            log.warn("【登录校验】Cookie中查不到token");
            throw new SellerAuthorizeException();
            
        }

        //去redis里查询
        String tokenValue = redisTemplate.opsForValue().get(String.format(RedisConstant.TOKEN_PREFIX, cookie.getValue()));
        if (StringUtils.isEmpty(tokenValue)) {
            log.warn("【登录校验】Redis中查不到token");
            throw new SellerAuthorizeException();
        }
    }
}
```

* 在切面类中获取request对象的两种方

  * ```
    ServletRequestAttributes attributes = (ServletRequestAttributes)
    RequestContextHolder.getRequestAttributes();
    ```
    
  * ```
    @Autowired  
    HttpServletRequest request; //自动注入当前request
    ```

##### 抛出异常后对异常进行捕捉

```java
@ControllerAdvice
public class SellExceptionHandler {

    @Autowired
    private ProjectUrlConfig projectUrlConfig;

    //拦截登录异常
    @ExceptionHandler(value = SellerAuthorizeException.class)
    //@ResponseStatus(HttpStatus.FORBIDDEN)
    public ModelAndView handlerAuthorizeException() {
        return new ModelAndView("redirect:/seller/login?openid=1234");
    }

    @ExceptionHandler(value = SellException.class)
    @ResponseBody
    public ResultVO handlerSellerException(SellException e) {
        return ResultVOUtil.error(e.getCode(), e.getMessage());
    }

    @ExceptionHandler(value = ResponseBankException.class)
    @ResponseStatus(HttpStatus.FORBIDDEN)
    public void handleResponseBankException() {

    }
}
```

* 关于ControllerAdvise： 。。。。。

* @ResponseStatus

  > 注解的作用是  返回的 Response body 状态码

#### webSocket消息推送

pom引入

```xml
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-websocket</artifactId>
        </dependency>
```

编写WebSocket类

```java
@Component
@ServerEndpoint("/webSocket")
@Slf4j
public class WebSocket {

    private Session session;

    private static CopyOnWriteArraySet<WebSocket> webSocketSet = new CopyOnWriteArraySet<>();

    @OnOpen
    public void onOpen(Session session) {
        this.session = session;
        webSocketSet.add(this);
        log.info("【websocket消息】有新的连接, 总数:{}", webSocketSet.size());
    }

    @OnClose
    public void onClose() {
        webSocketSet.remove(this);
        log.info("【websocket消息】连接断开, 总数:{}", webSocketSet.size());
    }

    @OnMessage
    public void onMessage(String message) {
        log.info("【websocket消息】收到客户端发来的消息:{}", message);
    }

    public void sendMessage(String message) {
        for (WebSocket webSocket: webSocketSet) {
            log.info("【websocket消息】广播消息, message={}", message);
            try {
                webSocket.session.getBasicRemote().sendText(message);
                session.getBasicRemote().sendText("这是专门给你发的信息！！");
                //还未经过测试  是否是单播 
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
    }

}

```

* 关于WebSocket框架.....



##### 前端编写Socket

```html
<#--播放音乐-->
<audio id="notice" loop="loop">
    <source src="/sell/mp3/song.mp3" type="audio/mpeg" />
</audio>
```



```js
var websocket = null;
    if('WebSocket' in window) {
        websocket = new WebSocket('ws://localhost/sell/webSocket');
    }else {
        alert('该浏览器不支持websocket!');
    }

    websocket.onopen = function (event) {
        console.log('建立连接');
    }

    websocket.onclose = function (event) {
        console.log('连接关闭');
    }

    websocket.onmessage = function (event) {
        console.log('收到消息:' + event.data)
        //弹窗提醒, 播放音乐
        $('#myModal').modal('show');

        document.getElementById('notice').play();
    }

    websocket.onerror = function () {
        alert('websocket通信发生错误！');
    }

    window.onbeforeunload = function () {
        websocket.close();
    }

//停止播放音乐 
document.getElementById('notice').pause();
//在onclick="javascript:document.getElementById('notice').pause();"
```



#### Mybatis

mapper 类

```java
public interface ProductCategoryMapper {

        //通过map定义 属性字段
    @Insert("insert into product_category(category_name, category_type) values (#{categoryName, jdbcType=VARCHAR}, #{category_type, jdbcType=INTEGER})")
    int insertByMap(Map<String, Object> map);

    //直接传入一个对象
    @Insert("insert into product_category(category_name, category_type) values (#{categoryName, jdbcType=VARCHAR}, #{categoryType, jdbcType=INTEGER})")
    int insertByObject(ProductCategory productCategory);

    //对查出来的属性做映射
    @Select("select * from product_category where category_type = #{categoryType}")
    @Results({
            @Result(column = "category_id", property = "categoryId"),
            @Result(column = "category_name", property = "categoryName"),
            @Result(column = "category_type", property = "categoryType")
    })
    ProductCategory findByCategoryType(Integer categoryType);

    //如果是多条记录，就会产出来 一个list
    @Select("select * from product_category where category_name = #{categoryName}")
    @Results({
            @Result(column = "category_id", property = "categoryId"),
            @Result(column = "category_name", property = "categoryName"),
            @Result(column = "category_type", property = "categoryType")
    })
    List<ProductCategory> findByCategoryName(String categoryName);

    //传多个参数的时候要加上这个注解以区分
    @Update("update product_category set category_name = #{categoryName} where category_type = #{categoryType}")
    int updateByCategoryType(@Param("categoryName") String categoryName,
                             @Param("categoryType") Integer categoryType);

    //通过一个对象进行更新
    @Update("update product_category set category_name = #{categoryName} where category_type = #{categoryType}")
    int updateByObject(ProductCategory productCategory);

    @Delete("delete from product_category where category_type = #{categoryType}")
    int deleteByCategoryType(Integer categoryType);

 	//xml 文件配置
    ProductCategory selectByCategoryType(Integer categoryType);
}
```

* 打印mybatis的SQL语句

  > 在yml中添加日志级别  
  >
  > ```yml
  > logging:
  > 	level:
  > 		com.supersst.dataobj.mapper: trace
  > ```

* mybatis xml文件配置

  > 在yml中添加:
  >
  > ```yml
  > mybatis:
  > 	mapper-locations: classpath:....
  > ```



### 发布

在Linux编写Service

```sh
[Unit]
Description=sell
After=syslog.target network.target

[Service]
Type=simple

ExecStart=/usr/bin/java -jar /.....jar
ExecStop=/bin/kill -15 $MAINPID

User=root
Group=root

[Install]
WanteBy=multi-uer.target
```

> 直接利用 systemctl  start ，stop ， enable ，disable 启动，自启服务



### zb 技巧

自定义banner ：[DIY banner](https://www.cnblogs.com/liuchuanfeng/p/6845528.html)

使用 //TODO 注释，可以通过idea快速跳转

ctrl + "+" or "-" 展开，收缩方法





## question

* Request方法返回页面的返回值问题
   1. modelAndview
   
      > 将  map  数据类放到 方法调用参数中？  和在方法中定义有何区别
   
      [link](https://www.cnblogs.com/tanzq/p/8687267.html)
   
   2. string
   
   3. string 可以传值给页面吗
   
* freemark 模板框架的使用

* 切面类 aspect  和 advise  以及controllerAdvise

