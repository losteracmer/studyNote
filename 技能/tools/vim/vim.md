## vim 编辑器

> vim是从vi发展过来的一款文本编辑器

### 中文文档

```sh
$wget https://nchc.dl.sourceforge.net/project/vimcdoc/vimcdoc/1.5.0/vimcdoc-1.5.0.tar.gz  
```

* 解压  tar -zxvf vimcdoc-1.5.0.tar.gz
* 运行安装命令   $sudo ./vimcdoc.sh -i

切换中/英文模式

```
:set helplang=en/cn
```

帮助文档的打开/回退

```
ctrl + ]
ctrl + o
```

查看帮助文档

```
:help {快捷键或者相关主题}
:help CTRL-A  控制字符的帮助
:help i_CTRL-H  #insert 模式
:help v_CTRL-H  #Visal 模式
:help c_CTRL-H  #Command 模式
:help E37  #查看错误码
# 按下table #可以匹配前缀的帮助主题
# 按下Ctrl + D #都列出来

# 帮助主题  分组匹配
:helpgrep pattern  # 进入后可以进行如下操作
:cn
:cN :cprev
:cfirst
:clast
```

### 工作模式:

1. 命令模式 -- 打开文件之后, 默认进入命令模式
2. 编辑模式 -- 需要输入一些命令, 切换到编辑模式
3. 末行模式 -- 在末行模式下可以输入一些命令

### 移动命令

```
w  单词移动
b  反向单词移动

e  光标移动到word的最后一个字符上
ge  光标移动到word的前一个字符上
```

**大写命令**

```
W
B
E
gE
# 跳到是non-word 的特殊字符 比如".","-"
```

**翻页快捷键**

ctr+f ：向后翻整页
ctr+b ：向前翻整页

**搜索跳转**

```
fx  # 搜索本行字符x
3fx  # 搜索第三个x符号
Fx  # 反向 
3Fx  # 反向 

t  # 类似，只不过光标停留在前一个字符上
T  # 方向相反 光标在下一个字符上

% # 在 (){}[] 之间跳转
```

**跳转行号**

```
[num]G  #跳转到num行
gg  #跳转到第一行  相当于1G
G  #到最后一行
50%  #光标到文档的百分之位行上
C-G  # 查看当前命令的行号，百分比
:set nu[mber]  # 显示行号
:set nonu[mber]
:set ruler  # 右下角显示光标信息
:set noruler
```

**滚屏操作**

```
C-u   #  up  向上滚动一半屏幕
C-d   #  down  向下滚动一半屏幕
C-e   # 文本向下一行
C-y   # 文本向上一行
C-f   #向后翻一页  forward
C-b   #向前翻一页  backward
zz  # 将当前行放到正中间
zt  # 放到屏幕顶端 top
zb  # bottom
```

**搜索命令**

直接V模式下按 `/`

模式：`/string`  查找包含string的

n,N 下一次，上一次 ，当然也可以加数字

如果是无法搜索的特殊字符，可以用 `\`进行转义  比如 ： `. ~ $ ^`

`:set ignorecase`  `:set noignorcase` 设置是否搜索忽略大小写

光标放到单词上直接按 `*` `#` 就可以进行向下，向上搜索

`/string`\> 查找以string 结束的单词

`/\<`查找以string开始的

`/\<word\>` 完整包含word的

高亮搜索: `:set hlsearch`  `:set nohlserch`

`:nohlsearch`  去掉当前的高亮显示

`:set incsearch`  `:set noincsearch`  开启关闭 即时搜索，每输入一个字符就进行搜索

`:set wrapscan`  `:set nowapscan `  开启 关闭 收到文件尾部会向另一个方向进行搜索

正则搜索

> 正则无敌

`^`  `$`  `.`  开头，结尾，统配

**标记**

`    ```   跳转会原来的位置

跳转： G   搜索

C-o  跳转到前一个光标停留的命令

C-i  反向跳转

标记的使用

打标记: m + x  （x是一个标记符号可以是a-z 0-1)

跳转到标记 ` + x  到标记位置  |  ' + x 跳转到标记行首

`:marks`  显示所有标记

> set all 查看所有设置

   **小幅修改**

dw  删除一个单词，包括单词后的空格（delete word）

d4w 删除四个单词

de  删除光标到单词尾部，不包括空格

d$  d0  行尾或者行首

cc 改变整行，删除整行，但是不改变so

:read /Path/file  将file文件的内容读取到当前打开的文件中

快捷命令

:set filetype=vim   设置文件类型

```sh
x = dl

X = dh

D = d$

C = c$

s = cl

S = cc
```

**删除**

```
daw  删除一个单词(包括后边的空格)
diw  删除一个单词，但是不包括空格

cis  change inner sentence 修改一个句子(由.进行分割的)

dG 删除从光标到文末尾所有的内容
dgg  删除当前到文本头所有内容

~ 改变大小写

```

按R  进入insert模式,esc 结束

### 常用快捷键

```sh
命令模式下的操作:
	1>. 光标的移动
				k
			H        L
				j
		前  下  上  后
		行首: 0
		行尾: $
		文件开始位置: gg
		文件末尾: G
		行跳转: 300G
	2>. 删除操作
			删除光标后边的字符: x
			........前......: 大X
			........单词: dw  (光标移动到单词的开始位置, 否只能删除一部分)
			...光标到行首的字符串: d0
			.........行尾.......: D(d$)
			删除光标当前行: dd
			删除多行: ndd (n -- 自然数)
	3>. 撤销操作
				撤销: u
				反撤销: ctrl + r

	4>. 复制粘贴
				复制: yy or Y
				复制多行: nyy
				复制单词：yw  
				复制n个单词：ynw
				复制到行尾：y$  y0
				粘贴: p (光标所在行的下一行)
				粘贴: P (光标所在行)

				剪切 == 删除
		5>. 可视模式
				切换到可是模式: v
				选择内容: hjkl
				操作: 复制: y   删除: d
		6>. 查找操作
				1). /hello
				2). ?hello
				3). # -- 把光标移动到查找的单词身上 , 按#
				遍历时候的快捷键: N/n
		7>. r: 替换当前字符

		缩进:
				向右: >>
				向左: <<
		8>. 查看man文档
	文本模式下的操作:
		切换到文本模式:
			a -- 在光标所在位置的后边插入
			A -- 在当前行的尾部插入

			i -- 在光标所在位置的前边插入
			I -- 在光标所在行的行首插入

			o -- 在光标所在行的下边开辟一个新的行
			O -- .............上.........

			s -- 删除光标后边的字符
			S -- 删除光标所在的行
	末行模式下的操作:
			查找: :s/tom/jack/g
						:%s/tom/jack/
						:20,25s/tom/jack/g
			保存退出:
				q: 退出
				q!: 退出不保存
				w: 保存
				wq: 保存退出
				x: == wq
	在命令模式下保存退出: ZZ
	分屏操作:
		1>. 水平分屏  sp
		2>. 垂直分屏  vsp
		分屏之间切换： 
```

### 分屏

```
vim的分屏功能

总结起来，基本都是ctrl+w然后加上某一个按键字母，触发一个功能。
（1）在shell里打开几个文件并且分屏:
　　vim -On file1 file2 ...
　　vim -on file1 file2 ...

大O表示垂直分割(vertical)，小o表示水平分割（默认horizontal），后面的n表示分几个屏，实际上我觉得不用写，默认按后面要分割的文件数来决定分几个屏。
（2）在vim里打开一个分屏:
　　创建空白分屏：
　　:new
　　打开任意文件：
　　:vsplit(:vsp) filename
　　:sp(split) filename
　　打开当前文件：
　　ctrl+w 和 s(split)
　　ctrl+w 和 v(vsplit)

（3）关闭一个分屏:
　　:only 或者 ctrl+w 和 o取消其它分屏，只保留当前分屏
　　ctrl+w 和 c(close)
　　只剩最后一个分屏以后推出：
　　ctrl+w 和 q(quit)
（4）移动光标，也就是切换分屏；也可以移动分屏，比如将左分屏移动到右边。
　　ctrl+w 和 w（各种切换，只有两个分屏的时候还是比较方便的）
　　ctrl+w 和 h(H) 左
　　ctrl+w 和 j(J) 下
　　ctrl+w 和 k(K) 上
　　ctrl+w 和 l(L) 右
（5）最后就是改变分屏尺寸的操作了。
　　ctrl+w 和 < 左
　　ctrl+w 和 > 右
　　ctrl+w 和 + 上
　　ctrl+w 和 - 下
　　ctrl+w 和 = 恢复均等
```

### 编辑多个文件

:edit[!]  filename 关闭当前文件去编辑另一个，不保存

hide edit filename   隐藏缓冲区内容，直接修改编辑另一个文件

---

vim file1 file2 file3  打开多个文件，默认是第一个

:args  打开文件的参数列表

:args  从新定义打开的文件参数

:[n]next[!] 进入下一[n]个文件

:wnext   write next  保存修改并进入下一个文件
:[w]previous   [保存]上一个文件

:last  打开最后一个文件

:first 打开第一个文件

:set [no] autowrite  在不同文件之间切换时，自动保存

C-^ 在两个文件中快速切换

:set backup  生成备份文件（需要保存:w 后才会生成一个filename~）

:set backupext=~  设置备份文件的文件后缀

:set patchmode=.org  设置保存前 文件后缀

---

复制文件，需要在复制后（y）打开新文件 `:edit newfile`,然后p粘贴

寄存器复制：

输入 `"[寄存器a-z]y` 将内容复制到寄存器中

粘贴 `"[寄存器a-z]p` 将寄存器中的内容粘贴

`"[a-z]yas`  as    a sentense  复制一句话(含有.)

`"[a-z]daw`  删除一个单词，并放到寄存器中

> `"[a-z] + cmd` 对于寄存器的操作

---

**向文件中追加内容**

:read note06.txt   :向当前文件进行追加note06.txt文件内容.

:write >> note06.txt :将当前文件追加到文件名为note06.txt文件中去,只能追加到文件的最后.

:write newfile :将当前文件写入到newfile 中去

:saveas filename  另存为

:file newname  将文件改名  同上

### other

配合数字使用

```
:数字n,`a`,内容,`esc`    # 会将内容重复输入n次
```

```
:数字n,x 删除n个字符
```

放弃所有的编辑直接退出

```
:e!
```

### 常用设置

：map    设置一个按键映射 ，将一些列命令映射到指定的按键，很方便

：options    打开选项，，按回车可以设置

：set oneOptions&  将某个选项设置成默认值

```
:set nowrap  不要折行
:set sidescroll=10 | 0 左右滚动的屏幕偏移量
:set whichwrap=b,s [,<,>][,[,]]  跨行命令，智能上上下下
:set iskeyword=@,48-57,_,192-255 将其中的ASCII，@（字母） 看做一个整体字符，按b或者w跳过完整的字符
:set iskeyword+=
:set iskeyword-=  添加，或者减少某个关键字符
:syntax enable|clear  :打开|关闭语法支持

:colorschemo blue  moning  night  设置主题


```

### 折叠

这个作者的vim系列是高级的用法， 要学习一下。

https://blog.easwy.com/archives/advanced-vim-skills-advanced-move-method/

---

#### 一、简介

vim自带代码折叠功能，会使得我们开发时更简单。在vim中折叠设置:set fdm=xxx（fdm<>foldmethod缩写），可在.vimrc中定义实现永久有效，有manual，indent，marker，diff，syntax，expr等5种模式，此处介绍前三种。

manual：手工定义折叠

indent：按缩进折叠

marker：用标记/*{{{*/ /*}}}*/来定义折叠

diff：比较模式，对没有更改的文本进行折叠

syntax：用语法高亮来定义折叠

expr：用表达式进行折叠

#### 二、使用

1、manual模式：set fdm=manual

说明：此模式下的折叠功能只能依靠人工创建折叠范围区，在此基础上对折叠区进行开启、关闭、删除和移动等操作。

zf：创建折叠区

vj/vk/vG/vgg选中区域后执行zf

zfnj：从当前行开始向下到n行折叠

zfnk：从当前行开始向上到n行折叠

zfgg：从当前行到第一行折叠

zfG：从当前行到最后一行折叠

zfngg：从当前行到第n行折叠

zfap：按段落折叠

**zfa(：折叠括号包围的区域（如：()、[]、{}、><等）**

开启

za：开启/关闭当前折叠区，任何时候有效

zi：开启/关闭所有级折叠区，仅对对自己开启的折叠区有效

zv/zo：打开当前折叠区

zO：打开当前所有级折叠区

zr：打开同一级折叠区

zR：递归打开所有折叠区

关闭

zm：关闭同一级折叠区

zM：关闭所有级折叠区

zc：关闭当前折叠区

zC：关闭选取范围内所有级折叠区

zn：禁用折叠

zN：启用折叠

删除

zd：删除当前折叠区

zD：删除当前所有级折叠区

zE：删除窗口内所有折叠区

移动

zj：向下一个折叠点移动

zk：向上一个折叠点移动

[z：移动到打开后的折叠区的开始处

]z：移动到打开后的折叠区的结束处

注意

vim不会自动记忆手工折叠点需要如下命令进行保存/读取

:mkview 进行保存

:loadview 进行读取

2、indent模式：set fdm=indent

说明：此模式下的折叠功能依据缩进自动进行，zf在此模式中无效，在此基础上对折叠区进行开启、关闭和移动等操作与手动模式的一致。

:set foldlevel=1 #指定级别折叠缩进

:set foldlevelstart=99 #避免启动编辑器代码自动折叠

3、marker模式：set fdm=marker

说明：此模式默认按{{{ }}}标志作为缩进依据，zf会自动生成该标志，在此基础上对折叠区进行开启、关闭、删除和移动等操作与手动模式的一致。

:set foldlevelstart=99 #避免启动编辑器代码自动折叠

### show

#### tab

* 文件中有 TAB 键的时候，你是看不见的。要把它显示出来：

```sql
:set list  
```

> 现在 TAB 键显示为 ^I，而 $显示在每行的结尾，以便你能找到可能会被你忽略的空白

* 方法1中这样做的一个缺点是在有很多 TAB 的时候看起来很丑。如果你使用一个有颜色的

```
:set listchars=tab:>-,trail:-
```

> 现在，TAB会被显示成 ">---" 而行尾多余的空白字符显示成 "-"。

* 设定tab的位置

```
:set tabstop=4
```

* tab自动转空格

```
:set expandtab
```

> 如果此时需要输入真正的tab，则输入Ctrl+V, tab，在windows下是Ctrl+Q, tab

* 将已存在的tab都转化为空格 (重新设置table)

```
:retab
```
