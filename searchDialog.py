# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'searchDialog.ui'
#
# Created: Tue May 14 01:08:39 2013
#      by: PyQt4 UI code generator 4.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_SearchDialog(object):
    def setupUi(self, SearchDialog):
        SearchDialog.setObjectName(_fromUtf8("SearchDialog"))
        SearchDialog.resize(507, 312)
        self.groupBox = QtGui.QGroupBox(SearchDialog)
        self.groupBox.setGeometry(QtCore.QRect(0, 10, 491, 231))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.searchLineEdit = QtGui.QLineEdit(self.groupBox)
        self.searchLineEdit.setGeometry(QtCore.QRect(0, 0, 321, 27))
        self.searchLineEdit.setObjectName(_fromUtf8("searchLineEdit"))
        self.searchPushButton = QtGui.QPushButton(self.groupBox)
        self.searchPushButton.setGeometry(QtCore.QRect(320, 0, 51, 27))
        self.searchPushButton.setObjectName(_fromUtf8("searchPushButton"))
        self.getOwnListButton = QtGui.QPushButton(self.groupBox)
        self.getOwnListButton.setGeometry(QtCore.QRect(370, 0, 61, 27))
        self.getOwnListButton.setObjectName(_fromUtf8("getOwnListButton"))
        self.searchTableWidget = QtGui.QTableWidget(self.groupBox)
        self.searchTableWidget.setGeometry(QtCore.QRect(0, 30, 451, 181))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.searchTableWidget.sizePolicy().hasHeightForWidth())
        self.searchTableWidget.setSizePolicy(sizePolicy)
        self.searchTableWidget.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.searchTableWidget.setSelectionBehavior(QtGui.QAbstractItemView.SelectItems)
        self.searchTableWidget.setShowGrid(True)
        self.searchTableWidget.setObjectName(_fromUtf8("searchTableWidget"))
        self.searchTableWidget.setColumnCount(3)
        self.searchTableWidget.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setStyleStrategy(QtGui.QFont.PreferDefault)
        item.setFont(font)
        self.searchTableWidget.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
        self.searchTableWidget.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.NoBrush)
        item.setForeground(brush)
        self.searchTableWidget.setHorizontalHeaderItem(2, item)
        self.addPushButton = QtGui.QPushButton(SearchDialog)
        self.addPushButton.setGeometry(QtCore.QRect(340, 240, 97, 27))
        self.addPushButton.setObjectName(_fromUtf8("addPushButton"))
        self.backPushButton = QtGui.QPushButton(SearchDialog)
        self.backPushButton.setGeometry(QtCore.QRect(0, 240, 97, 27))
        self.backPushButton.setObjectName(_fromUtf8("backPushButton"))

        self.retranslateUi(SearchDialog)
        QtCore.QMetaObject.connectSlotsByName(SearchDialog)

    def retranslateUi(self, SearchDialog):
        SearchDialog.setWindowTitle(_translate("SearchDialog", "SearchDialog", None))
        self.groupBox.setTitle(_translate("SearchDialog", "GroupBox", None))
        self.searchPushButton.setText(_translate("SearchDialog", "Search", None))
        self.getOwnListButton.setText(_translate("SearchDialog", "own list", None))
        item = self.searchTableWidget.horizontalHeaderItem(0)
        item.setText(_translate("SearchDialog", "Artist", None))
        item = self.searchTableWidget.horizontalHeaderItem(1)
        item.setText(_translate("SearchDialog", "Title", None))
        item = self.searchTableWidget.horizontalHeaderItem(2)
        item.setText(_translate("SearchDialog", "Duration", None))
        self.addPushButton.setText(_translate("SearchDialog", "Add", None))
        self.backPushButton.setText(_translate("SearchDialog", "Back", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    SearchDialog = QtGui.QDialog()
    ui = Ui_SearchDialog()
    ui.setupUi(SearchDialog)
    SearchDialog.show()
    sys.exit(app.exec_())

