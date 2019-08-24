## awk

sed以行为单位处理文件，awk比sed强的地方在于不仅能以行为单位还能以列为单位处理文件。**awk****缺省的行分隔符是换行，缺省的列分隔符是连续的空格和Tab**，但是行分隔符和列分隔符都可以自定义，比如/etc/passwd文件的每一行有若干个字段，字段之间以:分隔，就可以重新定义awk的列分隔符为:并以列为单位处理这个文件。awk实际上是一门很复杂的脚本语言，还有像C语言一样的分支和循环结构，但是基本用法和sed类似，awk命令行的基本形式为：

```sh
awk option 'script' file1 file2 ...
awk option -f scriptfile file1 file2 ...
```

和sed一样，awk处理的文件既可以由标准输入重定向得到，也可以当命令行参数传入，编辑命令可以直接当命令行参数传入，也可以用-f参数指定一个脚本文件，编辑命令的格式为：

```sh
/pattern/{actions}
condition{actions}
```

和sed类似，**pattern**是正则表达式，**actions**是一系列操作。awk程序一行一行读出待处理文件，如果某一行与pattern匹配，或者满足condition条件，则执行相应的actions，如果一条awk命令只有actions部分，则actions作用于待处理文件的**每一行**。比如文件testfile的内容表示某商店的库存量：

```
ProductA 30
ProductB 76
ProductC 55
```

打印每一行的第二列:

```sh
$ awk '{print $2;}' testfile
```

```
30
76
55
```

自动变量$1、$2分别表示第一列、第二列等，类似于Shell脚本的位置参数，而**$0表示整个当前行**。再比如，如果某种产品的库存量低于75则在行末标注需要订货：

```sh
$ awk '$2<75 {printf "%s\t%s\n", $0, "REORDER";} $2>=75 {print $0;}' testfile
# ; 可加 也可以 不加  printf 也可以像C中加括号，如：
$ awk '/ /{c=c+1} END {printf("%d\n",c);}' html1.html 
# 统计含有空格的行数，并最终输出
```

```sh
ProductA 30 REORDER
ProductB 76
ProductC 55 REORDER
```

awk命令的condition部分还可以是两个特殊的condition－**BEGIN和END**，对于每个待处理文件，BEGIN后面的actions在处理整个文件之前执行一次，END后面的actions在整个文件处理完之后执行一次。

awk命令可以像C语言一样使用变量（但不需要定义变量），比如统计一个文件中的空行数

```sh
$ awk '/^ *$/ {x=x+1;} END {print x;}' testfile
```

就像Shell的环境变量一样，有些awk变量是预定义的有特殊含义的：

awk常用的内建变量

```sh
FILENAME    当前输入文件的文件名，该变量是只读的
NR          当前行的行号，该变量是只读的，R代表record
NF          当前行所拥有的列数，该变量是只读的，F代表field
OFS         输出格式的列分隔符，缺省是空格
FS          输入文件的列分融符，缺省是连续的空格和Tab
ORS         输出格式的行分隔符，缺省是换行符
RS          输入文件的行分隔符，缺省是换行符
```

例如打印系统中的用户帐号列表

```sh
$ awk 'BEGIN {FS=":"} {print $1;}' /etc/passwd
# 指定列分隔符为 ： 
```

awk也可以像C语言一样使用if/else、while、for控制结构。

```sh
awk 'BEGIN {FS="<"}  {if(NF > 5) print $0}' html1.html
# 判断如果一个html文件中的一行标签大于5，则输出整行
```

