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

from urllib import unquote
import json
import locale

import PyQt4
from PyQt4 import QtGui, QtCore, uic, QtWebKit
from PyQt4.QtGui import QDialog
from PyQt4.QtCore import QUrl
from PyQt4.QtGui import QMessageBox

from searchDialog import Ui_SearchDialog

import api_exception

class SearchExc(Exception):
    def __init__(self, error_msg):
        self.error_msg = error_msg
    def __str__(self):
        return repr(self.error_msg)

class searchDialog(QtGui.QDialog, Ui_SearchDialog):
    def __init__(self, parent=None):
        super(searchDialog, self).__init__(parent)
        self.parent = parent
        self.setupUi(self)
        self.connect(self.searchPushButton, PyQt4.QtCore.SIGNAL("clicked()"), self.searchAudio)
        self.connect(self.getOwnListButton, PyQt4.QtCore.SIGNAL("clicked()"), self.getAudio)
        self.connect(self.addPushButton,  PyQt4.QtCore.SIGNAL("clicked()"), self.addToPlayList)
        self.connect(self.backPushButton,  PyQt4.QtCore.SIGNAL("clicked()"), self.closeLoginDialog)
        self.searchTableWidget.keyPressEvent = self.searchTableWidgetKey
        self.searchTableWidget.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
        self.searchTableWidget.setColumnCount(3)
        self.searchTableWidget.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows);




    def searchTableWidgetKey(self, event):
        if event.key() == PyQt4.QtCore.Qt.Key_Delete:
            self.delete(self.playlist_selected())
        elif event.key() == PyQt4.QtCore.Qt.Key_Enter or event.key() == PyQt4.QtCore.Qt.Key_Return:
            self.play(self.searchTableWidget.selectedRanges()[0].topRow())
        PyQt4.QtGui.QTableWidget.keyPressEvent(self.searchTableWidget, event)

    def playlist_selected(self):
        indexes = []
        for selectionRange in self.playlistTableWidget.selectedRanges():
            indexes.extend(range(selectionRange.topRow(), selectionRange.bottomRow()+1))
        return indexes


    def closeLoginDialog(self):
        self.close()

    def getAudio(self):
        try:
            method = 'audio.get'
            self.resp = self.parent.vk.getAudio(method=method, user_id=self.parent.user_id, token=self.parent.token)
        except api_exception.MethodErr, e:
            msg = PyQt4.QtGui.QMessageBox(self)
            msg.setText(e.error_msg+'\n'+str(e.request_params))
            msg.setWindowTitle('Api Error')
            msg.exec_()
            return
        self.handleResponse(self.resp)


    def searchAudio(self):
        # query = str("Выс")
        # print query
        # decoded_str = query.decode("windows-1252")
        # encoded_str = decoded_str.encode("utf8")

        # enc = locale.getpreferredencoding()
        # print enc
        query=self.searchLineEdit.text()
        # query=("Высоцкий").decode(enc)
        # print query
        try:
            method = 'audio.search'
            self.resp = self.parent.vk.searchAudio(method=method, user_id=self.parent.user_id, token=self.parent.token, q=query)
        except api_exception.MethodErr, e:
            msg = PyQt4.QtGui.QMessageBox(self)
            msg.setText(e.error_msg+'\n'+str(e.request_params))
            msg.setWindowTitle('Api Error')
            msg.exec_()
            return
        self.handleResponse(self.resp)


    def handleResponse(self, res):
        self.searchTableWidget.setRowCount(len(self.resp)-1)
        i = 0
        for song_info in self.resp[1:]:
            artist   = PyQt4.QtGui.QTableWidgetItem(song_info['artist'])
            title    = PyQt4.QtGui.QTableWidgetItem(song_info['title'])
            duration = PyQt4.QtGui.QTableWidgetItem(self.parent.convertDuration(song_info['duration']))

            self.searchTableWidget.setItem(i, 0, artist)
            self.searchTableWidget.setItem(i, 1, title)
            self.searchTableWidget.setItem(i, 2, duration)
            i += 1
        return

    def addToPlayList(self):
            indexes = self.search_selected()
            if len(indexes) == 0:
                return
            if self.parent.playlist is None:
                self.parent.playlist = []
            for i in indexes:
                self.parent.playlist.append(self.resp[i+1])
                self.parent.player.add(self.resp[i+1][u'url'])

            selected = self.searchTableWidget.selectedIndexes()

            count = len(selected)/3
            old_count = self.parent.playlistTableWidget.rowCount()
            self.parent.playlistTableWidget.setRowCount(self.parent.playlistTableWidget.rowCount()+count)
            for i in range(len(selected)/3):
                artist = PyQt4.QtGui.QTableWidgetItem(selected[i].data(0).toString())
                title = PyQt4.QtGui.QTableWidgetItem(selected[i+count].data(0).toString())
                duration = PyQt4.QtGui.QTableWidgetItem(selected[i+2*count].data(0).toString())

                self.parent.playlistTableWidget.setItem(old_count+i, 0, PyQt4.QtGui.QTableWidgetItem(artist))
                self.parent.playlistTableWidget.setItem(old_count+i, 1, PyQt4.QtGui.QTableWidgetItem(title))
                self.parent.playlistTableWidget.setItem(old_count+i, 2, PyQt4.QtGui.QTableWidgetItem(duration))

            self.closeLoginDialog()

    def search_selected(self):
        indexes = []
        for selectionRange in self.searchTableWidget.selectedRanges():
            indexes.extend(range(selectionRange.topRow(), selectionRange.bottomRow()+1))
        return indexes
