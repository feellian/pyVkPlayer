import simplejson as json
from PyQt4 import QtGui
import urllib2
import api_exception

class Api(object):
    def __init__(self):
        pass

    def method(self, method, **kwargs):
        try:
            url = "https://api.vk.com/method/"+ method
            params = ''
            for i in kwargs:
                params += "&" + i + '=' + kwargs[i].decode('utf-8')
            url = url  + '?' + params[1:]
            url = url.encode('utf-8')
            return json.loads(urllib2.urlopen(url).read())["response"]
        except api_exception.MethodErr, e:
            msg = QtGui.QMessageBox(self)
            msg.setText(e.error_msg+'\n'+str(e.request_params))
            msg.setWindowTitle('Api Error')
            msg.exec_()
            return


