## sed

sed意为流编辑器（Stream Editor），在Shell脚本和Makefile中作为过滤器使用非常普遍，也就是把前一个程序的输出引入sed的输入，经过一系列编辑命令转换为另一种格式输出。sed和vi都源于早期UNIX的ed工具，所以很多sed命令和vi的末行命令是相同的。

sed命令行的基本格式为:

```sh
sed option 'script' file1 file2 ...
sed option -f scriptfile file1 file2 ...
```

选项含义：

```sh
--version 				显示sed版本。
--help					显示帮助文档。
-n,--quiet,--silent 	静默输出，默认情况下，sed程序在所有的脚本指令执行完毕后，将自动打印模式空间中的内容，这些选项可以屏蔽自动打印。
-e script 				允许多个脚本指令被执行。
-f script-file,
--file=script-file 		从文件中读取脚本指令，对编写自动脚本程序来说很棒！
-i,--in-place 			直接修改源文件，经过脚本指令处理后的内容将被输出至源文件（源文件被修改）慎用！
-l N, --line-length=N 	该选项指定l指令可以输出的行长度，l指令用于输出非打印字符。
--posix 				禁用GNU sed扩展功能。
-r, --regexp-extended 	在脚本指令中使用扩展正则表达式
-s, --separate 			默认情况下，sed将把命令行指定的多个文件名作为一个长的连续的输入流。而GNU sed则允许把他们当作单独的文件，这样如正则表达式则不进行跨文件匹配。
-u, --unbuffered 		最低限度的缓存输入与输出。
```

以上仅是sed程序本身的选项功能说明，至于具体的脚本指令（即对文件内容做的操作）后面我们会详细描述，这里就简单介绍几个脚本指令操作作为sed程序的例子。

```sh
a,	append 			追加
i,	insert 			插入
d,	delete 			删除
s,	substitution 	替换
```

如：`$ sed "2a itcast" ./testfile` 在输出testfile内容的第二行后添加"itcast"。

`$ sed "2,5d" testfile` 删除2到5行

sed处理的文件既可以由标准输入重定向得到，也可以当命令行参数传入，命令行参数可以一次传入多个文件，sed会依次处理。sed的编辑命令可以直接当命令行参数传入，也可以写成一个脚本文件然后用-f参数指定，编辑命令的格式为：

```sh
/pattern/action
```

其中pattern是正则表达式，action是编辑操作。sed程序一行一行读出待处理文件，如果某一行与pattern匹配，则执行相应的action，如果一条命令没有pattern而只有action，这个action将作用于待处理文件的每一行。

### 常用sed命令

```shell
/pattern/p 打印匹配pattern的行
/pattern/d 删除匹配pattern的行
/pattern/s/pattern1/pattern2/ 查找符合pattern的行，将该行第一个匹配pattern1的字符串替换为pattern2
/pattern/s/pattern1/pattern2/g 查找符合pattern的行，将该行所有匹配pattern1的字符串替换为pattern2
```

使用p命令需要注意，sed是把待处理文件的内容连同处理结果一起输出到标准输出的，因此p命令表示除了把文件内容打印出来之外还额外打印一遍匹配pattern的行。比如一个文件testfile的内容是

```makefile
123
abc
456
```

执行打印含有abc行的sed语句

```sh
$ sed '/abc/p' testfile
123
abc
abc
456
```

要想只输出处理结果，应加上-n选项，这种用法相当于grep命令

```sh
$ sed -n '/abc/p' testfile
abc
```

使用d命令就不需要-n参数了，比如删除含有abc的行

```sh
$ sed '/abc/d' testfile
123
456
```

**注意**，sed命令**不会修改原文件**，删除命令只表示某些行不打印输出，而不是从原文件中删去。

使用查找替换命令时，可以把匹配pattern1的字符串复制到pattern2中，比如：

```sh
$ sed 's/bc/-&-/' testfile
123
a-bc-
456
#pattern2中的&表示原文件的当前行中与pattern1相匹配的字符串
```

```sh
$ sed '/west/s/\(es\)/-\1-/' file1
# 将含有west的行中 第一个 es  替换成 -es-  \1  和正则中的一样代表第一个括号中匹配到的串
```

pattern2中的\1表示与pattern1的第一个()括号相匹配的内容，\2表示与pattern1的第二个()括号相匹配的内容。sed默认使用Basic正则表达式规范，如果指定了-r选项则使用Extended规范，那么()括号就不必转义了。如：

```sh
sed -r 's/([0-9])([0-9])/-\1-~\2~/' out.sh
```

替换结束后，所有行，含有连续数字的第一个数字前后都添加了“-”号；第二个数字前后都添加了“~”号。

**可以一次指定多条不同的替换命令**，用“;”隔开：

```sh
$ sed 's/yes/no/;s/static/dhcp/' ./testfile
#注：使用分号隔开指令。
```

也可以使用`-e`参数来指定不同的替换命令，有几个替换命令需添加几个 -e 参数：

```sh
$ sed -e 's/yes/no/' -e 's/static/dhcp/' testfile
#注：使用-e选项。
```

如果testfile的内容是:

```html
<html><head><title>Hello World</title></head>
<body>Welcome to the world of regexp!</body></html>
```

现在要去掉所有的HTML标签，使输出结果为：

```
Hello World
Welcome to the world of regexp!
```

怎么做呢？如果用下面的命令

```sh
$ sed 's/<.*>//g' testfile
```

结果是两个空行，把所有字符都过滤掉了。这是因为，正则表达式中的数量限定符会匹配尽可能长的字符串，这称为贪心的(Greedy)。比如sed在处理第一行时，<.*>匹配的并不是`<html>`或`<head>`这样的标签，而是

```html
<html><head><title>Hello World</title>
```

这样一整行，因为这一行开头是<，中间是若干个任意字符，末尾是>。那么这条命令怎么改才对呢？

```sh
 sed 's/<[^<>]*>//g' html1.html 
```

> 理解一下，我们要把尖括号中的字符替换成空（包括尖括号），根据正则的贪心原则，可能会从头匹配到尾，所以我们加以限定，用`'<[^<>]>'` 来代表由尖括号包着的，且内容不包含尖括号的符号，然后将他替换了就好了 























