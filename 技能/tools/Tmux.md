# Tmux


## Tmux概念


使用 Tmux 的时候不用去背指令，所有的指令都可以在 `.tmux.conf` 配置文件中绑定自己顺手的快捷键，也可以配置开启鼠标。

在Tmux逻辑中，需要分清楚Server > Session > Window > Pane这个大小和层级顺序是极其重要的，直接关系到工作效率：

* Server：是整个tmux的后台服务。有时候更改配置不生效，就要使用tmux kill-server来重启tmux。
* Session：是tmux的所有会话。我之前就错把这个session当成窗口用，造成了很多不便里。一般只要保存一个session就足够了。
* Window：相当于一个工作区，包含很多分屏，可以针对每种任务分一个Window。如下载一个Window，编程一个window。
* Pane：是在Window里面的小分屏。最常用也最好用


## 快捷键

所有的快捷键之前都要加一个tmux的前置快捷键（默认 ctrl - b）

### 基本操作

| **?** | 列出所有快捷键；按**q**返回                                                 |
| ----------- | --------------------------------------------------------------------------------- |
| d           | 脱离当前会话,可暂时返回Shell界面，输入tmux attach能够重新进入之前会话             |
| s           | 选择并切换会话；在同时开启了多个会话时使用                                        |
| D           | 选择要脱离的会话；在同时开启了多个会话时使用                                      |
| :           | 进入命令行模式；此时可输入支持的命令，例如kill­server所有tmux会话                |
| [           | 复制模式，光标移动到复制内容位置，空格键开始，方向键选择复制，回车确认，q/Esc退出 |
| ]           | 进入粘贴模式，粘贴之前复制的内容，按q/Esc退出                                     |
| ~           | 列出提示信息缓存；其中包含了之前tmux返回的各种提示信息                            |
| t           | 显示当前的时间                                                                    |
| Ctrl+z      | 挂起当前会话                                                                      |

### 窗口操作

| **c** | 创建新窗口                               |
| ----------- | ---------------------------------------- |
| &           | 关闭当前窗口                             |
| 数字键      | 切换到指定窗口                           |
| p           | 切换至上一窗口                           |
| n           | 切换至下一窗口                           |
| l           | 前后窗口间互相切换                       |
| w           | 通过窗口列表切换窗口                     |
| ,           | 重命名当前窗口，便于识别                 |
| .           | 修改当前窗口编号，相当于重新排序         |
| f           | 在所有窗口中查找关键词，便于窗口多了切换 |

### 面板操作

| **“** | 将当前面板上下分屏                                     |
| ------------ | ------------------------------------------------------ |
| %            | 将当前面板左右分屏                                     |
| x            | 关闭当前分屏                                           |
| !            | 将当前面板置于新窗口,即新建一个窗口,其中仅包含当前面板 |
| Ctrl+方向键  | 以1个单元格为单位移动边缘以调整当前面板大小            |
| Alt+方向键   | 以5个单元格为单位移动边缘以调整当前面板大小            |
| 空格键       | 可以在默认面板布局中切换，试试就知道了                 |
| q            | 显示面板编号                                           |
| o            | 选择当前窗口中下一个面板                               |
| 方向键       | 移动光标选择对应面板                                   |
| {            | 向前置换当前面板                                       |
| }            | 向后置换当前面板                                       |
| Alt+o        | 逆时针旋转当前窗口的面板                               |
| Ctrl+o       | 顺时针旋转当前窗口的面板                               |
| z            | tmux 1.8新特性，最大化当前所在面板                     |
| t            | 在当前面板显示时间                                     |
