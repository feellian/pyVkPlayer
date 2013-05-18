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

import PyQt4
from PyQt4 import QtGui, QtCore
import shelve
import random
from time import sleep
import thread

from mainwindow import Ui_MainWindow
import api
import api_exception
import player
import about
import login
import search
import config
import songText

class Communicate(QtCore.QObject):
    updateTime = QtCore.pyqtSignal()


class mainWindow(PyQt4.QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(mainWindow, self).__init__()
        self.setupUi(self)
        self.API_ID = "3629495"
        self.user_id = False
        self.token = False
        self.expires = False
        self.player = player.Player()
        self.player.redrawPlayList = self.redraw
        self.player.setStatusBar = self.statusBarMessage
        self.player.setSliderRange = self.setSliderRange


        self.actionRandom.setShortcut('Ctrl+Shift+R')
        self.actionQuite.setShortcut('Ctrl+Q')
        self.actionLogin.setShortcut('Ctrl+L')
        self.actionSavePlaylist.setShortcut('Ctrl+S')
        self.actionOpenPlaylist.setShortcut('Ctrl+O')
        self.addPushButton.setShortcut('Ctrl+AltA')
        self.playPushButton.setShortcut('Ctrl+X')
        self.pausePushButton.setShortcut('Ctrl+C')
        self.stopPushButton.setShortcut('Ctrl+V')
        self.nextPushButton.setShortcut('Ctrl+B')
        self.prevPushButton.setShortcut('Ctrl+Z')

        self.actionLogin.triggered.connect(self.openLoginDialog)
        self.actionAbout.triggered.connect(self.openAboutDialog)
        self.actionPlay.triggered.connect(self.player.play)
        self.actionStop.triggered.connect(self.player.stop)
        self.actionPause.triggered.connect(self.player.pause)
        self.actionViewText.triggered.connect(self.viewSongText)
        self.actionRandom.triggered.connect(self.setRandomMode)
        self.actionRandom.setCheckable(True);
        # self.actionRepeat.setShortcut('Ctrl+Shift+R')
        self.actionRepeat.triggered.connect(self.setRepeatMode)
        self.actionRepeat.setCheckable(True);
        self.actionQuite.triggered.connect(self.closeApp)
        self.actionSavePlaylist.triggered.connect(self.savePlaylist)
        self.actionOpenPlaylist.triggered.connect(self.loadPlaylist)
        self.actionAddSongs.triggered.connect(self.openSearchDialog)
        self.actionSingle.triggered.connect(self.setSingleMode)
        self.actionSingle.setCheckable(True);



        self.progressSlider.sliderMoved .connect(self.player.setTrackPosition)
        self.connect(self.progressSlider,  PyQt4.QtCore.SIGNAL("clicked()"), self.openSearchDialog)

        self.connect(self.addPushButton,  PyQt4.QtCore.SIGNAL("clicked()"), self.openSearchDialog)
        self.connect(self.playPushButton, PyQt4.QtCore.SIGNAL("clicked()"), self.player.play)
        self.connect(self.pausePushButton, PyQt4.QtCore.SIGNAL("clicked()"), self.player.pause)
        self.connect(self.stopPushButton, PyQt4.QtCore.SIGNAL("clicked()"), self.player.stop)
        self.connect(self.nextPushButton, PyQt4.QtCore.SIGNAL("clicked()"), self.player.next)
        self.connect(self.prevPushButton, PyQt4.QtCore.SIGNAL("clicked()"), self.player.prev)
        self.connect(self.playlistTableWidget, PyQt4.QtCore.SIGNAL("cellDoubleClicked(int, int)"), self.player.play)
        self.connect(self.playlistTableWidget, PyQt4.QtCore.SIGNAL("cellClicked(int, int)"), self.setPosition)
        self.playlistTableWidget.keyPressEvent = self.playlistTableWidgetKey
        # self.playlistTableWidget.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
        self.playlistTableWidget.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows);

        self.playlistTableWidget.setColumnWidth(0, 225)
        self.playlistTableWidget.setColumnWidth(1, 225)
        self.playlistTableWidget.setColumnWidth(2, 80)
        self.playlistTableWidget.horizontalHeader().setResizeMode(0, QtGui.QHeaderView.Stretch)
        self.playlist = []
        self.playlistTableWidget.setColumnCount(3)

        self.highlighted = -1
        self.user_id, self.token, self.playlist, self.expires = config.load_session()

        if not self.expires:
            self.addPushButton.setEnabled(False)
            self.actionAddSongs.setEnabled(False)

        if self.playlist:
            self.updatePlaylist()
        if self.user_id == None and self.token == None:
            self.addPushButton.setEnabled(False)
            self.actionAddSongs.setEnabled(False)

        self.vk = api.Api(self.API_ID)
        self.message = ''

        self.c = Communicate()
        self.c.updateTime.connect(self.updateTime)

        thread.start_new_thread(self.handl, (1,))

    def handl(self, delay):
        while True:
            self.c.updateTime.emit()
            sleep(1)

    def setSliderPos(self, pos):
        self.progressSlider.setSliderPosition(pos)

    def setSliderRange(self):
        max = self.playlist[self.player.position]['duration']
        self.progressSlider.setRange(0, max)

    def updateTime(self):
        timePos = int(self.player.timePos())
        self.setSliderPos(timePos)

        try:
            self.timeLabel.setText(self.convertDuration(timePos)
                + "/" + self.convertDuration(self.playlist[self.player.position]['duration']))
        except IndexError:
            self.timeLabel.setText("00:00:00/00:00:00")

    def setSingleMode(self, single):
        self.player.single = single

    def highlight(self, pos):
        if self.highlighted != -1:
            for i in range(3):
                self.playlistTableWidget.item(self.highlighted, i).setBackground(PyQt4.QtGui.QBrush(PyQt4.QtGui.QColor("white")))
        if pos != -1:
            for i in range(3):
                self.playlistTableWidget.item(pos, i).setBackground(PyQt4.QtGui.QBrush(PyQt4.QtGui.QColor("yellow")))
        self.highlighted = pos

    def playlistTableWidgetKey(self, event):
        if event.key() == PyQt4.QtCore.Qt.Key_Delete:
            self.delete(self.playlistSelected())
        elif event.key() == PyQt4.QtCore.Qt.Key_Enter or event.key() == PyQt4.QtCore.Qt.Key_Return:
            self.player.play()
        PyQt4.QtGui.QTableWidget.keyPressEvent(self.playlistTableWidget, event)

    def playlistSelected(self):
        indexes = []
        for selectionRange in self.playlistTableWidget.selectedRanges():
            indexes.extend(range(selectionRange.topRow(), selectionRange.bottomRow()+1))
        return indexes

    def delete(self, indexes):
        indexes.sort()
        indexes.reverse()
        self.player.delete(indexes)
        for i in indexes:
            self.playlist.pop(i)
            self.playlistTableWidget.removeRow(i)

    def savePlaylist(self):
        fileDialog = PyQt4.QtGui.QFileDialog()
        fileDialog.setFileMode(PyQt4.QtGui.QFileDialog.AnyFile)
        fileDialog.setAcceptMode(PyQt4.QtGui.QFileDialog.AcceptSave)
        fname = fileDialog.getSaveFileName()
        s = shelve.open(unicode(fname), 'c')
        s['playlist'] = self.playlist
        s.close()


    def loadPlaylist(self):
        fileDialog = PyQt4.QtGui.QFileDialog()
        fileDialog.setFileMode(PyQt4.QtGui.QFileDialog.AnyFile)
        fileDialog.setAcceptMode(PyQt4.QtGui.QFileDialog.AcceptOpen)
        fname = fileDialog.getOpenFileName()
        s = shelve.open(unicode(fname), 'r')
        self.playlist.extend(s['playlist'])
        self.updatePlaylist()
        s.close()

    def updatePlaylist(self):
        old_count = self.playlistTableWidget.rowCount()
        self.playlistTableWidget.setRowCount(len(self.playlist))

        for song_info in self.playlist:
            artist = PyQt4.QtGui.QTableWidgetItem(song_info['artist'])
            title = PyQt4.QtGui.QTableWidgetItem(song_info['title'])
            duration = PyQt4.QtGui.QTableWidgetItem(self.convertDuration(song_info['duration']))

            self.playlistTableWidget.setItem(old_count, 0, artist)
            self.playlistTableWidget.setItem(old_count, 1, title)
            self.playlistTableWidget.setItem(old_count, 2, duration)
            old_count += 1
            self.player.add(song_info['url'])

    def convertDuration(self, time):
        time = int(time)
        hours = time // 3600
        minutes = (time - 3600 * hours) // 60
        seconds = (time - 3600 * hours - 60 * minutes)
        return "%02d:%02d:%02d" % (hours, minutes, seconds)

    def setPosition(self, position):
        self.player.selected = position

    def viewSongText(self):
        method = 'audio.getLyrics'
        lyrics_id = self.playlist[self.player.position]['lyrics_id']

        resp = self.vk.getLyrics(method=method, user_id=self.user_id, token=self.token, lyrics_id=lyrics_id)
        self.tD = songText.songTextDialog(self)
        self.tD.show()
        self.tD.setText(resp)


    def statusBarMessage(self):
        pos = self.player.position
        message = (self.playlist[pos]['artist'] + " : " +  self.playlist[pos]['title']).replace('amp;', '')
        self.statusbar.showMessage(message)


    def redraw(self):
        if self.player.state == "stop":
            self.highlight(-1)
        else:
            self.highlight(self.player.position)

    def setRepeatMode(self, action):
        if action:
            self.player.mode = "repeat"
        else:
            self.player.mode = "simple"

    def setRandomMode(self, action):
        if action:
            self.player.mode = "random"
        else:
            self.player.mode = "simple"

    def openLoginDialog(self):
        self.lD = login.loginDialog(self)
        self.lD.show()

    def openAboutDialog(self):
        self.about = about.aboutDialog(self)
        self.about.show()

    def openSearchDialog(self):
        self.sD = search.searchDialog(self)
        self.sD.show()

    def closeApp(self):
        config.save_session(user_id=self.user_id, token=self.token, playlist=self.playlist, expires=self.expires)
        exit()
