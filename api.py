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

import simplejson as json

import urllib2
import urllib
from urllib import urlencode
from urlparse import urlparse
import api_exception

class Api(object):
    def __init__(self, api_id):
        self.api_id = unicode(api_id)

    def searchAudio(self, **kwargs):
        url = "https://api.vk.com/method/%s?q=%s&uid=%s&access_token=%s&count=200" % (kwargs["method"], kwargs["q"], kwargs["user_id"], kwargs["token"])
        # print (urllib2.urlopen(url).read())
        return json.loads(urllib2.urlopen(url).read())["response"]

    def getAudio(self, **kwargs):
        url = "https://api.vk.com/method/%s?uid=%s&access_token=%s" % (kwargs["method"], kwargs["user_id"], kwargs["token"])
        return json.loads(urllib2.urlopen(url).read())["response"]

    def getLyrics(self, **kwargs):
        url = "https://api.vk.com/method/%s?uid=%s&access_token=%s&lyrics_id=%s" % (kwargs["method"], kwargs["user_id"], kwargs["token"], kwargs["lyrics_id"])
        return json.loads(urllib2.urlopen(url).read())["response"]
