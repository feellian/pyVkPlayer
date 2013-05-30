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

import shelve
import os
import time

fileNames = {u'config_dir': u'.pvp',
             u'session': u'session.db'}


def configDirCheck():
    configDirPath = os.environ[u'HOME'] + '/' + fileNames[u'config_dir']
    if os.access(configDirPath, os.F_OK):
        return True
    else:
        os.mkdir(configDirPath)
        return False


def configFileCheck(configFilePath, mode):
    if not configDirCheck():
        return False
    if os.access(configFilePath, mode):
        return True
    else:
        return False


def checkSession(expires):
    if not expires or expires - time.time() < 0:
            return 0
    else:
        return expires


def loadSession():
    sessionPath = os.environ[u'HOME'] + '/' + fileNames[
        u'config_dir'] + '/' + fileNames[u'session']
    if configFileCheck(sessionPath, os.R_OK):
        s = shelve.open(sessionPath, 'r')

        userId = s.get("userId", False)
        token = s.get('token', False)
        playlist = s.get('playlist', [])
        expires = checkSession(s.get('expires', 0))

        s.close()
        return userId, token, playlist, expires
    else:
        return False, False, [], False


def saveSession(**kwarg):
    configDirCheck()
    sessionPath = os.environ[u'HOME'] + '/' + fileNames[
        u'config_dir'] + '/' + fileNames[u'session']
    s = shelve.open(sessionPath, 'n')
    for i in kwarg:
        s[i] = kwarg[i]
    s.close()
