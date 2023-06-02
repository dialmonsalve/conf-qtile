# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import os
import subprocess

from libqtile import hook
from libqtile import bar, layout, widget
from libqtile.config import Match, Screen, Key, Group
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

from qtile_extras import widget
from qtile_extras.widget.decorations import PowerLineDecoration

#! Custom classes
from custom.shortcuts import keys, mod
from custom.utils  import CustomColor, CustomFont, CustomOthers
from custom.widgets import CustomTemperature, CustomNet, CustomClock, CustomColumns

terminal = guess_terminal()

#! Clases para la barra
custom_temp = CustomTemperature()
custom_net = CustomNet()
custom_clock = CustomClock()
custom_columns = CustomColumns()

groups = [Group(i) for i in "12345678"]

for i in groups:
    keys.extend(
        [
            # mod1 + letter of group = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            # mod1 + shift + letter of group = switch to & move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc="Switch to & move focused window to group {}".format(i.name),
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod1 + shift + letter of group = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )

layouts = [
    layout.Columns(border_focus_stack=["#d75f5f", "#8f3d3d"], border_width=4),
    layout.Max(),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    # layout.MonadTall(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font=CustomFont.font_family,
    fontsize=CustomFont.font_size,
    padding=3,
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.GroupBox(
                    active=CustomColor.orange,
                    background=CustomColor.dark_gray,
                    border_width=CustomOthers.border_width,
                    disable_drag = True,
                    fontsize=CustomFont.font_size + 8,
                    foreground=CustomColor.purple,
                    highlight_method = "block",
                    inactive=CustomColor.lighter_blue,
                    margin_x=0,
                    margin_y=2,
                    other_current_screen_border = CustomColor.gray,
                    other_screen_border = CustomColor.gray,
                    this_current_screen_border = CustomColor.light,
                    this_screen_border = CustomColor.light,
                    urgent_alert_method = "block",
                    urgent_border = CustomColor.urgent,
                ),
                widget.Prompt(),
                widget.WindowName(
                    foreground=CustomColor.light,
                    background=CustomColor.dark_gray
                ),
                widget.Systray(
                    icon_size = CustomFont.font_size + 2,
                    background=CustomColor.dark_gray,
                    decorations = [
                        PowerLineDecoration(path="arrow_right")
                    ]

                ),
                #! Grupo temperatura
                custom_temp.create_icono(""),
                custom_temp.thermal_sensor(tag_sensor="Core 0",fmt='T1:{}'),
                custom_temp.thermal_sensor(tag_sensor="Core 1",fmt='T2:{}'),
                custom_temp.memory(),

                #! Grupo red
                custom_net.create_icono("󰁪"),
                custom_net.check_updates(),
                custom_net.create_icono("󰓅"),
                custom_net.widget_net(),

                #! Grupo reloj
                custom_clock.clock(),
                custom_clock.create_icono(""),
                custom_clock.volume(),
                
                custom_columns.current_layout_icon(),
                custom_columns.current_layout()
            ],
            32,
        )
    )
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"

@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser('~')
    subprocess.Popen([home + '/.config/qtile/custom/autostart.sh'])