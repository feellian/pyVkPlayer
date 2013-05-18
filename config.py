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

file_names = {u'config_dir': u'.pvp',
u'session': u'session.db'}

def config_dir_check():
	config_dir_path = os.environ[u'HOME']+'/'+file_names[u'config_dir']
	if os.access(config_dir_path, os.F_OK):
		return True
	else:
		os.mkdir(config_dir_path)
		return False

def config_file_check(config_file_path, mode):
	if not config_dir_check():
		return False
	if os.access(config_file_path, mode):
		return True
	else:
		return False
def checkSession(expires):
	if not expires or expires - time.time() < 0:
	   		return False



def load_session():
	session_path = os.environ[u'HOME']+'/'+file_names[u'config_dir']+'/'+file_names[u'session']
	if config_file_check(session_path, os.R_OK):

		s = shelve.open(session_path, 'r')
		if "user_id" and 'token' and 'playlist' and 'expires' in s:
			user_id = s['user_id']
			token = s['token']
			playlist = s['playlist']
			expires = checkSession(s['expires'])
		else:
			s.close()
			return False, False, [], False
		s.close()
		return user_id, token, playlist, expires
	else:
		return False, False, [], False

def save_session(**kwarg):
	config_dir_check()
	session_path = os.environ[u'HOME']+'/'+file_names[u'config_dir']+'/'+file_names[u'session']
	s = shelve.open(session_path, 'n')
	for i in kwarg:
		s[i] = kwarg[i]
	s.close()

