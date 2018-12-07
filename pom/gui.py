# Copyright: Anders Dalskov, 2018
# See LICENSE

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib
import threading

from .util import format_time

def prettify_time(t):
    return f"<span font_size='xx-large'><b>{format_time(t)}</b></span>"

class _PomGUI(Gtk.Window):

    def __init__(self, obj):
        self.obj = obj
        Gtk.Window.__init__(self, title='Pomodoro!')

        # this shows the remaining time
        self.counter = Gtk.Label()
        self.update_time()

        # quit button
        self.quit_btn = Gtk.Button(label='quit')
        self.quit_btn.connect('clicked', self.bail)

        # pause button
        self.pause_btn = Gtk.Button(label='pause')
        self.pause_btn.connect('clicked', self.pause)

        GLib.timeout_add(1000, self.update_time)

        # construct layout
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.set_border_width(10)
        self.add(vbox)
        vbox.pack_start(self.counter, True, True, 0)
        hbox = Gtk.Box(spacing=6)
        vbox.pack_start(hbox, True, True, 0)
        hbox.pack_start(self.pause_btn, True, True, 0)
        hbox.pack_start(self.quit_btn, True, True, 0)
        self.set_default_size(200, 100)

    def update_time(self):
        t = self.obj['remainingtime']
        self.counter.set_markup(prettify_time(t))
        return True

    def bail(self, widget):
        self.obj['bail'] = True
        Gtk.main_quit()

    def pause(self, widget):
        if self.obj['paused']:
            self.obj['paused'] = False
            label = self.pause_btn.get_child()
            label.set_text('pause')
            print('unpaused')
        else:
            self.obj['paused'] = True
            label = self.pause_btn.get_child()
            label.set_text('resume')
            print('paused')


class PomGUI():
    def __init__(self, obj):
        t = threading.Thread(target=self.start, args=(obj,), daemon=True)
        t.start()

    def start(self, obj):
        win = _PomGUI(obj)
        win.connect('destroy', Gtk.main_quit)
        win.show_all()
        Gtk.main()
