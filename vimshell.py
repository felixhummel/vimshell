#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# This program is Licenced under GPL, see http://www.gnu.org/copyleft/gpl.html
# Author: Felix Hummel <felix@felixhummel.de>

import dbus
import os.path
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

class Yakuake(object):
    def __init__(self):
        try:
            self.bus = dbus.SessionBus()
        except:
            notify("Could not connect to dbus.")
        try:
            self.sessions = self._get_interface('org.kde.yakuake', '/yakuake/sessions', 'org.kde.yakuake')
            self.mainwindow = self._get_interface('org.kde.yakuake', '/yakuake/MainWindow_1', 'org.freedesktop.MediaPlayer')
        except:
            notify("Could not connect to Yakuake.")

    def _get_interface(self, servicename, path, interface):
        obj = self.bus.get_object(servicename, path)
        return dbus.Interface(obj, dbus_interface=interface)

    def open_file(self, filename, lineno=1):
        self.sessions.addSession()
        self.sessions.runCommand('vim -c ":%s" %s'%(lineno, filename))

def get_args():
    x = len(sys.argv)
    if x == 1:
        notify("expected FILENAME")
        sys.exit(1)
    elif x == 2:
        return (sys.argv[1], None)
    else:
        return (sys.argv[1], sys.argv[2])

if __name__ == '__main__':
    filename, lineno = get_args()
    ya = Yakuake()
    ya.open_file(filename, lineno)
