# How to add nautilus "Open in Terminator" option

"Nautilus" or "Files" is the default file explorer in Ubuntu 20.04. It comes with a feature to open the current directory in a command line. For this it always used the default gnome terminal. Because I'm using terminator, I wanted nautilus to open the shell in terminator instead of the default gnome shell.

As of writing this (nautilus version 3.36.1.1-stable) there is no settings option to change the default terminal.

### Install Nautilus Python

With [Nautilus Python](https://wiki.gnome.org/Projects/NautilusPython) you can add extensions to nautilus. We will create a new extension to add an "open in terminator" option to the right-click menu.

Install Nautilus Python with:

```
$ sudo apt install python-nautilus
```

### Create new extension

Nautilus Python looks at those three directories for extensions:

1. $XDG*DATA*HOME/nautilus-python/extensions (i.e. \~/.local/share/...)
2. nautilus*prefix/share/nautilus-python/extensions (i.e. \~/Development/...)*
3. *$XDG*DATA_DIRS/nautilus-python/extensions (i.e. /usr/share/...)

We will put our extension into the first directory, which you have to create first:

```
$ mkdir -p ~/.local/share/nautilus-python/extensions
```

Now create a file into the newly created directory:

```
$ vim ~/.local/share/nautilus-python/extensions/open-terminator.py
```

And paste the following code into it:

```
import os

from gi.repository import Nautilus, GObject

class ColumnExtension(GObject.GObject, Nautilus.MenuProvider):
    def __init__(self):
        pass
    def menu_activate_cb(self, menu, file):
        os.system("/usr/bin/terminator --working-directory=" + file.get_location().get_path())

    def get_background_items(self, window, file):
        item = Nautilus.MenuItem(name='NautilusOpenTerminator',
                                         label='Open in Terminator',
                                         tip='',
                                         icon='')
        item.connect('activate', self.menu_activate_cb, file)
        return item,
```

### Enable extension

To enable the extension you need to restart nautilus. You can quit nautilus with:

```
$ nautilus  -q
```