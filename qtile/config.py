# A customized config.py for Qtile window manager (http://www.qtile.org)
# Modified by Derek Taylor (http://www.gitlab.com/dwt1/ )
#
# The following comments are the copyright and licensing information from the default
# qtile config. Copyright (c) 2010 Aldo Cortesi, 2010, 2014 dequis, 2012 Randall Ma,
# 2012-2014 Tycho Andersen, 2012 Craig Barnes, 2013 horsik, 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this
# software and associated documentation files (the "Software"), to deal in the Software
# without restriction, including without limitation the rights to use, copy, modify,
# merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be included in all copies
# or substantial portions of the Software.

##### IMPORTS #####

import os
import re
import socket
import subprocess
import configparser
from libqtile.extension import Dmenu, RunCommand
from libqtile.config import Key, Screen, Group, Drag, Click
from libqtile.command import lazy
from libqtile import layout, bar, widget, hook
from libqtile.widget import Spacer
from libqtile.extension import Dmenu

#### DEFINING SOME WINDOW FUNCTIONS #####


config_file_path = './config.conf'
configuration = configparser.RawConfigParser()
configuration.read(config_file_path)


@lazy.function
def window_to_prev_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i - 1].name)


@lazy.function
def window_to_next_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i + 1].name)

##### LAUNCH APPS IN SPECIFIED GROUPS #####

def app_or_group(group, app):
    def f(qtile):
        if qtile.groupMap[group].windows:
            qtile.groupMap[group].cmd_toscreen()
        else:
            qtile.groupMap[group].cmd_toscreen()
            qtile.cmd_spawn(app)
    return f

# KEYBINDINGS\

def init_keys():
    keys = [
        Key([mod], "Return",       lazy.spawn(myTerm)), # open terminal
        Key([mod], "t",            lazy.spawn("notify-send asd")), # open terminal
        Key([mod], "Tab",          lazy.next_layout()), # next layouy
        Key([mod], "q",            lazy.window.kill()), # kill window
        Key([mod, "shift"], "r",   lazy.restart()),     # restart qtile
        Key([mod, "shift"], "q",   lazy.shutdown()),    # quit qtile

        ### Window controls
        Key([mod], "j",            lazy.layout.down()), # Go to window down
        Key([mod], "k",            lazy.layout.up()),   # Go to window up
        Key([mod, "shift"], "j",   lazy.layout.shuffle_down()), # Switch windows
        Key([mod, "shift"], "k",   lazy.layout.shuffle_up()),   # Switch windows
        Key([mod, "shift"], "l",   lazy.layout.grow(),
                                         # increase size of window (XmonadTall)
                                   lazy.layout.increase_nmaster()),
                                         # Increase number in master pane (Tile)
        Key([mod, "shift"], "h",   lazy.layout.shrink(),
                                         # Shrink size of window (XmonadTall)
                                   lazy.layout.decrease_nmaster()),
                                         # Decrease number in master pane (Tile)

        Key([mod], "z",
            lazy.to_screen(0)                       # Keyboard focus to screen(0)
            ),
        Key([mod], "x",
            lazy.to_screen(1)                       # Keyboard focus to screen(1)
            ),
        Key(
            [mod], "n",
            lazy.layout.normalize()                 # Restore all windows to default size ratios
            ),
        Key(
            [mod], "m",
            lazy.layout.maximize()                  # Toggle a window between minimum and maximum sizes
            ),
        Key(
            [mod], "f",
            lazy.window.toggle_floating()           # Toggle floating
            ),
        Key(
            [mod, "shift"], "space",
            lazy.layout.rotate(),                   # Swap panes of split stack (Stack)
            lazy.layout.flip()                      # Switch which side main pane occupies (XmonadTall)
            ),
        ### Stack controls
        Key(
            [mod], "space",
            lazy.layout.next()                      # Switch window focus to other pane(s) of stack
            ),
        Key(
            [mod, "control"], "Return",
            lazy.layout.toggle_split()              # Toggle between split and unsplit sides of stack
            ),

        ### Dmenu Run Launcher
        Key(
            [mod, "shift"], "Return",
            lazy.spawn("dmenu_run -fn 'Ubuntu Mono Nerd Font:size=10' -nb {0} -nf '#ffffff' -sb {1} -sf '#ffffff' -p 'dmenu:'".format(colors[0][0], colors[5][0]))
            ),
        # Key([mod, "control"], "o", lazy.spawn("librewolf")),
        # Key([mod, "control"], "i", lazy.spawn("midori")),
        Key([mod, "control"], "p", lazy.spawn("firefox")),
        Key([mod, "control"], "k", lazy.spawn("atom")),
        Key([mod, "control"], "b", lazy.spawn("alacritty -e pulsemixer")),
        Key([mod, "control"], "z", lazy.spawncmd()), # open terminal
        Key([mod, "control"], "l", lazy.spawn("nautilus")),
        Key([mod, "control"], "m",
            lazy.spawn("kwrite /home/igg/git/wiki_me/wiki_me.md")),
        Key([mod, "control"], "n",
            lazy.spawn("kwrite /home/igg/git/wiki_me/to_do.md")),
        Key(
            [mod, "mod1"], "e",
            lazy.spawn(myTerm+" -e neomutt")
            ),
        Key(
            [mod, "mod1"], "m",
            lazy.spawn(myTerm+" -e sh ./scripts/toot.sh")
            ),
        Key(
            [mod, "mod1"], "t",
            lazy.spawn(myTerm+" -e sh ./scripts/tig-script.sh")
            ),
        Key(
            [mod, "mod1"], "f",
            lazy.spawn(myTerm+" -e sh ./.config/vifm/scripts/vifmrun")
            ),
        Key(
            [mod, "mod1"], "j",
            lazy.spawn(myTerm+" -e joplin")
            ),
        Key(
            [mod, "mod1"], "c",
            lazy.spawn(myTerm+" -e cmus")
            ),
        Key(
            [mod, "mod1"], "i",
            lazy.spawn(myTerm+" -e irssi")
            ),
        Key(
            [mod, "mod1"], "y",
            lazy.spawn(myTerm+" -e htop")
            ),
        Key(
                [mod, "mod1"], "a",
                lazy.spawn(myTerm+" -e ncpamixer")
            ),
        Key(
            [], "XF86AudioLowerVolume",
            lazy.spawn(" /home/igg/git/configs/custom_scripts/vol_down")
           ),
        Key(
            [], "XF86AudioRaiseVolume",
            lazy.spawn("/home/igg/git/configs/custom_scripts/vol_up")
           ),
        Key(
            [], "XF86AudioMute",
            lazy.spawn("/home/igg/git/configs/custom_scripts/vol_mute"),
           ),
        Key(
           [], "XF86AudioMicMute",
           lazy.spawn("pactl set-source-mute @DEFAULT_SOURCE@ toggle"),
          ),
        Key(
	   [], "XF86MonBrightnessUp",
	   lazy.spawn("light -A 15")
           ),
        Key(
           [], "XF86MonBrightnessDown",
           lazy.spawn("light -U 15")
            )
    ]
    return keys

##### BAR COLORS #####

def init_colors():
    return [["#282a36", "#282a36"], # panel background
            ["#434758", "#434758"], # background for current screen tab
            ["#ffffff", "#ffffff"], # font color for group names
            ["#ff5555", "#ff5555"], # background color for layout widget
            ["#000000", "#000000"], # background for other screen tabs
            ["#0c6e13", "#0c6e13"], # dark green gradiant for other screen tabs
            ["#50fa7b", "#50fa7b"], # background color for network widget
            ["#7197E7", "#7197E7"], # background color for pacman widget
            ["#9AEDFE", "#9AEDFE"], # background color for cmus widget
            ["#000000", "#000000"], # background color for clock widget
            ["#434758", "#434758"]] # background color for systray widget

##### GROUPS #####

def init_group_names():
    return [("I", {'layout': 'monadtall'}),
            ("II", {'layout': 'monadtall'}),
            ("III", {'layout': 'monadtall'}),
            ("IV", {'layout': 'monadtall'}),
            ("V",{'layout': 'monadtall'}),
            ("VI",{'layout': 'monadtall'}),
            ("VII", {'layout': 'monadtall'}),
            ("VIII", {'layout': 'monadtall'}),
            ("IX", {'layout': 'floating'})]

def init_groups():
    return [Group(name, **kwargs) for name, kwargs in group_names]


##### LAYOUTS #####

def init_floating_layout():
    return layout.Floating(border_focus="#9AEDFE")

def init_layout_theme():
    return {"border_width": 3,
            "margin": 10,
            "border_focus": colors[5][0][1:],
            "border_normal": "1D2330"
           }

def init_border_args():
    return {"border_width": 2}

def init_layouts():
    return [
            # layout.Bsp(**layout_theme),
            # layout.Stack(stacks=2, **layout_theme),
            # layout.Columns(**layout_theme),
            # layout.VerticalTile(**layout_theme),
            # layout.Tile(shift_windows=True, **layout_theme),
            # layout.Zoomy(**layout_theme),
            layout.MonadTall(**layout_theme),
            layout.RatioTile(**layout_theme),
            # layout.Matrix(**layout_theme),
            layout.MonadWide(**layout_theme),
            layout.Max(**layout_theme),
            # layout.TreeTab(
            #     font = "Ubuntu",
            #     fontsize = 10,
            #     sections = ["FIRST", "SECOND"],
            #     section_fontsize = 11,
            #     bg_color = "141414",
            #     active_bg = "90C435",
            #     active_fg = "000000",
            #     inactive_bg = "384323",
            #     inactive_fg = "a0a0a0",
            #     padding_y = 10,
            #     section_padding = 10,
            #     section_top = 10,
            #     panel_width = 320,
            #     **layout_theme
            #     ),
            layout.Floating(**layout_theme)]

##### WIDGETS #####

def init_widgets_defaults():
    return dict(font="Ubuntu Mono",
                fontsize = 15,
                padding = 2,
                background=colors[0])

def init_widgets_list():
    prompt = "{0}@{1}: ".format(os.environ["USER"], socket.gethostname())
    widgets_list = [
               widget.Sep(
                        linewidth = 0,
                        padding = 6,
                        foreground = colors[2][0],
                        background = colors[0][0]
                        ),
               widget.GroupBox(font="Ubuntu Mono Bold",
                        fontsize = 10,
                        margin_y = 2,
                        margin_x = 0,
                        padding_y = 5,
                        padding_x = 5,
                        borderwidth = 3,
                        active = colors[2],
                        inactive = colors[2],
                        rounded = False,
                        highlight_method = "block",
                        this_current_screen_border = colors[5],
                        this_screen_border = colors [1],
                        other_current_screen_border = colors[0],
                        other_screen_border = colors[0],
                        foreground = colors[2],
                        background = colors[0],
                        disable_drag = True,
                        hide_unused = False,
                        ),
                widget.CurrentLayoutIcon(
                        foreground = colors[2],
                        background = colors[0],
                        padding = 10
                        ),
               widget.Prompt(
                        prompt=prompt,
                        font="Ubuntu Mono",
                        padding=10,
                        foreground = colors[3],
                        background = colors[1]
                        ),
               widget.WindowName(font="Ubuntu Mono",
                        fontsize = 17,
                        foreground = colors[5],
                        background = colors[0],
                        padding = 3
                        ),
               widget.Battery(
                        foreground=colors[2],
                        background=colors[0],
                        font="Ubuntu Mono",
                        padding = 0,
                        # fontsize=15,
                        discharge_char = "" ,
                        charge_char="^",
                        format= " [ Bat:{percent: 1.0%}{char} ] ",
                        show_short_text = False,
                        notify_below = 20,
                        unknown_char = '',
                        update_interval = 5
                        ),
               widget.Clock(
                        foreground = colors[2],
                        background = colors[0],
                        format="[%A, %B %d ] [ %H:%M ]",
                        # fontsize = 15,
                        ),

                widget.Systray(
                         background=colors[0],
                         padding = 5
                         ),
              ]
    return widgets_list

##### SCREENS ##### (TRIPLE MONITOR SETUP)

def init_widgets_screen1():
    widgets_screen1 = init_widgets_list()
    return widgets_screen1                       # Slicing removes unwanted widgets on Monitors 1,3

def init_widgets_screen2():
    widgets_screen2 = init_widgets_list()
    return widgets_screen2                       # Monitor 2 will display all widgets in widgets_list

def init_screens():
    return [Screen(top=bar.Bar(widgets=init_widgets_screen1(), opacity=0.95, size=20)),
            Screen(top=bar.Bar(widgets=init_widgets_screen2(), opacity=0.95, size=20)),
            Screen(top=bar.Bar(widgets=init_widgets_screen1(), opacity=0.95, size=20))]

##### FLOATING WINDOWS #####

@hook.subscribe.client_new
def floating(window):
    floating_types = ['notification', 'toolbar', 'splash', 'dialog']
    transient = window.window.get_wm_transient_for()
    if window.window.get_wm_type() in floating_types or transient:
        window.floating = True

@hook.subscribe.client_new
def inkscape_dialogues(window):
   floating_programs = ['to_do.md', "wiki_me.md ", 'pulsemixer', "wiki_me.md  \342\200\224 KWrite"]
   if(window.window.get_name() in floating_programs) or "wiki_me" in window.window.get_name() or "to_do.md" in  window.window.get_name():
        window.floating = True

def init_mouse():
    return [Drag([mod], "Button1", lazy.window.set_position_floating(),      # Move floating windows
                 start=lazy.window.get_position()),
            Drag([mod], "Button3", lazy.window.set_size_floating(),          # Resize floating windows
                 start=lazy.window.get_size()),
            Click([mod, "shift"], "Button1", lazy.window.bring_to_front())]  # Bring floating window to front

##### DEFINING A FEW THINGS #####



if __name__ in ["config", "__main__"]:
    mod = "mod4"                                     # Sets mod key to SUPER/WINDOWS
    myTerm = "alacritty"                                    # My terminal of choice
    myConfig = "/home/igg/.config/qtile/config.py"   # Qtile config file location

    colors = init_colors()
    keys = init_keys()
    mouse = init_mouse()
    group_names = init_group_names()
    groups = init_groups()
    floating_layout = init_floating_layout()
    layout_theme = init_layout_theme()
    border_args = init_border_args()
    layouts = init_layouts()
    screens = init_screens()
    widget_defaults = init_widgets_defaults()
    widgets_list = init_widgets_list()
    widgets_screen1 = init_widgets_screen1()
    widgets_screen2 = init_widgets_screen2()

##### SETS GROUPS KEYBINDINGS #####

for i, (name, kwargs) in enumerate(group_names, 1):
    keys.append(Key([mod], str(i), lazy.group[name].toscreen()))          # Switch to another group
    keys.append(Key([mod, "shift"], str(i), lazy.window.togroup(name)))   # Send current window to another group

##### STARTUP APPLICATIONS #####

@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser('~')
    # subprocess.call([home + '/.config/qtile/autostart.sh'])



##### NEEDED FOR SOME JAVA APPS #####

#wmname = "LG3D"
wmname = "qtile"
