#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# This program is Licenced under GPL, see http://www.gnu.org/copyleft/gpl.html
# Author: Felix Hummel <felix@felixhummel.de>

import dbus
import glob
import os
import sys
try:
    import pynotify
except:
    pass

NOTIFICATION_TIMEOUT_IN_MS = 3000

# notify ubuntu style, fall back to printing
def notify(msg):
    print(msg)
if pynotify.init("vimshell"):
    def notify(msg):
        n = pynotify.Notification("vimshell", msg)
        n.set_timeout(NOTIFICATION_TIMEOUT_IN_MS)
        assert n.show(), "Failed to send notification"

def get_bus():
    try:
        bus = dbus.SessionBus()
    except:
        notify("Could not connect to dbus.")
        sys.exit(1)
    return bus

def _get_dbus_object(bus, servicename, path, interface):
    obj = bus.get_object(servicename, path)
    return dbus.Interface(obj, dbus_interface=interface)

def get_yakuake(bus):
    try:
        sessions = _get_dbus_object(bus, 'org.kde.yakuake', '/yakuake/sessions', 'org.kde.yakuake')
        mainwindow = dbus.Interface(bus.get_object('org.kde.yakuake', '/yakuake/MainWindow_1'),
                  dbus_interface='org.freedesktop.MediaPlayer')
    except:
        notify("Could not connect to Yakuake.")
        sys.exit(1)
    return sessions, mainwindow

def open_file_in_new_shell(sessions, mainwindow, filename):
    sessions.addSession()
    sessions.runCommand('vim %s'%filename)

def get_filename():
    try:
        return sys.argv[1]
    except IndexError:
        notify("expected FILENAME")
        sys.exit(1)

if __name__ == '__main__':
    #filename = get_filename()
    filename = '/tmp/x'
    bus = get_bus()
    sessions, mainwindow = get_yakuake(bus)
    open_file_in_new_shell(sessions, mainwindow, filename)
