# shell

## shell历史

> Shell的作用是解释执行用户的命令，用户输入一条命令，Shell就解释执行一条，这种方式称为交互式（Interactive），Shell还有一种执行命令的方式称为批处理（Batch），用户事先写一个Shell脚本（Script），其中有很多条命令，让Shell一次把这些命令执行完，而不必一条一条地敲命令。Shell脚本和编程语言很相似，也有变量和流程控制语句，但Shell脚本是解释执行的，不需要编译，Shell程序从脚本中一行一行读取并执行这些命令，相当于一个用户把脚本中的命令一行一行敲到Shell提示符下执行。

由于历史原因，UNIX系统上有很多种Shell：

- sh（Bourne Shell）：由Steve Bourne开发，各种UNIX系统都配有sh。
- csh（C Shell）：由Bill Joy开发，随BSD UNIX发布，它的流程控制语句很像C语言，支持很多Bourne Shell所不支持的功能：作业控制，命令历史，命令行编辑。
- ksh（Korn Shell）：由David Korn开发，向后兼容sh的功能，并且添加了csh引入的新功能，是目前很多UNIX系统标准配置的Shell，在这些系统上/bin/sh往往是指向/bin/ksh的符号链接。
- tcsh（TENEX C Shell）：是csh的增强版本，引入了命令补全等功能，在FreeBSD、MacOS X等系统上替代了csh。
- bash（Bourne Again Shell）：由GNU开发的Shell，主要目标是与POSIX标准保持一致，同时兼顾对sh的兼容，bash从csh和ksh借鉴了很多功能，是各种Linux发行版标准配置的Shell，在Linux系统上/bin/sh往往是指向/bin/bash的符号链接。虽然如此，bash和sh还是有很多不同的，一方面，bash扩展了一些命令和参数，另一方面，bash并不完全和sh兼容，有些行为并不一致，所以bash需要模拟sh的行为：当我们通过sh这个程序名启动bash时，bash可以假装自己是sh，不认扩展的命令，并且行为与sh保持一致。

通过下面命令查看本机支持哪些shell

```sh
cat /etc/shells	
echo $shell  # 查看现在的shell
```

```bash
vim tec/password  # 	其中最后一列显示了用户对应的shell类型
```

```sh
root:x:0:0:root:/root:/bin/bash
bin:x:1:1:bin:/bin:/sbin/nologin
daemon:x:2:2:daemon:/sbin:/sbin/nologin
adm:x:3:4:adm:/var/adm:/sbin/nologin
lp:x:4:7:lp:/var/spool/lpd:/sbin/nologin
sync:x:5:0:sync:/sbin:/bin/sync
shutdown:x:6:0:shutdown:/sbin:/sbin/shutdown
halt:x:7:0:halt:/sbin:/sbin/halt
```

用户在命令行输入命令后，一般情况下Shell会fork并exec该命令，但是Shell的内建命令例外，执行内建命令相当于调用Shell进程中的一个函数，并不创建新的进程。以前学过的cd、alias、umask、exit等命令即是内建命令，凡是用which命令查不到程序文件所在位置的命令都是内建命令，内建命令没有单独的man手册，要在man手册中查看**内建命令**，应该执行

```sh
man bash-builtins
```

如export、shift、if、eval、[、for、while等等。内建命令虽然不创建新的进程，但也会有Exit Status，通常也用0表示成功非零表示失败，虽然内建命令不创建新的进程，但执行结束后也会有一个状态码，也可以用特殊变量$?读出。



## 执行脚本

​	编写一个简单的脚本sh1.sh：

```sh
vim sh1.sh
...
echo 'hello,world'
...
./sh1.sh
# -bash: ./sh1.sh: Permission denied 没有执行权限，拒绝执行
chmod a+x sh1.sh  # 授权
./sh1.sh # 执行成功
```

Shell脚本中用#表示注释，相当于C语言的//注释。但如果#位于第一行开头，并且是#!（称为Shebang）则例外，它表示该脚本使用后面指定的解释器/bin/sh解释执行。如果把这个脚本文件加上可执行权限然后执行

Shell会fork一个子进程并调用exec执行./sh1.sh这个程序，exec系统调用应该把子进程的代码段替换成./sh1.sh程序的代码段，并从它的start开始执行。然而sh1.sh是个文本文件，根本没有代码段和start函数，怎么办呢？其实exec还有另外一种机制，如果要执行的是一个文本文件，并且第一行用Shebang指定了解释器，则用解释器程序的代码段替换当前进程，并且从解释器的_start开始执行，而这个文本文件被当作命令行参数传给解释器。因此，执行上述脚本相当于执行程序

```bash
/bin/sh ./sh1.sh  #以这种方式执行不需要sh1.sh文件具有可执行权限。
```

如果将命令行下输入的命令用()括号括起来，那么也会fork出一个子Shell执行小括号中的命令，一行中可以输入由分号;隔开的多个命令，比如：

```bash
(cd ..;ls -l)  # 因为是fork出新的进程，所以运行结束后，当前目录还是原来的目录
```

和上面两种方法执行Shell脚本的效果是相同的，cd ..命令改变的是子Shell的PWD，而不会影响到交互式Shell。然而命令

```bash
cd ..;ls -l
```

则有不同的效果，cd ..命令是直接在交互式Shell下执行的，改变交互式Shell的PWD，然而这种方式相当于这样执行Shell脚本：

```bash
source ./sh1.sh
```

或者

```bash
. ./sh1.sh
```

source或者.命令是Shell的内建命令，这种方式也不会创建子Shell，而是直接在交互式Shell下逐行执行脚本中的命令。

## 基本语法

### 变量

按照惯例，Shell变量通常由字母加下划线开头，由任意长度的字母、数字、下划线组成。有两种类型的Shell变量：

1. 环境变量

环境变量可以**从父进程传给子进程**，因此Shell进程的环境变量可以从当前Shell进程传给fork出来的子进程。用`printenv`命令可以显示当前Shell进程的环境变量。

2. 本地变量

只存在于当前Shell进程，用set命令可以显示当前Shell进程中定义的所有变量（包括本地变量和环境变量）和函数。

环境变量是任何进程都有的概念，而本地变量是Shell特有的概念。在Shell中，环境变量和本地变量的定义和用法相似。在Shell中定义或赋值一个变量：

```sh
VARNAME=value
```

注意等号两边都**不能有空格**，否则会被Shell解释成命令和命令行参数。

一个变量定义后仅存在于当前Shell进程，它是**本地变量**，用export命令可以把本地变量导出为环境变量，定义和导出环境变量通常可以一步完成：

```sh
export VARNAME=value
```

也可以分两步完成：

```sh
VARNAME=value
export VARNAME
```

用**unset**命令可以**删除**已定义的环境变量或本地变量。

```sh
unset VARNAME
```

如果一个变量叫做VARNAME，用 ' VARNAME ' 可以表示它的值，在不引起歧义的情况下也可以用VARNAME表示它的值。通过以下例子比较这两种表示法的不同：

```sh
echo $SHELL
```

注意，在定义变量时不用`'`取变量值时要用。和C语言不同的是，Shell变量不需要明确定义类型，事实上Shell变量的值都是字符串，比如我们定义VAR=45，其实VAR的值是字符串45而非整数。Shell变量不需要先定义后使用，如果对一个没有定义的变量取值，则值为空字符串。(emmmm,还说js不是脚本语言)

### 文件名代换（Globbing）

这些用于匹配的字符称为通配符（Wildcard），如：* ? [ ] 具体如下：

```sh
#	* 匹配0个或多个任意字符
#	? 匹配一个任意字符
#	[若干字符] 匹配方括号中任意一个字符的一次出现

ls /dev/ttyS*
ls ch0?.doc
ls ch0[0-2].doc
ls ch[012] [0-9].doc

```

注意，Globbing所匹配的文件名是由Shell展开的，也就是说在参数还没传给程序之前已经展开了，比如上述ls ch0[012].doc命令，如果当前目录下有ch00.doc和ch02.doc，则传给ls命令的参数实际上是这两个文件名，而不是一个匹配字符串。

### 命令代换

由反引号括起来的也是一条命令，Shell先执行该命令，然后将输出结果立刻代换到当前命令行中。例如定义一个变量存放date命令的输出：

```sh
DATE=`date`
```

```sh
echo $DATE
```

> 如果直接执行 `date``  会提示Web not found 这就说明执行这条命令的时候，是将输出结果直接执行了，但是自己写的sh脚本却是只是输出了结果 

命令代换也可以用$()表示：

```sh
DATE=$(date)
```

### 算术代换

使用$(())，用于算术计算，(())中的Shell变量取值将转换成整数，同样含义的$[ ]等价例如：

```sh
VAR=45
echo $(($VAR+3))   等价于   echo $[VAR+3]或 $[$VAR+3]
```

$(())中只能用+-*/和()运算符，并且只能做整数运算。

$[base#n]，其中base表示进制，n按照base进制解释，后面再有运算数，按十进制解释。

```sh
echo $[2#10+11]
echo $[8#10+11]
echo $[16#10+11]
```

### 转义字符

和C语言类似，\在Shell中被用作转义字符，用于去除紧跟其后的单个字符的特殊意义（回车除外），换句话说，紧跟其后的字符取字面值。例如：

```sh
echo $SHELL
#/bin/bash
echo \$SHELL
#$SHELL
itcastecho \\
#\
```

比如创建一个文件名为“$”的文件（$间含有空格）可以这样：

```sh
itcasttouch \$\ \$
```

还有一个字符虽然不具有特殊含义，但是要用它做文件名也很麻烦，就是-号。如果要创建一个文件名以-号开头的文件，这样是不正确的：

```sh
touch -hello
#touch: invalid option -- h
#Try `touch --help' for more information.
```

即使加上\转义也还是报错：

```sh
touch \-hello
touch: invalid option -- h
Try `touch --help' for more information.
```

因为各种UNIX命令都把-号开头的命令行参数当作命令的选项，而不会当作文件名。如果非要处理以-号开头的文件名，可以有两种办法：

```sh
touch ./-hello
```

或者

```sh
touch -- -hello
```

\还有一种用法，在\后敲回车表示续行，Shell并不会立刻执行命令，而是把光标移到下一行，给出一个续行提示符>，等待用户继续输入，最后把所有的续行接到一起当作一个命令执行。例如：

```sh
ls \
\> -l
#（ls -l命令的输出）
```

### 单引号

和C语言同，Shell脚本中的单引号和双引号一样都是字符串的界定符（双引号下一节介绍），而不是字符的界定符。单引号用于保持引号内所有字符的字面值，即使引号内的\和回车也不例外，但是字符串中不能出现单引号。如果引号没有配对就输入回车，Shell会给出续行提示符，要求用户把引号配上对。例如：

```sh
echo '$SHELL'
$SHELL
echo 'ABC\（回车）
> DE'（再按一次回车结束命令）
ABC\
DE
```

### 双引号

被双引号用括住的内容，将被视为单一字串。它防止通配符扩展，但允许变量扩展。这点与单引号的处理方式不同

```sh
DATE=$(date)
echo "$DATE" #Wed Aug 21 11:10:40 UTC 2019
echo '$DATE' #$DATE
```

## Shell脚本语法

### 条件测试

**命令test**或 [ 可以测试一个条件是否成立，如果测试结果为真，则该命令的Exit Status为0，如果测试结果为假，则命令的Exit Status为1（注意与C语言的逻辑表示正好相反）。例如测试两个数的大小关系：

```sh
a=2
test $a -gt 1
echo $?
#0
```

> -gt 是比较大小的转义

虽然看起来很奇怪，但左方括号
[ 确实是一个命令的名字，传给命令的各参数之间应该用空格隔开，比如：$VAR、-gt、3、] 是 [ 命令的四个参数，它们之间必须用空格隔开。命令test或 [ 的参数形式是相同的，只不过test命令不需要 ] 参数。以 [ 命令为例，常见的测试命令如下表所示：

```
[ -d DIR ] 如果DIR存在并且是一个目录则为真
[ -f FILE ] 如果FILE存在且是一个普通文件则为真
[ -z STRING ] 如果STRING的长度为零则为真
[ -n STRING ] 如果STRING的长度非零则为真
[ STRING1 = STRING2 ] 如果两个字符串相同则为真
[ STRING1 != STRING2 ] 如果字符串不相同则为真
[ ARG1 OP ARG2 ] ARG1和ARG2应该是整数或者取值为整数的变量，OP是-eq（等于）-ne（不等于）-lt（小于）-le（小于等于）-gt（大于）-ge（大于等于）之中的一个
```

和C语言类似，测试条件之间还可以做与、或、非逻辑运算：

```
[ ! EXPR ] EXPR可以是上表中的任意一种测试条件，!表示“逻辑反(非)”
[ EXPR1 -a EXPR2 ] EXPR1和EXPR2可以是上表中的任意一种测试条件，-a表示“逻辑与” and
[ EXPR1 -o EXPR2 ] EXPR1和EXPR2可以是上表中的任意一种测试条件，-o表示“逻辑或” or 
```

```sh
VAR=abc
[ -d Desktop -a $VAR = 'abc' ]
echo $?
0
```

注意，如果上例中的$VAR变量事先没有定义，则被Shell展开为空字符串，会造成测试条件的语法错误（展开为[ -d Desktop -a = ‘abc’ ]），作为一种好的**Shell**编程习惯**，**应该总是把变量取值放在双引号之中（展开为[ -d Desktop -a “” = ‘abc’ ]）：

```sh
unset VAR	
[ -d Desktop -a $VAR = 'abc' ]
bash: [: too many arguments
[ -d Desktop -a "$VAR" = 'abc' ]
echo $?
1
```

### 分支

#### if/then/elif/else/fi

和C语言类似，在Shell中用if、then、elif、else、fi这几条命令实现分支控制。这种流程控制语句本质上也是由若干条Shell命令组成的，例如先前讲过的

```sh
if [ -f ~/.bashrc ]; then
	. ~/.bashrc
fi
```

其实是三条命令，if [ -f ∼/.bashrc ]是第一条，then . ∼/.bashrc是第二条，fi是第三条。如果两条命令写在同一行则**需要用 `; `号隔开**，一行只写一条命令就不需要写`;`号了，另外，then后面有换行，但这条命令没写完，Shell会自动续行，把下一行接在then后面当作一条命令处理。和[命令一样，要注意命令和各参数之间必须用空格隔开。if命令的参数组成一条子命令，如果该子命令的Exit Status为0（表示真），则执行then后面的子命令，如果Exit Status非0（表示假），则执行elif、else或者fi后面的子命令。if后面的子命令通常是测试命令，但也可以是其它命令。Shell脚本没有{}括号，所以用fi表示if语句块的结束。见下例：

```sh
#! /bin/sh

if [ -f /bin/bash ]
then 
	echo "/bin/bash is a file"
else 
	echo "/bin/bash is NOT a file"
elif [-d /bin/bash]
then
	echo "/bin/bash is a dir"
fi
if :; then echo "always true"; fi
```

`:`是一个特殊的命令，称为空命令，该命令不做任何事，但Exit Status总是真。此外，也可以执行/bin/true或/bin/false得到真或假的Exit Status。再看一个例子：

```sh
#! /bin/sh

echo "Is it morning? Please answer yes or no."
read YES_OR_NO
if [ "$YES_OR_NO" = "yes" ]; then
	echo "Good morning!"
elif [ "$YES_OR_NO" = "no" ]; then
	echo "Good afternoon!"
else
	echo "Sorry, $YES_OR_NO not recognized. Enter yes or no."
	exit 1
fi
exit 0
```

上例中的read命令的作用是等待用户输入一行字符串，将该字符串存到一个Shell变量中。

此外，Shell还提供了&&和||语法，和C语言类似，具有Short-circuit特性，很多Shell脚本喜欢写成这样：

```sh
test "$(whoami)" != 'root' && (echo you are using a non-privileged account; exit 1)
```

&&相当于“if…then…”，而||相当于“if not…then…”

> 当判断条件为&& 时，执行到第一个为false的就停止判断后面的了，如果为||，则遇到一个为true的就不执行后面的了

&&和||用于连接两个命令，而上面讲的-a和-o仅用于在测试表达式中连接两个测试条件，要注意它们的区别，例如：

```sh
test "$VAR" -gt 1 -a "$VAR" -lt 3
```

和以下写法是等价的:

```sh
test "$VAR" -gt 1 && test "$VAR" -lt 3
```

#### case/esac

case命令可类比C语言的switch/case语句，esac表示case语句块的结束。C语言的case只能匹配整型或字符型常量表达式，而Shell脚本的case可以匹配字符串和Wildcard，**每个匹配分支可以有若干条命令，末尾必须以;;结束**，执行时找到第一个匹配的分支并执行相应的命令，然后直接跳到esac之后，不需要像C语言一样用break跳出。

```sh
#! /bin/sh

echo "Is it morning? Please answer yes or no."
read YES_OR_NO
case "$YES_OR_NO" in
yes|y|Yes|YES)
	echo "Good Morning!";;
[nN]*)
	echo "Good Afternoon!";;
*)
	echo "Sorry, $YES_OR_NO not recognized. Enter yes or no."
	exit 1;;
esac
exit 0
```

> 如果用source 执行这个脚本，你当前的会话将会推出

使用case语句的例子可以在系统服务的脚本目录/etc/init.d中找到。这个目录下的脚本大多具有这种形式（以/etc/init.d/nfs-kernel-server为例）：

```sh
case "$1" in
	start)
		...
	;;
	stop)
		...
	;;
	reload | force-reload)
		...
	;;
	restart)
		...
	*)
	    log_success_msg"Usage: nfs-kernel-server {start|stop|status|reload|force-reload|restart}"
	    exit 1
	;;
esac
```

启动nfs-kernel-server服务的命令是

```sh
$ sudo /etc/init.d/nfs-kernel-server start
```

> 这里的 `$n` n就是你传入的第几个参数

### 循环

#### for/do/done

Shell脚本的for循环结构和C语言很不一样，它类似于某些编程语言的foreach循环。例如：

```sh
#! /bin/sh
for FRUIT in apple banana pear; do

echo "I like $FRUIT"
done
```

FRUIT是一个循环变量，第一次循环$FRUIT的取值是apple，第二次取值是banana，第三次取值是pear。再比如，要将当前目录下的chap0、chap1、chap2等文件名改为chap0`~`、chap1`~`、chap2`~`等（按惯例，末尾有~字符的文件名表示临时文件），这个命令可以这样写：

```sh
$ for FILENAME in chap?; do mv $FILENAME $FILENAME~; done
```

也可以这样写：

```sh
$ for FILENAME in `ls chap?`; do mv $FILENAME $FILENAME~; done
```

循环一定次数

```sh
for ((i=1;i<3;i++));
do
echo $i 
done
# 第一行的 ; 不是一定必须的？
```



#### while/do/done

while的用法和C语言类似。比如一个验证密码的脚本：

```sh
#! /bin/sh

echo "Enter password:"
read TRY
while [ "$TRY" != "secret" ]; do
echo "Sorry, try again"
read TRY
done
```

下面的例子通过算术运算控制循环的次数：

```sh
#! /bin/sh
COUNTER=1
while [ "$COUNTER" -lt 10 ]; do

echo "Here we go again"

COUNTER=$(($COUNTER+1))

done
```

另，Shell还有until循环，类似C语言的do…while。

#### break和continue

break[n]可以指定跳出几层循环；continue跳过本次循环，但不会跳出循环。

即break跳出，continue跳过。

### 位置参数和特殊变量

有很多特殊变量是被Shell自动赋值的，我们已经遇到了$?和$1。其他常用的位置参数和特殊变量在这里总结一下：

```sh
$0 			相当于C语言main函数的argv[0]
$1、$2...	这些称为位置参数（Positional Parameter），相当于C语言main函数的argv[1]、argv[2]...
$# 			相当于C语言main函数的argc - 1(参数的个数)，注意这里的#后面不表示注释
$@ 			表示参数列表"$1" "$2" ...，例如可以用在for循环中的in后面。
$* 			表示参数列表"$1" "$2" ...，同上
$? 			上一条命令的Exit Status
$$ 			当前进程号
```

位置参数可以用shift命令左移。比如shift 3表示原来的$4现在变成$1，原来的$5现在变成$2等等，原来的$1、$2、$3丢弃，$0不移动。不带参数的shift命令相当于shift 1。例如：

```sh
#! /bin/sh

echo "The program $0 is now running"
echo "The first parameter is $1"
echo "The second parameter is $2"
echo "The parameter list is $@"
shift  # 	
echo "The first parameter is $1"
echo "The second parameter is $2"
echo "The parameter list is $@"
```

> 输出结果
>
> ```
> # ./shift.sh a b c d e f 
> The program ./shift.sh is now running
> The first parameter is a
> The second parameter is b
> The parameter list is a b c d e f
> The first parameter is b
> The second parameter is c
> The parameter list is b c d e f
> ```
>
> 每次调用一次shift，将参数列表对列出队列

### 输入输出

#### echo

显示文本行或变量，或者把字符串输入到文件。

```sh
echo [option] string
-e #解析转义字符
-n #不回车换行。默认情况echo回显的内容后面跟一个回车换行。
echo "hello\n\n"
echo -e "hello\n\n"
echo "hello"
echo -n "hello"
```

#### 管道

可以通过 | 把一个命令的输出传递给另一个命令做输入。

```sh
cat myfile | more
ls -l | grep "myfile"
df -k | awk '{print $1}' | grep -v "文件系统"
df -k 查看磁盘空间，找到第一列，去除“文件系统”，并输出
```

#### tee

tee命令把结果输出到标准输出，顺便输出到相应文件。

```sh
df -k | awk '{print $1}' | grep -v "文件系统" | tee a.txt
```

tee -a a.txt表示追加操作。

```sh
df -k | awk '{print $1}' | grep -v "文件系统" | tee -a a.txt
```

#### 文件重定向

```sh
cmd > file 				把标准输出重定向到新文件中
cmd >> file 			追加
cmd > file 2>&1 		标准出错也重定向到1所指向的file里
cmd >> file 2>&1
cmd < file1 > file2 	输入输出都定向到文件里
cmd < &fd 				把文件描述符fd作为标准输入
cmd > &fd 				把文件描述符fd作为标准输出
cmd < &- 				关闭标准输入
```

> 2 代表文件描述符 ERROR 错误，然后在  2>&1  将错误输出到屏幕，相当于又重定向到文件
>
> 例如 ls -l notExistFile >file 2>&1  

### 函数

和C语言类似，Shell中也有函数的概念，但是函数定义中没有返回值也没有参数列表。例如：

```sh
#! /bin/sh

foo(){ echo "Function foo is called";}
echo "-=start=-"
foo
echo "-=end=-"
```

注意函数体的左花括号 { 和后面的命令之间必须有空格或换行，如果将最后一条命令和右花括号 } 写在同一行，**命令末尾必须有分号;**。但，不建议将函数定义写至一行上，不利于脚本阅读。

在定义foo()函数时并不执行函数体中的命令，就像定义变量一样，只是给foo这个名一个定义，到后面调用foo函数的时候（注意Shell中的函数调用不写括号）才执行函数体中的命令。Shell脚本中的函数**必须先定义后调用**，一般把函数定义语句写在脚本的前面，把函数调用和其它命令写在脚本的最后（类似C语言中的main函数，这才是整个脚本实际开始执行命令的地方）。

Shell函数没有参数列表并不表示不能传参数，事实上，函数就像是迷你脚本，调用函数时可以传任意个参数，在函数内同样是用$0、$1、$2等变量来提取参数，函数中的位置参数相当于函数的局部变量，改变这些变量并不会影响函数外面的$0、$1、$2等变量。函数中可以用return命令返回，如果return后面跟一个数字则表示函数的Exit Status。

下面这个脚本可以一次创建多个目录，各目录名通过命令行参数传入，脚本逐个测试各目录是否存在，如果目录不存在，首先打印信息然后试着创建该目录。

```sh
#! /bin/sh

is_directory()
{
	DIR_NAME=$1
	if [ ! -d $DIR_NAME ]; then
		return 1
	else
		return 0
	fi
}
for DIR in "$@"; do
	if is_directory "$DIR"
	then :
	else
		echo "$DIR doesn't exist. Creating it now..."
		mkdir $DIR > /dev/null 2>&1
		if [ $? -ne 0 ]; then
			echo "Cannot create directory $DIR"
			exit 1
		fi
	fi
done
```

**注意：is_directory()返回0表示真返回1表示假。**

## Shell脚本调试方法

Shell提供了一些用于调试脚本的选项，如：

* -n               读一遍脚本中的命令但不执行，用于检查脚本中的语法错误。

* -v               一边执行脚本，一边将执行过的脚本命令打印到标准错误输出。

* -x               提供跟踪执行信息，将执行的每一条命令和结果依次打印出来。

这些选项有三种常见的使用方法：

1. 在命令行提供参数。如：

    ```sh
$ sh -x ./script.sh
    ```

2. 在脚本开头提供参数。如：

   ```sh
   #! /bin/sh -x
   ```

3. 在脚本中用set命令启用或禁用参数。如：

    ```sh
    #! /bin/sh
    if [ -z "$1" ]; then
        set -x
        echo "ERROR: Insufficient Args."
        exit 1
        set +x
    fi
    ```

set -x和set +x分别表示启用和禁用-x参数，这样可以只对脚本中的某一段进行跟踪调试。

