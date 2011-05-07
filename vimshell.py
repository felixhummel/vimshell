#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# This program is licenced under the GPL, see http://www.gnu.org/copyleft/gpl.html
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

class Bus(object):
    def __init__(self):
        try:
            self.bus = dbus.SessionBus()
        except:
            notify("Could not connect to dbus.")

    def _get_interface(self, servicename, path, interface):
        obj = self.bus.get_object(servicename, path)
        return dbus.Interface(obj, dbus_interface=interface)

class Yakuake(Bus):
    def __init__(self):
        Bus.__init__(self)
        try:
            self.sessions = self._get_interface('org.kde.yakuake', '/yakuake/sessions', 'org.kde.yakuake')
            self.tabs = self._get_interface('org.kde.yakuake', '/yakuake/tabs', 'org.kde.yakuake')
            self.mainwindow = self._get_interface('org.kde.yakuake', '/yakuake/MainWindow_1', 'org.freedesktop.MediaPlayer')
        except:
            notify("Could not connect to Yakuake.")
            import traceback
            traceback.print_exc()

    def open_file(self, filename, lineno=None):
        self.sessions.addSession()
        cmd = 'vim %s'%(filename)
        if lineno:
            cmd = 'vim +%s %s'%(lineno, filename)
        self.sessions.runCommand(cmd)
        session_id = self.sessions.activeSessionId()
        self.tabs.setTabTitle(session_id, 'vimshell')

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
