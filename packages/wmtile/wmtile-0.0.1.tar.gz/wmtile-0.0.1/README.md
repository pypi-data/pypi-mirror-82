usage: wmtile [-h] [-H] [-V] [-i] [-k] [-m] [-t] [-p] [-l] [-s] [-b] [-c]

window tiler for XFCE and many other desktop environments

wmtile is a CLI program, but you should use it:

- either by mouse (via wmtile -i)
- or by keyboard (via wmtile -k)
```
$ wmtile -k
installing 7 wmtile keyboard shortcuts...
    Shift+Alt+M --> wmtile -m
    Shift+Alt+T --> wmtile -t
    Shift+Alt+P --> wmtile -p
    Shift+Alt+L --> wmtile -l
    Shift+Alt+S --> wmtile -s
    Shift+Alt+B --> wmtile -b
    Shift+Alt+C --> wmtile -c
...please reboot in order to make wmtile keyboard shortcuts effective
```
for further details, type:
```
    $ wmtile -H
```
optional arguments:
```
  -h, --help            show this help message and exit
  -H, --user-guide      open User Guide in PDF format and exit
  -V, --version         show program's version number and exit
  -i, --panel-launchers
                        install 7 panel launchers (XFCE only)
  -k, --keyboard-shortcuts
                        install 7 keyboard shortcuts (XFCE only)
  -m, --minimize        Minimize all windows in current desktop
  -t, --tiles           reshape as Tiles all windows in current desktop
  -p, --portraits       reshape as Portraits all windows in current desktop
  -l, --landscapes      reshape as Landscapes all windows in current desktop
  -s, --stack           reshape as a Stack all windows in current desktop
  -b, --big             reshape as Big (maximize) all windows in current
                        desktop
  -c, --close           gracefully Close all windows in current desktop
```
