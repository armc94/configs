# Lines configured by zsh-newuser-install
HISTFILE=~/.histfile
HISTSIZE=1000
SAVEHIST=1000
export XDG_CONFIG_HOME=/home/igg/.config

bindkey -e
# End of lines configured by zsh-newuser-install
# The following lines were added by compinstall
zstyle :compinstall filename '/home/igg/.zshrc'

autoload -Uz compinit
compinit
# End of lines added by compinstall
#
export PATH=$PATH:/home/igg/.local/bin
export PYTHONTRACEMALLOC=1
autoload -U colors && colors	# Load colors
PS1="%B%{$fg[red]%}[%{$fg[red]%}%n%{$fg[red]%}@%{$fg[yellow]%}%M %{$fg[yellow]%}%~%{$fg[yellow]%}]% $%b%{$reset_color%} "
source /usr/share/zsh/plugins/zsh-syntax-highlighting/zsh-syntax-highlighting.plugin.zsh
alias ls='ls --color=auto'

alias erpn='cd /home/igg/git/frappe_docker/; sudo docker-compose --project-name erpn up -d; atom ../imports'

export hesh2="D0:8A:55:25:34:E3"
