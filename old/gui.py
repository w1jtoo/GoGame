# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Field(object):
    def setupUi(self, Field):
        Field.setObjectName("Field")
        Field.resize(400, 500)
        Field.setMinimumSize(QtCore.QSize(400, 400))
        Field.setMaximumSize(QtCore.QSize(400, 500))
        Field.setMouseTracking(1)
        Field.setGeometry(0, 0, 400, 500)
        self.QGraph_field = QtWidgets.QGraphicsView(Field)
        self.QGraph_field.setGeometry(QtCore.QRect(0, 0, 400, 400))
        self.QGraph_field.setMouseTracking(1)
        self.QGraph_field.setMinimumSize(QtCore.QSize(0, 0))
        self.QGraph_field.setMaximumSize(QtCore.QSize(400, 400))
        #self.QGraph_field.setFocusPolicy(QtCore.Qt.NoFocus)
        #self.QGraph_field.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        #elf.QGraph_field.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.QGraph_field.setSceneRect(QtCore.QRectF(0.0, 0.0, 250.0, 250.0))
        self.QGraph_field.setObjectName("QGraph_field")

        self.retranslateUi(Field)
        QtCore.QMetaObject.connectSlotsByName(Field)

    def retranslateUi(self, Field):
        _translate = QtCore.QCoreApplication.translate
        Field.setWindowTitle(_translate("Field", "Go Game"))
