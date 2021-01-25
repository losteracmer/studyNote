### java note

```java
Properties properties = new Properties();
//map子类，配置文件
Class<reflect_use> reflect_useClass = reflect_use.class;
ClassLoader classLoader = reflect_useClass.getClassLoader();
InputStream is = classLoader.getResourceAsStream("study//pro.properties");
//获取类加载器
properties.load(is);
//properties加载   字节流||字符流
System.out.println(properties.get("className"));

Class<?> className = Class.forName(properties.get("className").toString());
Object o = className.newInstance();
Method method = o.getClass().getMethod(properties.get("method").toString());
method.invoke(o);
```



### annotation

​	。。。。@@

​	注解 @interface 注解是一个接口

### JDBC

```java
 static {
        Properties jdbcproperties = new Properties();
     //使用classloader 加载当前Modal ** res ** 文件夹下的资源文件
     //并且用getPath() 方法获取 绝对路径 /C:/Users/44524/IdeaProjects/IdeaFirstProject/out/production/JDBC_study/jdbcPro.properties
        ClassLoader classLoader = JDBCUtils.class.getClassLoader();
        URL res = classLoader.getResource("jdbcPro.properties");
        String path = res.getPath();
        System.out.println("jdbc配置文件路径" + path);
        try {
            jdbcproperties.load(new FileReader(path));
        } catch (IOException e) {
            e.printStackTrace();
        }
        String dbname = jdbcproperties.getProperty("dbname");
        String user = jdbcproperties.getProperty("user");
        String password = jdbcproperties.getProperty("password");
        String url = jdbcproperties.getProperty("url");

        try {
            Class.forName(url);
        } catch (ClassNotFoundException e) {
            e.printStackTrace();
        }
        try {
            conn = DriverManager.getConnection(dbname, user, password);
        } catch (SQLException e) {
            e.printStackTrace();
        }
        try {
            statement = conn.createStatement();
        } catch (SQLException e) {
            e.printStackTrace();
        }

    }
```

* ClassLoader.getResource("**这个路径是res下的相对路径**")   

* resultSet.next()   这个是首先要执行的

* resset.getXXX()   mysql 的bigInt 将会超出range

### jdbc工具类

```java
/**
 * Druid连接池的工具类
 */
public class druidUtils {

    //1.定义成员变量 DataSource
    private static DataSource ds;

    static {
        try {
            //1.加载配置文件
            Properties pro = new Properties();
            pro.load(druidUtils.class.getClassLoader().getResourceAsStream("druid.properties"));
            //2.获取DataSource
            ds = DruidDataSourceFactory.createDataSource(pro);
        } catch (IOException e) {
            e.printStackTrace();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    /**
     * 获取连接
     */
    public static Connection getConnection() throws SQLException {
        return ds.getConnection();
    }

    /**
     * 释放资源
     */
    public static void close(Statement stmt, Connection conn) {
        close(null, stmt, conn);
    }


    public static void close(ResultSet rs, Statement stmt, Connection conn) {


        if (rs != null) {
            try {
                rs.close();
            } catch (SQLException e) {
                e.printStackTrace();
            }
        }


        if (stmt != null) {
            try {
                stmt.close();
            } catch (SQLException e) {
                e.printStackTrace();
            }
        }

        if (conn != null) {
            try {
                conn.close();//归还连接
            } catch (SQLException e) {
                e.printStackTrace();
            }
        }
    }

    /**
     * 获取连接池方法
     */

    public static DataSource getDataSource() {
        return ds;
    }

}

```

### jdbcTemplate

```java
@Test
    public void test2(){
        JdbcTemplate template = new JdbcTemplate(druidUtils.getDataSource());

        String sql = "select * from labour";
        List<labour> list = 
            template.query(sql, new BeanPropertyRowMapper<labour>(labour.class));
        // BeanRowMapper 的实现类 需要传入一个Class对象
        for (labour labour : list) {	//list.for + TAB
            System.out.println(labour);
        }
    }

    /**
     * 查询cout
     * queryForObject
     */
    @Test
    public void test3() {
        JdbcTemplate template = new JdbcTemplate(druidUtils.getDataSource());

        Long cout = template.queryForObject("select count(*) from labour", long.class);
        System.out.println(cout);
    }
```



### XML

##### 约束  知道是这么回事就行

常见的约束：

 * dtd
 * schema

##### 解析  Jsoup解析

```java
String path = JsoupDemo1.class.getClassLoader().getResource("student.xml").getPath();
Document document = Jsoup.parse(new File(path),"utf-8");
Elements elements = document.getElementsByTag("name");
//Elements extends Arraylist
System.out.println("共有"+elements.size()+"个元素");
for (Element element : elements) {
    System.out.println(element.text());
}
//document same Elements Object 
//选择器
Elements ele = document.select("student[number='heima_0001']");
System.out.println(ele);
```

## Tomcat

#### 部署配置

```java
1. 直接放在webapp目录下  放war包 会自动解压
2.
config /server.xml
<Host></Host> 标签下
<Context docBase:"D:/..." path:"/path"  
3.在confi/Catalina/localhost path.xml 中放置如上文件内容
```

#####  REquest中文乱码问题

```java
Req.setEncodeing("utf-8")// 好像是。。忘了
```

##### 资源跳转

```java
req.getRequestDispatcher("/path").forWord()
```

### pink

​	 不用事先实现方法，直接写，然后alt+enter

​	提示框  confirm("提示文字")  返回 是否点击确定 

​	checkbox 直接在外面套一个form   js调用form submit() 事件

​	idea 快速查找实现类  Ctrl+alt +B





### javaWeb



###### pink

```java
tomcat8  极其+ 可以解决中文乱码问题
手动解决 :
LMString = new String(LMString.getByte("iso-8859-1"),"UTF-8");
将乱码先转化成byte数组，然后将此数组通过  指定编码转换

浏览器 storge nsession 

$.prop  是对元素的固有属性进行设置
$.attr  是对元素的固有属性 以及自定义属性（-data-）进行设置
```



###### pageBean 

```java
<a> 标签中  JavaScript:调用函数();
2  分页逻辑 (前5后4)
if totalPage < 10  
    begin = 1  end totalPage
    else if (totalPage > = 10){
    if nowP < 6 {
    begin = 1  end = 10;
    }else if(nowP < totalPage -4){
    end = totalPage;
    begin = totalPage -10;
    }else {
    begin = nowP -5;
    end = nowP +4
    }
}


```

###### 前端获取参数

```js
function getParameter(name) {
    var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)","i");
    var r = location.search.substr(1).match(reg);
    if (r!=null) return (r[2]); return null;
}
windows.decodeURIcoponent(uriCode)  对中文URI解码
```

###### js StringBuilder

```js

```

java 可变参数 

