
from urllib import unquote

import PyQt4
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

class searchDialog(PyQt4.QtGui.QDialog, Ui_SearchDialog):
    def __init__(self, parent=None):
        super(searchDialog, self).__init__(parent)
        self.parent = parent
        self.resp = '';
        self.setupUi(self)
        self.connect(self.searchPushButton, PyQt4.QtCore.SIGNAL("clicked()"), self.audioSearch)
        self.connect(self.getOwnListButton, PyQt4.QtCore.SIGNAL("clicked()"), self.audioGet)
        self.connect(self.addPushButton,  PyQt4.QtCore.SIGNAL("clicked()"), self.addToPlayList)
        self.connect(self.backPushButton,  PyQt4.QtCore.SIGNAL("clicked()"), self.closeLoginDialog)
        self.searchTableWidget.horizontalHeader().setResizeMode(PyQt4.QtGui.QHeaderView.Stretch)
        self.searchTableWidget.setColumnCount(3)
        self.searchTableWidget.setSelectionBehavior(PyQt4.QtGui.QAbstractItemView.SelectRows);

    def closeLoginDialog(self):
        self.close()

    def audioGet(self):
        method = 'audio.get'
        self.resp = self.parent.vk.method(method, uid=self.parent.userId, access_token=self.parent.token)
        self.handleResponse()

    def audioSearch(self):
        query =str(self.searchLineEdit.text().toUtf8())
        query = query.replace(' ', '%20')
        method = 'audio.search'
        count = '200'
        self.resp = self.parent.vk.method(method, uid=self.parent.userId, access_token=self.parent.token, q=query, count=count)
        self.handleResponse()

    def handleResponse(self):
        self.searchTableWidget.setRowCount(len(self.resp)-1)
        i = 0
        for songInfo in self.resp[1:]:
            artist   = PyQt4.QtGui.QTableWidgetItem(songInfo['artist'])
            title    = PyQt4.QtGui.QTableWidgetItem(songInfo['title'])
            duration = PyQt4.QtGui.QTableWidgetItem(self.parent.convertDuration(songInfo['duration']))

            self.searchTableWidget.setItem(i, 0, artist)
            self.searchTableWidget.setItem(i, 1, title)
            self.searchTableWidget.setItem(i, 2, duration)
            i += 1
        return

    def addToPlayList(self):
            indexes = self.searchSelected()
            if len(indexes) == 0:
                return
            if self.parent.playlist is None:
                self.parent.playlist = []
            for i in indexes:
                self.parent.playlist.append(self.resp[i+1])
                self.parent.player.add(self.resp[i+1][u'url'])

            selected = self.searchTableWidget.selectedIndexes()

            count = len(selected)/3
            oldCount = self.parent.playlistTableWidget.rowCount()
            self.parent.playlistTableWidget.setRowCount(self.parent.playlistTableWidget.rowCount()+count)
            for i in range(len(selected)/3):
                artist = PyQt4.QtGui.QTableWidgetItem(selected[i].data(0).toString())
                title = PyQt4.QtGui.QTableWidgetItem(selected[i+count].data(0).toString())
                duration = PyQt4.QtGui.QTableWidgetItem(selected[i+2*count].data(0).toString())

                self.parent.playlistTableWidget.setItem(oldCount+i, 0, PyQt4.QtGui.QTableWidgetItem(artist))
                self.parent.playlistTableWidget.setItem(oldCount+i, 1, PyQt4.QtGui.QTableWidgetItem(title))
                self.parent.playlistTableWidget.setItem(oldCount+i, 2, PyQt4.QtGui.QTableWidgetItem(duration))

            self.closeLoginDialog()

    def searchSelected(self):
        indexes = []
        for selectionRange in self.searchTableWidget.selectedRanges():
            indexes.extend(range(selectionRange.topRow(), selectionRange.bottomRow() + 1))
        return indexes
