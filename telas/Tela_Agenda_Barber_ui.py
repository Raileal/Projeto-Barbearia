# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:\Programacao\Projetos\ProjetoBarbearia\telas\Tela_Agenda_Barber.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Tela_Agenda_barber(object):
    def setupUi(self, Tela_Agenda_barber):
        Tela_Agenda_barber.setObjectName("Tela_Agenda_barber")
        Tela_Agenda_barber.resize(1000, 700)
        Tela_Agenda_barber.setMinimumSize(QtCore.QSize(1000, 700))
        Tela_Agenda_barber.setMaximumSize(QtCore.QSize(1000, 700))
        self.centralwidget = QtWidgets.QWidget(Tela_Agenda_barber)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(10, 640, 93, 28))
        self.pushButton.setObjectName("pushButton")
        self.layoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(260, 580, 491, 30))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEdit_2.setText("")
        self.lineEdit_2.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.horizontalLayout.addWidget(self.lineEdit_2)
        self.pushButton_2 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout.addWidget(self.pushButton_2)
        self.pushButton_3 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_3.setObjectName("pushButton_3")
        self.horizontalLayout.addWidget(self.pushButton_3)
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(860, 640, 124, 28))
        self.pushButton_4.setObjectName("pushButton_4")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(430, 10, 139, 33))
        self.label.setObjectName("label")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(470, 60, 62, 21))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(460, 100, 79, 21))
        self.label_4.setObjectName("label_4")
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(170, 130, 661, 441))
        self.listWidget.setObjectName("listWidget")
        Tela_Agenda_barber.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(Tela_Agenda_barber)
        self.statusbar.setObjectName("statusbar")
        Tela_Agenda_barber.setStatusBar(self.statusbar)

        self.retranslateUi(Tela_Agenda_barber)
        QtCore.QMetaObject.connectSlotsByName(Tela_Agenda_barber)

    def retranslateUi(self, Tela_Agenda_barber):
        _translate = QtCore.QCoreApplication.translate
        Tela_Agenda_barber.setWindowTitle(_translate("Tela_Agenda_barber", "MainWindow"))
        self.pushButton.setText(_translate("Tela_Agenda_barber", "Voltar"))
        self.lineEdit_2.setPlaceholderText(_translate("Tela_Agenda_barber", "Digite a Busca"))
        self.pushButton_2.setText(_translate("Tela_Agenda_barber", "Buscar"))
        self.pushButton_3.setText(_translate("Tela_Agenda_barber", "Mostrar Original"))
        self.pushButton_4.setText(_translate("Tela_Agenda_barber", "Desmarcar por Data"))
        self.label.setText(_translate("Tela_Agenda_barber", "<html><head/><body><p align=\"center\"><span style=\" font-size:16pt;\">BARBEARIA</span></p></body></html>"))
        self.label_3.setText(_translate("Tela_Agenda_barber", "<html><head/><body><p align=\"center\"><span style=\" font-size:10pt;\">Barbeiro</span></p></body></html>"))
        self.label_4.setText(_translate("Tela_Agenda_barber", "<html><head/><body><p align=\"center\"><span style=\" font-size:10pt;\">AGENDA</span></p></body></html>"))
