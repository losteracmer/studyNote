技巧之重复
当我们用vim编辑文本的时候，不免会进行一些重复的操作，当我们想要重复上次的操作，难道还要重复一遍相同的操作么？这样不免会浪费时间。于是vim就将你上次进行的一些操作记录在vim的寄存器里，当你想要重复上次进行的操作的时候，直接点击快捷键就可以了。

技巧之重复
当我们用vim编辑文本的时候，不免会进行一些重复的操作，当我们想要重复上次的操作，难道还要重复一遍相同的操作么？这样不免会浪费时间。于是vim就将你上次进行的一些操作记录在vim的寄存器里，当你想要重复上次进行的操作的时候，直接点击快捷键就可以了。

Vim重复的类型
vim中有五种基本的重复类型，分别是：


|   重复类型   | 重复操作符 | 回退操作符 |
| :----------: | :--------: | :--------: |
| 文本改变重复 |     .     |     u     |
| 行内查找重复 |     ;     |     ,     |
| 全文查找重复 |     n     |     N     |
| 文本替换重复 |     &     |     u     |
|    宏重复    | @[寄存器] |     u     |


下面我们来见详细介绍这几种重复操作

文本改变重复
通过 : h .来查看vim的帮助手册：

. Repeat last change, with count replaced with [count]. Also repeat a yank command, when the ‘y’ flag is included in ‘cpoptions’. Does not repeat a command-line command.

可见.操作就是用来重复上一次更改的

举几个栗子:

example1:
用x操作来删除一个字符，接着用.重复删除字符

example2:
用dd删除一行数据，然后用.重复删除一行数据

example3:
用yy复制一行数据，p进行粘贴，点击.来重复粘贴操作

行内查找重复
有时候我们想要在当前行内查找一个字符，我们可以通过f{char}/t{char}来从当前位置开始到行尾进行查找，也可以通过F{char}/T{char}从当前位置开始到行首进行查找。简单的说就是小写向后找，大写向前找。

通过 : h ；来查看vim的帮助手册：

; Repeat latest f, t, F or T [count] times. See cpo-;

, Repeat latest f, t, F or T in opposite direction [count] times. See also cpo-;

可见我们可以用;来重复vim查找的操作，,重复反向找的操作

举几个栗子:

example1:
在文件main.cc的31行里面首先用f：来查找:字符，之后用;来重复查找操作

example2:
我们将前文讲到的更改操作重复和行内查找操作重复结合在一起，在文件main.cc的31行里面首先用f+：来查找:字符，然后cl将:字符替换为+字符，之后重复的键入;.来将剩下的:替换为+

全文查找重复
通过:h /来查看vim的帮助手册:

/{pattern}[/]`<CR>` Search forward for the [count]’th occurrence of {pattern} exclusive.
?{pattern}[?]`<CR>` Search backward for the [count]’th previous occurrence of {pattern} exclusive.
在vim里面通过/pattern`<CR>`来从当前位置开始在全文中向下查找匹配项，或者?pattern`<CR>`来从当前位置开始在全文中向上查找匹配项

通过:h n来查看vim的帮助手册:

n Repeat the latest “/” or “?” [count] times. last-pattern {Vi: no count}
N Repeat the latest “/” or “?” [count] times in opposite direction. last-pattern {Vi: no count}
在查找完毕以后，我们可以用n跳转到下一个匹配项，N跳转到上一个匹配项

举个栗子:
在main.cc里面查找suite，并用gUaw将单转为大写，之后重复n.操作将全部转为大写文本重复替换
通过:h &来查看vim的帮助手册:

```
& Synonym for :s (repeat last substitute). Note that the flags are not remembered, thus it might actually work differently. You can use :&& to keep the flags.
```

一般来说，我们可以采用这样的形式:s/target/replacement/g来将行内出现的字符串target替换为另外一个字符串replacement,要是我们想在其他行执行相同的替换工作，可以用&来重复替换操作

举个栗子:
将main.cc文件31行内的::字符串采用下面的形式替换为+-+:s/::/+-+/g,之后用重复j&操作替换下面的两行

宏录制重复
通过:h @来查看vim的帮助手册:

@{0-9a-z".=*+} Execute the contents of register {0-9a-z”.=*+} [count] times. Note that register ‘%’ (name of the current file) and ‘#’ (name of the alternate file) cannot be used.

vim里面宏录制是一个非常NB的功能，你可以录制一系列的操作到寄存器里面，之后直接@{寄存器}就可以重复之前录制的一系列操作

vim里面可以用q{寄存器}开始进行录制，之后用q来结束录制,寄存器的名字a-z中的任意一个，比如qa就是将操作录制到寄存器a中，之后如果想要使用该宏，使用@a就可以重复录制的操作

举几个栗子:

example1:将当前行的::替换为+-+，然后删除行尾的；号，并将文本向右缩进一行

example2:在内容为this is number1进行复制，然后粘贴到下一行，并将数字1增加为2,内容变为this is number2,以此重复十次，所以最后一行的内容应为this is number12

这里用到了vim里面的一个冷知识，那就是Ctrl+a,该操作会从光标开始，向后查找离光标最近的数字，如果找到就将数字的值加1，同理Ctrl+x就是将数字减1，于是我们录制了这样的一个宏操作qa,yy,p,ctrl+a,q,然后10@a将这个宏重复十次就成了上面的效果啦
————————————————
版权声明：本文为CSDN博主「qeesung」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/ii1245712564/article/details/4649634

Vim重复的类型
vim中有五种基本的重复类型，分别是：

重复类型	重复操作符	回退操作符
文本改变重复	.	u
行内查找重复	;	,
全文查找重复	n	N
文本替换重复	&	u
宏重复	@[寄存器]	u
下面我们来见详细介绍这几种重复操作

文本改变重复
通过 : h .来查看vim的帮助手册：

. Repeat last change, with count replaced with [count]. Also repeat a yank command, when the ‘y’ flag is included in ‘cpoptions’. Does not repeat a command-line command.

可见.操作就是用来重复上一次更改的

举几个栗子:

example1:
用x操作来删除一个字符，接着用.重复删除字符

example2:
用dd删除一行数据，然后用.重复删除一行数据

example3:
用yy复制一行数据，p进行粘贴，点击.来重复粘贴操作

行内查找重复
有时候我们想要在当前行内查找一个字符，我们可以通过f{char}/t{char}来从当前位置开始到行尾进行查找，也可以通过F{char}/T{char}从当前位置开始到行首进行查找。简单的说就是小写向后找，大写向前找。

通过 : h ；来查看vim的帮助手册：

; Repeat latest f, t, F or T [count] times. See cpo-;

, Repeat latest f, t, F or T in opposite direction [count] times. See also cpo-;

可见我们可以用;来重复vim查找的操作，,重复反向找的操作

举几个栗子:

example1:
在文件main.cc的31行里面首先用f：来查找:字符，之后用;来重复查找操作

example2:
我们将前文讲到的更改操作重复和行内查找操作重复结合在一起，在文件main.cc的31行里面首先用f+：来查找:字符，然后cl将:字符替换为+字符，之后重复的键入;.来将剩下的:替换为+

全文查找重复
通过:h /来查看vim的帮助手册:

/{pattern}[/]`<CR>` Search forward for the [count]’th occurrence of {pattern} exclusive.
?{pattern}[?]`<CR>` Search backward for the [count]’th previous occurrence of {pattern} exclusive.
在vim里面通过/pattern`<CR>`来从当前位置开始在全文中向下查找匹配项，或者?pattern`<CR>`来从当前位置开始在全文中向上查找匹配项

通过:h n来查看vim的帮助手册:

n Repeat the latest “/” or “?” [count] times. last-pattern {Vi: no count}
N Repeat the latest “/” or “?” [count] times in opposite direction. last-pattern {Vi: no count}
在查找完毕以后，我们可以用n跳转到下一个匹配项，N跳转到上一个匹配项

举个栗子:
在main.cc里面查找suite，并用gUaw将单词转为大写，之后重复n.操作将全部转为大写

文本重复替换
通过:h &来查看vim的帮助手册:

& Synonym for :s (repeat last substitute). Note that the flags are not remembered, thus it might actually work differently. You can use :&& to keep the flags.

一般来说，我们可以采用这样的形式:s/target/replacement/g来将行内出现的字符串target替换为另外一个字符串replacement,要是我们想在其他行执行相同的替换工作，可以用&来重复替换操作

举个栗子:
将main.cc文件31行内的::字符串采用下面的形式替换为+-+:s/::/+-+/g,之后用重复j&操作替换下面的两行

宏录制重复
通过:h @来查看vim的帮助手册:

@{0-9a-z".=*+} Execute the contents of register {0-9a-z”.=*+} [count] times. Note that register ‘%’ (name of the current file) and ‘#’ (name of the alternate file) cannot be used.

vim里面宏录制是一个非常NB的功能，你可以录制一系列的操作到寄存器里面，之后直接@{寄存器}就可以重复之前录制的一系列操作

vim里面可以用q{寄存器}开始进行录制，之后用q来结束录制,寄存器的名字a-z中的任意一个，比如qa就是将操作录制到寄存器a中，之后如果想要使用该宏，使用@a就可以重复录制的操作

举几个栗子:

example1:将当前行的::替换为+-+，然后删除行尾的；号，并将文本向右缩进一行

example2:在内容为this is number1进行复制，然后粘贴到下一行，并将数字1增加为2,内容变为this is number2,以此重复十次，所以最后一行的内容应为this is number12

这里用到了vim里面的一个冷知识，那就是Ctrl+a,该操作会从光标开始，向后查找离光标最近的数字，如果找到就将数字的值加1，同理Ctrl+x就是将数字减1，于是我们录制了这样的一个宏操作qa,yy,p,ctrl+a,q,然后10@a将这个宏重复十次就成了上面的效果啦

原文链接：https://blog.csdn.net/ii1245712564/article/details/46496347
