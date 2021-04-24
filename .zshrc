# Lines configured by zsh-newuser-install
autoload -U colors && colors	# Load colors
HISTFILE=~/.histfile
HISTSIZE=1000
SAVEHIST=1000
bindkey -e
# End of lines configured by zsh-newuser-install
# The following lines were added by compinstall
zstyle :compinstall filename '/home/igg/.zshrc'

autoload -Uz compinit
compinit
# End of lines added by compinstall
PS1="%B%{$fg[red]%}[%{$fg[red]%}%n%{$fg[yellow]%}@%{$fg[yellow]%}%M %{$fg[yellow]%}%~%{$fg[yellow]%}]$%{$reset_color%}%b "
