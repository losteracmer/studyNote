```
show git bolb type :
git cat-file -p/-t [fileName]

```

## git commit 标准

commit 格式

```
<type>(<scope>): <subject>
<BLANK LINE>
<body>
<BLANK LINE>
<footer>
```

#### type

```git
# 主要type
feat:     增加新功能
fix:      修复bug

# 特殊type
docs:     只改动了文档相关的内容
style:    不影响代码含义的改动，例如去掉空格、改变缩进、增删分号
build:    构造工具的或者外部依赖的改动，例如webpack，npm
refactor: 代码重构时使用
revert:   执行git revert打印的message

# 暂不使用type
test:     添加测试或者修改现有测试
perf:     提高性能的改动
ci:       与CI（持续集成服务）有关的改动
chore:    不修改src或者test的其余修改，例如构建过程或辅助工具的变动

```

## 常用命令

#### 远端覆盖本地

```
git reset --hard origin/master
```

#### 合并某个commit到当前分支

> 只合并某一次提交，而并非将此分支都合过来

```shell
git cherry-pick <commit_id>
```

#### 将某个分支的文件覆盖到当前分支

```
git checkout branch --  <file_name>
```

#### 修改分支名称

```git
git branch -m oldName newName
```

如果已经推到远端，先删除后，重新推送

```git
git branch --unset-upstream # 解除关联远程分支
git push --delete origin oldName
git push origin newName
git branch --set-upstream-to origin/newName # 把修改后的本地分支与远程分支关联
```
