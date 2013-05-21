#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       Copyright (C) 2013  Alexey Ulyanov
#
#       This file is part of vkontakte audio player.
#       vkontakte audio player is free software: you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation, either version 3 of the License, or
#       (at your option) any later version.
#
#       vkontakte audio player is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#
#       You should have received a copy of the GNU General Public License
#       along with vkontakte audio player.  If not, see <http://www.gnu.org/licenses/>.
#

import time
from urllib import unquote

# import PyQt4
from PyQt4 import QtGui, QtCore, uic, QtWebKit
from PyQt4.QtGui import QDialog
from PyQt4.QtCore import QUrl

from loginDialog import Ui_LoginDialog

class LoginExc(Exception):
    def __init__(self, error_msg):
        self.error_msg = error_msg
    def __str__(self):
        return repr(self.error_msg)

class loginDialog(QtGui.QDialog, Ui_LoginDialog):
    def __init__(self, parent=None):
        super(loginDialog, self).__init__(parent)
        self.parent = parent
        self.setupUi(self)
        self.setWindowTitle('Login')
        self.webView = QtWebKit.QWebView(self)
        self.webView.setGeometry(6, 6, 800, 400)
        self.webView.setObjectName("webView")
        self.webView.connect(self.webView, QtCore.SIGNAL("urlChanged(const QUrl&)"), self.evurlChanged)
        self.webView.load(QUrl("""https://oauth.vk.com/authorize?client_id=3629495&scope=8&
            redirect_uri=http://oauth.vk.com/blank.html&display=popup&response_type=token"""))

    def closeLoginDialog(self):
        self.close()

    def evurlChanged(self):
        path = str(self.webView.url().path())
        if path == '/blank.html':
            self.webView.url().path()
            self.returnSession(unquote(unicode(self.webView.url().toString())).split('='))
        elif path == '/api/login_failure.html':
            raise LoginExc('Login failure')

    def returnSession(self, session):
        session = "&".join(session).split('&')
        session = {session[i]:session[i + 1] for i in range(0, len(session), 2)}

        self.parent.expires = time.time() + int(session["expires_in"])
        self.parent.userId = session[u"user_id"]
        self.parent.token = session[u"https://oauth.vk.com/blank.html#access_token"]

        self.parent.addPushButton.setEnabled(True)
        self.parent.actionAddSongs.setEnabled(True)
        self.closeLoginDialog()
