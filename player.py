import pygst
import gst
import gobject
import random
import sys


class Player(object):
    def __init__(self):
        self.playbin = gst.element_factory_make("playbin", "player")
        fakesink = gst.element_factory_make("fakesink", "fakesink")
        self.playbin.set_property("video-sink", fakesink)
        bus = self.playbin.get_bus()
        bus.add_signal_watch()
        bus.connect("message", self.onMessage)

        self.playlist = []
        self.state = "stop"
        self.mode = "simple"
        self.single = False
        self.position = -1
        self.selected = -1
        self.duration = "00:00:00"

    def onMessage(self, bus, message):
        t = message.type
        if t == gst.MESSAGE_EOS:
            self.playbin.set_state(gst.STATE_NULL)
            self.next()
        elif t == gst.MESSAGE_ERROR:
            self.playbin.set_state(gst.STATE_NULL)
            err, debug = message.parse_error()
            sys.stderr.write("Error: " + str(err) + str(debug))

    def delete(self, pos):
        pos.sort()
        if self.position in pos:
            self.stop()
            self.position = -1
        else:
            shift = 0
            for p in pos:
                if self.position > p:
                    shift = shift + 1
            self.position = self.position - shift
        pos.reverse()
        [self.playlist.pop(i) for i in pos]



    """

    """
    def redrawPlayList(self):
        pass

    """
    Add a track into the player's play list.
    """
    def add(self, link):
        self.playlist.append(link)

    """
    Defined in gui.py
    """
    def setStatusBar(self):
        pass

    """
    Defined in gui.py
    """
    def setSliderRange(self):
        pass

    """
    Seeks the position of current track in sec.
    """
    def setTrackPosition(self, seek):
        self.playbin.seek_simple(gst.FORMAT_TIME, gst.SEEK_FLAG_FLUSH, seek * 1000000000)

    """
    Returns current position of an audio track in sec.
    """
    def timePos(self):
        try:
            timePos = self.playbin.query_position(gst.FORMAT_TIME, None)
            if timePos:
                return str(self.playbin.query_position(gst.FORMAT_TIME, None)[0] // 1000000000)
            else:
                return "0"
        except gst.QueryError:
                return "0"


    """
    Defined in gui.py
    """
    def changeStatusBar(self):
        pass

    def checkStates(self):
        if len(self.playlist) == 0:
            return False
        if self.position == -1 and self.state == "stop":
            return False
        return True

    """
    Plays an audio track from the play list.
    If we call this function as event handler we
    assign selected row as current position.
    """
    def play(self, pos=-1):
        if pos != -1:
            self.position = self.selected

        if self.checkStates():
            if self.position == -1:
                self.chooseFirst()
            if self.state == "play":
                self.stop()
            self.playbin.set_property("uri", self.playlist[self.position])
            self.playbin.set_state(gst.STATE_PLAYING)
            self.state = "play"
            self.redrawPlayList()
            self.setSliderRange()
            self.setStatusBar()


    """
    Set the current song on pause and remember current position.
    """
    def pause(self):
        if self.state == "play":
            self.playbin.set_state(gst.STATE_PAUSED)
            self.state = "pause"

    """
    Stops the player
    """
    def stop(self):
        if self.state != "stop":
            self.playbin.set_state(gst.STATE_NULL)
            self.state = "stop"
        self.redrawPlayList()

    """
    Starts to play the next song from the play list
    """
    def next(self):
        if self.checkStates():
            self.chooseNext()
            if self.position != -1:
                self.playbin.set_state(gst.STATE_READY)
                self.play()
            else:
                self.stop()

    """
    Plays next song from the play list.
    """
    def prev(self):
        if self.checkStates():
            self.choosePrev()
            if self.position != -1:
                self.playbin.set_state(gst.STATE_READY)
                self.play()
            else:
                self.stop()

    """
    Plays previous song from the play list.
    """
    def chooseFirst(self):
        if self.mode == "random":
            self.position = random.randint(0, len(self.playlist)-1)
        else:
            self.position = 0


    def chooseNext(self):
        if self.checkStates():
            if self.single:
                return
            if self.position == -1:
                self.chooseFirst()
                return
            if self.mode == "simple":
                if self.position == len(self.playlist) - 1:
                    self.position = -1
                else:
                    self.position += 1
            elif self.mode == "random" :
                self.position = random.randint(0, len(self.playlist)-1)
            elif self.mode == "repeat":
                if self.position == len(self.playlist) - 1:
                    self.chooseFirst()


    def choosePrev(self):
        if self.checkStates():
            if self.single:
                return
            if self.position == -1:
                self.chooseFirst()
                return
            if self.mode == "simple":
                if self.position == 0:
                    self.position = -1
                else:
                    self.position -= 1
            elif self.mode == "random" :
                self.position = random.randint(0, len(self.playlist)-1)
            elif self.mode == "repeat":
                if self.position == 0:
                    self.position = len(self.playlist) - 1
                else:
                    self.position += 1

gobject.threads_init()

