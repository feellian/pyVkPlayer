import PyQt4
import shelve
from time import sleep
import thread

from mainwindow import Ui_MainWindow
import api
import player
import about
import login
import search
import config
import songText

class Communicate(PyQt4.QtCore.QObject):
    updateTime = PyQt4.QtCore.pyqtSignal()


class mainWindow(PyQt4.QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(mainWindow, self).__init__()
        self.setupUi(self)
        self.apiId = "3629495"
        self.userId = False
        self.token = False
        self.expires = 0

        self.player = player.Player()
        self.player.redrawPlayList = self.redraw
        self.player.setStatusBar = self.statusBarMessage
        self.player.setSliderRange = self.setSliderRange
        self.setWindowIcon(PyQt4.QtGui.QIcon('windowIcon.jpg'))

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
        self.connect(self.downloadPushButton,  PyQt4.QtCore.SIGNAL("clicked()"), self.addAudioIntoOwnList)
        self.connect(self.playPushButton, PyQt4.QtCore.SIGNAL("clicked()"), self.player.play)
        self.connect(self.pausePushButton, PyQt4.QtCore.SIGNAL("clicked()"), self.player.pause)
        self.connect(self.stopPushButton, PyQt4.QtCore.SIGNAL("clicked()"), self.player.stop)
        self.connect(self.nextPushButton, PyQt4.QtCore.SIGNAL("clicked()"), self.player.next)
        self.connect(self.prevPushButton, PyQt4.QtCore.SIGNAL("clicked()"), self.player.prev)
        self.connect(self.playlistTableWidget, PyQt4.QtCore.SIGNAL("cellDoubleClicked(int, int)"), self.player.play)
        self.connect(self.playlistTableWidget, PyQt4.QtCore.SIGNAL("cellClicked(int, int)"), self.setPosition)
        self.playlistTableWidget.keyPressEvent = self.playlistTableWidgetKey
        self.playlistTableWidget.setSelectionBehavior(PyQt4.QtGui.QAbstractItemView.SelectRows);

        self.playlistTableWidget.setColumnWidth(0, 225)
        self.playlistTableWidget.setColumnWidth(1, 225)
        self.playlistTableWidget.setColumnWidth(2, 80)
        self.playlistTableWidget.horizontalHeader().setResizeMode(0, PyQt4.QtGui.QHeaderView.Stretch)
        self.playlist = []
        self.playlistTableWidget.setColumnCount(3)

        self.highlighted = -1
        self.userId, self.token, self.playlist, self.expires = config.loadSession()

        if not self.expires:
            self.addPushButton.setEnabled(False)
            self.actionAddSongs.setEnabled(False)

        if self.playlist:
            self.updatePlaylist()
        if self.userId == None and self.token == None:
            self.addPushButton.setEnabled(False)
            self.actionAddSongs.setEnabled(False)

        self.vk = api.Api()
        self.message = ''

        self.c = Communicate()
        self.c.updateTime.connect(self.updateTime)

        thread.start_new_thread(self.handl, (1,))

    def handl(self, delay):
        while True:
            self.c.updateTime.emit()
            sleep(delay)

    def setSliderPos(self, pos):
        self.progressSlider.setSliderPosition(pos)

    def setSliderRange(self):
        maxRange = self.playlist[self.player.position]['duration']
        self.progressSlider.setRange(0, maxRange)

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
        for i in range(len(self.playlist)):
            self.playlistTableWidget.removeRow(i)
        self.playlist = []
        self.playlist.extend(s['playlist'])
        self.updatePlaylist()
        s.close()


    def updatePlaylist(self):
        oldCount = self.playlistTableWidget.rowCount()
        self.playlistTableWidget.setRowCount(len(self.playlist))

        for songInfo in self.playlist:
            artist = PyQt4.QtGui.QTableWidgetItem(songInfo['artist'].replace('&amp;', "&"))
            title = PyQt4.QtGui.QTableWidgetItem(songInfo['title'].replace('&amp;', "&"))
            duration = PyQt4.QtGui.QTableWidgetItem(self.convertDuration(songInfo['duration']))

            self.playlistTableWidget.setItem(oldCount, 0, artist)
            self.playlistTableWidget.setItem(oldCount, 1, title)
            self.playlistTableWidget.setItem(oldCount, 2, duration)
            oldCount += 1
            self.player.add(songInfo['url'])

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
        lyricsId = self.playlist[self.player.position]['lyrics_id']
        resp = self.vk.method(method, uid=self.userId, access_token=self.token, lyrics_id=lyricsId)
        self.tD = songText.songTextDialog(self)
        self.tD.show()
        self.tD.setText(resp)

    def addAudioIntoOwnList(self):
        method = 'audio.add'
        aid = str(self.playlist[self.player.position]['aid'])
        oid = str(self.playlist[self.player.position]['owner_id'])
        resp = self.vk.method(method, uid=self.userId, access_token=self.token, aid=aid, oid=oid)

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
        self.about = about.aboutDialog()
        self.about.show()

    def openSearchDialog(self):
        self.sD = search.searchDialog(self)
        self.sD.show()

    def closeApp(self):
        config.saveSession(userId=self.userId, token=self.token, playlist=self.playlist, expires=self.expires)
        exit()
