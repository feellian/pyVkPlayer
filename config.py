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
