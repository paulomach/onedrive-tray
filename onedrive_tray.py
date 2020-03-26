#!/usr/sbin/env python3

import sys
from PyQt5 import QtWidgets, QtGui
import subprocess
from time import sleep
from os import path


class SystemTrayIcon(QtWidgets.QSystemTrayIcon):

    def __init__(self, icon, parent=None):
        QtWidgets.QSystemTrayIcon.__init__(self, icon, parent)
        menu = QtWidgets.QMenu(parent)
        self.start_action = menu.addAction("Start Sync")
        self.stop_action = menu.addAction("Pause Sync")
        self.exit_action = menu.addAction("Exit")
        self.setContextMenu(menu)
        self.exit_action.triggered.connect(self.exit)
        self.start_action.triggered.connect(self.start_sync)
        self.stop_action.triggered.connect(self.stop_sync)
        self.stop_action.setEnabled(False)
        self.proc = None

    def exit(self, checker):
        self.stop_sync()
        sys.exit(0)

    def start_sync(self):
        self.proc = subprocess.Popen('onedrive --monitor', shell=True)
        self.stop_action.setEnabled(True)
        self.start_action.setEnabled(False)

    def stop_sync(self):
        if self.proc:
            self.proc.terminate()
            self.start_action.setEnabled(True)
            self.stop_action.setEnabled(False)


def main():
    app = QtWidgets.QApplication(sys.argv)
    icon = path.dirname(sys.argv[0]) + '/onedrive.png'    
    w = QtWidgets.QDialog()
    tray_icon = SystemTrayIcon(QtGui.QIcon(icon), w)

    tray_icon.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
