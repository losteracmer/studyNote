# Oh My Zsh + powerlevel10k

## install zsh

```shell
apt install vim curl git
apt install zsh
# 更换默认shell，need relogin
chsh -s $(which zsh)
```

## install oh my zsh
[github](https://github.com/ohmyzsh/ohmyzsh)
```shell
wget https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh
sh install.sh
```

## p10k
[github](https://github.com/romkatv/powerlevel10k)
```shell
git clone --depth=1 https://github.com/romkatv/powerlevel10k.git ${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/themes/powerlevel10k
```

修改.zshrc中的主题
```conf
ZSH_THEME="powerlevel10k/powerlevel10k"
```

```shell
# 应用配置，并进入p10k configure
source ~/.zshrc
```

## plugin

[zsh-completions](https://github.com/zsh-users/zsh-completions)

[zsh-autosuggestions](https://github.com/zsh-users/zsh-autosuggestions)

[zsh-syntax-highlighting](https://github.com/zsh-users/zsh-syntax-highlighting)


修改.zshrc中的插件
```conf
plugins=(
git
zsh-completions 
zsh-autosuggestions 
zsh-syntax-highlighting
)
```

```shell
# 应用配置，并进入p10k configure
source ~/.zshrc
```

## 其它好用的特性


### 将指令输入行固定在最底部
```conf
# Fix prompt at the bottom of the terminal window
printf '\n%.0s' {1..100}
```
> 有挺多bug，比如clear

