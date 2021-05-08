#!/bin/sh

rm -rf $HOME/.config/dunst
ln -s $PWD/dunst $HOME/.config/dunst

rm -rf $HOME/.config/qtile
ln -s $PWD/qtile $HOME/.config/qtile

rm -rf $HOME/.config/alacritty
ln -s $PWD/alacritty $HOME/.config/alacritty
