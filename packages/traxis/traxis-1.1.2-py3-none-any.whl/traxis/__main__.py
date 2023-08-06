# Copyright (C) 2014 Syed Haider Abidi, Nooruddin Ahmed and Christopher Dydula
#
# This file is part of traxis.
#
# traxis is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# traxis is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with traxis.  If not, see <http://www.gnu.org/licenses/>.

import os
import sys
import ctypes
from PyQt5 import QtWidgets
from traxis.gui import mainwindow


def main():
    # if running on Windows, create an application user model id for this app
    # so that a custom taskbar icon can be used
    if hasattr(ctypes, 'windll'):
        appId = 'traxis'
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(appId)

    # store the path of this file at the start of sys.path so that all files under
    # the root traxis directory can be easily accessed
    basePath = os.path.dirname(os.path.realpath(__file__))
    sys.path.insert(0, basePath)

    # create a QApplication object for managing the GUI control flow and settings
    app = QtWidgets.QApplication(sys.argv)

    # create an instance of TraxisApplicationWindow and display it on the screen
    window = mainwindow.TraxisApplicationWindow()
    window.show()

    # begin the app's event handling loop; ensure a clean exit
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
