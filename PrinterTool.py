#!env python3
# -*- coding: utf-8 -*-

import argparse
import base64
import json
import os
import plistlib
import re
import shlex
import subprocess
import sys
import time
import traceback

import _tkinter

from functools import partial
from xml.etree import ElementTree
from xml.sax.saxutils import escape

import requests

from cryptography.fernet import Fernet
from PySide2 import QtCore, QtGui, QtWidgets


__application__ = "Jamf Pro Printer Tool"
__version__ = "v1.2.3"
__author__ = "Zack Thompson"
__created__ = "8/11/2020"
__updated__ = "9/25/2023"
__description__ = "This script utilizes the PySide2 Library (Qt) to generate a GUI that Site \
                    Admins can use to manage their own printers within Jamf Pro."
__about__ = """<html><head/><body><p><strong>Created By:</strong>  Zack Thompson</p>

<p><strong>Source:</strong></p>
Source code can be found on <a href="https://github.com/MLBZ521/JamfProPrinterTool">GitHub</a>!


<p><strong>Contributors:</strong></p>


<p><strong>Licenses:</strong></p>

<p>The code that generates the "Jamf Pro Printer Tool" is licensed under the MIT License.  A copy \
    of the MIT License can be found below.</p>

<p>This application utilizes the Qt Framework (specifically PySide2) to generate the GUI portion \
    of the application.  The author of this application has made efforts to abide by the Qt LGPL \
    License terms.  Additional information can be found below.</p>

<p>The current image used in this project is property of Jamf.  Copyright © Jamf. All rights \
    reserved.  Jamf Pro is a trademark of Jamf.</p>


<p><strong>About Qt</strong></p>
<p>This program uses Qt version 5.15.2</p>

<p>Qt is a C++ toolkit for cross-platform application development.  Qt is The Qt Company Ltd \
    product developed as an open source project. See <a href="https://qt.io">qt.io</a> for more \
    information.</p>

<p>Qt and Qt for Python (PySide2) are licensed under the GNU (L)GPLv3.  Please see <a \
    href="https://qt.io/licensing">qt.io/licensing</a> for an overview of Qt licensing.</p>

<p>Copyright (C) 2020 The Qt Company Ltd and other contributors.  Qt and the Qt logo are \
    trademarks of The Qt Company Ltd.</p>


<p><strong>MIT License:</strong></p>
<p>Permission is hereby granted, free of charge, to any person obtaining a copy of this software \
    and associated documentation files (the "Software"), to deal in the Software without \
    restriction, including without limitation the rights to use, copy, modify, merge, publish, \
    distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the \
    Software is furnished to do so, subject to the following conditions:</p>

<p>The above copyright notice and this permission notice shall be included in all copies or \
    substantial portions of the Software.</p>

<p>THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING \
    BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND \
    NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, \
    DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, \
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.</p>
</body></html>"""


class Ui_MainWindow(object):
    def setup_ui(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowModality(QtCore.Qt.NonModal)
        MainWindow.setEnabled(True)
        MainWindow.resize(560, 525)
        MainWindow.setMinimumSize(QtCore.QSize(560, 525))
        MainWindow.setMaximumSize(QtCore.QSize(930, 525))
        MainWindow.setAcceptDrops(False)
        MainWindow.setTabShape(QtWidgets.QTabWidget.Rounded)
        MainWindow.setDockNestingEnabled(False)
        MainWindow.setDockOptions(
            QtWidgets.QMainWindow.AllowTabbedDocks|QtWidgets.QMainWindow.AnimatedDocks)
        MainWindow.setUnifiedTitleAndToolBarOnMac(False)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.progress_bar = QtWidgets.QProgressBar(self.centralwidget)
        self.progress_bar.setGeometry(QtCore.QRect(20, 460, 511, 31))
        self.progress_bar.setProperty("value", 0)
        self.progress_bar.setObjectName("progress_bar")
        self.frame_sites = QtWidgets.QFrame(self.centralwidget)
        self.frame_sites.setGeometry(QtCore.QRect(10, 10, 541, 81))
        self.frame_sites.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_sites.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_sites.setObjectName("frame_sites")
        self.label_sites = QtWidgets.QLabel(self.frame_sites)
        self.label_sites.setGeometry(QtCore.QRect(10, 10, 401, 16))
        self.label_sites.setObjectName("label_sites")
        self.button_get_sites = QtWidgets.QPushButton(self.frame_sites)
        self.button_get_sites.setGeometry(QtCore.QRect(10, 40, 112, 32))
        self.button_get_sites.setStatusTip("")
        self.button_get_sites.setObjectName("button_get_sites")
        self.combo_sites = QtWidgets.QComboBox(self.frame_sites)
        self.combo_sites.setEnabled(False)
        self.combo_sites.setGeometry(QtCore.QRect(130, 40, 231, 32))
        self.combo_sites.setObjectName("combo_sites")
        self.frame_jps_printers = QtWidgets.QFrame(self.centralwidget)
        self.frame_jps_printers.setGeometry(QtCore.QRect(10, 320, 541, 131))
        self.frame_jps_printers.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_jps_printers.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_jps_printers.setObjectName("frame_jps_printers")
        self.label_printers = QtWidgets.QLabel(self.frame_jps_printers)
        self.label_printers.setGeometry(QtCore.QRect(10, 10, 231, 31))
        self.label_printers.setObjectName("label_printers")
        self.button_get_printers = QtWidgets.QPushButton(self.frame_jps_printers)
        self.button_get_printers.setEnabled(False)
        self.button_get_printers.setGeometry(QtCore.QRect(10, 50, 112, 32))
        self.button_get_printers.setObjectName("button_get_printers")
        self.combo_printers = QtWidgets.QComboBox(self.frame_jps_printers)
        self.combo_printers.setEnabled(False)
        self.combo_printers.setGeometry(QtCore.QRect(130, 50, 361, 32))
        self.combo_printers.setObjectName("combo_printers")
        self.button_update_printer = QtWidgets.QPushButton(self.frame_jps_printers)
        self.button_update_printer.setEnabled(False)
        self.button_update_printer.setGeometry(QtCore.QRect(150, 90, 112, 32))
        self.button_update_printer.setObjectName("button_update_printer")
        self.button_delete_printer = QtWidgets.QPushButton(self.frame_jps_printers)
        self.button_delete_printer.setEnabled(False)
        self.button_delete_printer.setGeometry(QtCore.QRect(280, 90, 112, 32))
        self.button_delete_printer.setObjectName("button_delete_printer")
        self.frame_local_printers = QtWidgets.QFrame(self.centralwidget)
        self.frame_local_printers.setGeometry(QtCore.QRect(10, 110, 541, 191))
        self.frame_local_printers.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_local_printers.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_local_printers.setObjectName("frame_local_printers")
        self.label_create = QtWidgets.QLabel(self.frame_local_printers)
        self.label_create.setGeometry(QtCore.QRect(10, 0, 401, 31))
        self.label_create.setObjectName("label_create")
        self.button_create_printers = QtWidgets.QPushButton(self.frame_local_printers)
        self.button_create_printers.setEnabled(False)
        self.button_create_printers.setGeometry(QtCore.QRect(200, 150, 112, 32))
        self.button_create_printers.setObjectName("button_create_printers")
        self.qlist_local_printers = QtWidgets.QListWidget(self.frame_local_printers)
        self.qlist_local_printers.setEnabled(True)
        self.qlist_local_printers.setGeometry(QtCore.QRect(10, 30, 511, 111))
        self.qlist_local_printers.setObjectName("qlist_local_printers")
        self.frame_printer_info = QtWidgets.QFrame(self.centralwidget)
        self.frame_printer_info.setGeometry(QtCore.QRect(570, 10, 351, 441))
        self.frame_printer_info.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_printer_info.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_printer_info.setObjectName("frame_printer_info")
        self.layoutWidget = QtWidgets.QWidget(self.frame_printer_info)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 10, 331, 421))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.label_updated_by = QtWidgets.QLabel(self.layoutWidget)
        self.label_updated_by.setObjectName("label_updated_by")
        self.gridLayout.addWidget(self.label_updated_by, 8, 0, 1, 1)
        self.label_created_by = QtWidgets.QLabel(self.layoutWidget)
        self.label_created_by.setObjectName("label_created_by")
        self.gridLayout.addWidget(self.label_created_by, 7, 0, 1, 1)
        self.label_printer_cups_name = QtWidgets.QLabel(self.layoutWidget)
        self.label_printer_cups_name.setObjectName("label_printer_cups_name")
        self.gridLayout.addWidget(self.label_printer_cups_name, 4, 0, 1, 1)
        self.lineEdit_printer_location = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEdit_printer_location.setReadOnly(True)
        self.lineEdit_printer_location.setObjectName("lineEdit_printer_location")
        self.gridLayout.addWidget(self.lineEdit_printer_location, 1, 2, 1, 1)
        self.lineEdit_printer_device_uri = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEdit_printer_device_uri.setReadOnly(True)
        self.lineEdit_printer_device_uri.setObjectName("lineEdit_printer_device_uri")
        self.gridLayout.addWidget(self.lineEdit_printer_device_uri, 3, 2, 1, 1)
        self.label_printer_device_uri = QtWidgets.QLabel(self.layoutWidget)
        self.label_printer_device_uri.setObjectName("label_printer_device_uri")
        self.gridLayout.addWidget(self.label_printer_device_uri, 3, 0, 1, 1)
        self.label_printer_model = QtWidgets.QLabel(self.layoutWidget)
        self.label_printer_model.setObjectName("label_printer_model")
        self.gridLayout.addWidget(self.label_printer_model, 2, 0, 1, 1)
        self.lineEdit_printer_ppd_file_path = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEdit_printer_ppd_file_path.setReadOnly(True)
        self.lineEdit_printer_ppd_file_path.setObjectName("lineEdit_printer_ppd_file_path")
        self.gridLayout.addWidget(self.lineEdit_printer_ppd_file_path, 5, 2, 1, 1)
        self.lineEdit_printer_model = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEdit_printer_model.setReadOnly(True)
        self.lineEdit_printer_model.setObjectName("lineEdit_printer_model")
        self.gridLayout.addWidget(self.lineEdit_printer_model, 2, 2, 1, 1)
        self.lineEdit_printer_cups_name = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEdit_printer_cups_name.setReadOnly(True)
        self.lineEdit_printer_cups_name.setObjectName("lineEdit_printer_cups_name")
        self.gridLayout.addWidget(self.lineEdit_printer_cups_name, 4, 2, 1, 1)
        self.label_site = QtWidgets.QLabel(self.layoutWidget)
        self.label_site.setObjectName("label_site")
        self.gridLayout.addWidget(self.label_site, 6, 0, 1, 1)
        self.label_printer_ppd_path = QtWidgets.QLabel(self.layoutWidget)
        self.label_printer_ppd_path.setObjectName("label_printer_ppd_path")
        self.gridLayout.addWidget(self.label_printer_ppd_path, 5, 0, 1, 1)
        self.lineEdit_printer_display_name = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEdit_printer_display_name.setEnabled(True)
        self.lineEdit_printer_display_name.setFrame(True)
        self.lineEdit_printer_display_name.setCursorPosition(0)
        self.lineEdit_printer_display_name.setReadOnly(True)
        self.lineEdit_printer_display_name.setObjectName("lineEdit_printer_display_name")
        self.gridLayout.addWidget(self.lineEdit_printer_display_name, 0, 2, 1, 1)
        self.label_printer_ppd_contents = QtWidgets.QLabel(self.layoutWidget)
        self.label_printer_ppd_contents.setAlignment(
            QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.label_printer_ppd_contents.setObjectName("label_printer_ppd_contents")
        self.gridLayout.addWidget(self.label_printer_ppd_contents, 9, 0, 1, 1)
        self.textEdit_printer_ppd_contents = QtWidgets.QTextEdit(self.layoutWidget)
        self.textEdit_printer_ppd_contents.setReadOnly(True)
        self.textEdit_printer_ppd_contents.setObjectName("textEdit_printer_ppd_contents")
        self.gridLayout.addWidget(self.textEdit_printer_ppd_contents, 9, 2, 1, 1)
        self.label_printer_display_name = QtWidgets.QLabel(self.layoutWidget)
        self.label_printer_display_name.setObjectName("label_printer_display_name")
        self.gridLayout.addWidget(self.label_printer_display_name, 0, 0, 1, 1)
        self.label_printer_location = QtWidgets.QLabel(self.layoutWidget)
        self.label_printer_location.setObjectName("label_printer_location")
        self.gridLayout.addWidget(self.label_printer_location, 1, 0, 1, 1)
        self.lineEdit_site = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEdit_site.setReadOnly(True)
        self.lineEdit_site.setObjectName("lineEdit_site")
        self.gridLayout.addWidget(self.lineEdit_site, 6, 2, 1, 1)
        self.lineEdit_created_by = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEdit_created_by.setReadOnly(True)
        self.lineEdit_created_by.setObjectName("lineEdit_created_by")
        self.gridLayout.addWidget(self.lineEdit_created_by, 7, 2, 1, 1)
        self.lineEdit_updated_by = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEdit_updated_by.setReadOnly(True)
        self.lineEdit_updated_by.setObjectName("lineEdit_updated_by")
        self.gridLayout.addWidget(self.lineEdit_updated_by, 8, 2, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 560, 22))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuSettings = QtWidgets.QMenu(self.menubar)
        self.menuSettings.setObjectName("menuSettings")
        MainWindow.setMenuBar(self.menubar)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)
        self.actionClearAPIToken = QtWidgets.QAction(MainWindow)
        self.actionClearAPIToken.setShortcutVisibleInContextMenu(False)
        self.actionClearAPIToken.setObjectName("actionClearAPIToken")
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionShow_Details = QtWidgets.QAction(MainWindow)
        self.actionShow_Details.setObjectName("actionShow_Details")
        self.actionAbout = QtWidgets.QAction(MainWindow)
        self.actionAbout.setObjectName(u"actionAbout")
        self.menuFile.addAction(self.actionExit)
        self.menuFile.addAction(self.actionAbout)
        self.menuSettings.addAction(self.actionClearAPIToken)
        self.menuSettings.addAction(self.actionShow_Details)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuSettings.menuAction())

        QtWidgets.QWidget.setTabOrder(self.button_get_sites, self.combo_sites)
        QtWidgets.QWidget.setTabOrder(self.combo_sites, self.qlist_local_printers)
        QtWidgets.QWidget.setTabOrder(self.qlist_local_printers, self.button_create_printers)
        QtWidgets.QWidget.setTabOrder(self.button_create_printers, self.button_get_printers)
        QtWidgets.QWidget.setTabOrder(self.button_get_printers, self.combo_printers)
        QtWidgets.QWidget.setTabOrder(self.combo_printers, self.button_update_printer)
        QtWidgets.QWidget.setTabOrder(self.button_update_printer, self.button_delete_printer)
        QtWidgets.QWidget.setTabOrder(
            self.button_delete_printer, self.lineEdit_printer_display_name)
        QtWidgets.QWidget.setTabOrder(
            self.lineEdit_printer_display_name, self.lineEdit_printer_location)
        QtWidgets.QWidget.setTabOrder(self.lineEdit_printer_location, self.lineEdit_printer_model)
        QtWidgets.QWidget.setTabOrder(
            self.lineEdit_printer_model, self.lineEdit_printer_device_uri)
        QtWidgets.QWidget.setTabOrder(
            self.lineEdit_printer_device_uri, self.lineEdit_printer_cups_name)
        QtWidgets.QWidget.setTabOrder(
            self.lineEdit_printer_cups_name, self.lineEdit_printer_ppd_file_path)
        QtWidgets.QWidget.setTabOrder(self.lineEdit_printer_ppd_file_path, self.lineEdit_site)
        QtWidgets.QWidget.setTabOrder(self.lineEdit_site, self.lineEdit_created_by)
        QtWidgets.QWidget.setTabOrder(self.lineEdit_created_by, self.lineEdit_updated_by)
        QtWidgets.QWidget.setTabOrder(self.lineEdit_updated_by, self.textEdit_printer_ppd_contents)

        self.retranslate_ui(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslate_ui(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Jamf Pro Printer Tool"))
        self.label_sites.setText(_translate("MainWindow", "Select the Site to work in:"))
        self.button_get_sites.setText(_translate("MainWindow", "Get Sites"))
        self.label_printers.setText(
            _translate("MainWindow", "Select the printer you want to modify:"))
        self.button_get_printers.setText(_translate("MainWindow", "Get Printers"))
        self.button_update_printer.setText(_translate("MainWindow", "Update Printer"))
        self.button_delete_printer.setText(_translate("MainWindow", "Delete Printer"))
        self.label_create.setText(_translate(
            "MainWindow", "Select the printer you want to use to create or update in Jamf Pro:"))
        self.button_create_printers.setText(_translate("MainWindow", "Create"))
        self.label_updated_by.setText(_translate("MainWindow", "Updated By"))
        self.label_created_by.setText(_translate("MainWindow", "Created By"))
        self.label_printer_cups_name.setText(_translate("MainWindow", "CUPS Name"))
        self.label_printer_device_uri.setText(_translate("MainWindow", "Device URI"))
        self.label_printer_model.setText(_translate("MainWindow", "Model"))
        self.label_site.setText(_translate("MainWindow", "Site"))
        self.label_printer_ppd_path.setText(_translate("MainWindow", "PPD File Path"))
        self.label_printer_ppd_contents.setText(_translate("MainWindow", "PPD Contents"))
        self.label_printer_display_name.setText(_translate("MainWindow", "Display Name"))
        self.label_printer_location.setText(_translate("MainWindow", "Location"))
        self.menuFile.setTitle(_translate("MainWindow", "FIle"))
        self.menuSettings.setTitle(_translate("MainWindow", "Settings"))
        self.actionClearAPIToken.setText(_translate("MainWindow", "Clear API Token"))
        self.actionClearAPIToken.setShortcut(_translate("MainWindow", "Ctrl+C"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionShow_Details.setText(_translate("MainWindow", "Show Details"))
        self.actionShow_Details.setShortcut(_translate("MainWindow", "Ctrl+D"))
        self.actionAbout.setText(_translate("MainWindow", u"About", None))


class Ui_LoginWindow(object):
    def setup_ui(self, LoginWindow):
        LoginWindow.setObjectName("LoginWindow")
        LoginWindow.setWindowModality(QtCore.Qt.WindowModal)
        LoginWindow.resize(494, 190)
        self.layoutWidget = QtWidgets.QWidget(LoginWindow)
        self.layoutWidget.setGeometry(QtCore.QRect(130, 60, 345, 81))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_description = QtWidgets.QLabel(self.layoutWidget)
        self.label_description.setObjectName("label_description")
        self.verticalLayout.addWidget(self.label_description)
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setFormAlignment(
            QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.formLayout.setObjectName("formLayout")
        self.label_username = QtWidgets.QLabel(self.layoutWidget)
        self.label_username.setObjectName("label_username")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_username)
        self.lineEdit_username = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEdit_username.setEnabled(True)
        self.lineEdit_username.setMinimumSize(QtCore.QSize(250, 0))
        self.lineEdit_username.setFrame(True)
        self.lineEdit_username.setObjectName("lineEdit_username")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.lineEdit_username)
        self.label_password = QtWidgets.QLabel(self.layoutWidget)
        self.label_password.setObjectName("label_password")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_password)
        self.lineEdit_password = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEdit_password.setMinimumSize(QtCore.QSize(250, 0))
        self.lineEdit_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_password.setPlaceholderText("")
        self.lineEdit_password.setObjectName("lineEdit_password")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.lineEdit_password)
        self.verticalLayout.addLayout(self.formLayout)
        self.label = QtWidgets.QLabel(LoginWindow)
        self.label.setGeometry(QtCore.QRect(10, -20, 101, 111))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap(app_icon))
        self.label.setObjectName("label")
        self.label_heading = QtWidgets.QLabel(LoginWindow)
        self.label_heading.setGeometry(QtCore.QRect(130, 10, 361, 41))
        self.label_heading.setObjectName("label_heading")
        self.widget = QtWidgets.QWidget(LoginWindow)
        self.widget.setGeometry(QtCore.QRect(290, 150, 171, 32))
        self.widget.setObjectName("widget")
        self.gridLayout = QtWidgets.QGridLayout(self.widget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.buttonOK = QtWidgets.QPushButton(self.widget)
        self.buttonOK.setObjectName("buttonOK")
        self.gridLayout.addWidget(self.buttonOK, 0, 1, 1, 1)
        self.buttonCancel = QtWidgets.QPushButton(self.widget)
        self.buttonCancel.setObjectName("buttonCancel")
        self.gridLayout.addWidget(self.buttonCancel, 0, 0, 1, 1)

        self.retranslate_ui(LoginWindow)
        QtCore.QMetaObject.connectSlotsByName(LoginWindow)

    def retranslate_ui(self, LoginWindow):
        _translate = QtCore.QCoreApplication.translate
        LoginWindow.setWindowTitle(_translate("LoginWindow", "Login"))
        self.label_description.setText(_translate(
            "LoginWindow",
            "<html><head/><body><p><span style=\" font-weight:600;\">\
                Enter your Site Admin credentials.</span></p></body></html>"
        ))
        self.label_username.setText(_translate("LoginWindow", "Username:  "))
        self.label_password.setText(_translate("LoginWindow", "Password:  "))
        self.label_heading.setText(_translate(
            "LoginWindow",
            "<html><head/><body><p>To determine which Sites you \
                manage, please authenticate.</p></body></html>"
        ))
        self.buttonOK.setText(_translate("LoginWindow", "OK"))
        self.buttonCancel.setText(_translate("LoginWindow", "Cancel"))


class Ui_About(object):
    def setup_ui(self, About):
        if not About.objectName():
            About.setObjectName(u"About")
        About.resize(400, 400)
        About.setMinimumSize(QtCore.QSize(400, 400))
        About.setMaximumSize(QtCore.QSize(400, 400))
        About.setSizeIncrement(QtCore.QSize(400, 400))
        self.verticalLayout = QtWidgets.QVBoxLayout(About)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.logo = QtWidgets.QLabel(About)
        self.logo.setObjectName(u"logo")
        self.logo.setPixmap(QtGui.QPixmap(app_icon))
        self.logo.setAlignment(QtCore.Qt.AlignCenter)
        self.verticalLayout.addWidget(self.logo)
        self.app_name_label = QtWidgets.QLabel(About)
        self.app_name_label.setObjectName(u"app_name_label")
        self.app_name_label.setAlignment(QtCore.Qt.AlignCenter)
        self.verticalLayout.addWidget(self.app_name_label)
        self.version_layout = QtWidgets.QFormLayout()
        self.version_layout.setObjectName(u"version_layout")
        self.version_label = QtWidgets.QLabel(About)
        self.version_label.setObjectName(u"version_label")
        self.version_label.setAlignment(QtCore.Qt.AlignCenter)
        self.version_layout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.version_label)
        self.version_string_label = QtWidgets.QLabel(About)
        self.version_string_label.setObjectName(u"version_string_label")
        self.version_string_label.setAlignment(QtCore.Qt.AlignCenter)
        self.version_layout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.version_string_label)
        self.verticalLayout.addLayout(self.version_layout)
        self.textBrowser_label = QtWidgets.QTextBrowser(About)
        self.textBrowser_label.setObjectName(u"textBrowser_label")
        self.textBrowser_label.setReadOnly(True)
        self.textBrowser_label.setOpenExternalLinks(True)
        self.verticalLayout.addWidget(self.textBrowser_label)
        self.copyright_label = QtWidgets.QLabel(About)
        self.copyright_label.setObjectName(u"copyright_label")
        self.copyright_label.setAlignment(QtCore.Qt.AlignCenter)
        self.verticalLayout.addWidget(self.copyright_label)

        self.retranslate_ui(About)
        QtCore.QMetaObject.connectSlotsByName(About)

    def retranslate_ui(self, About):
        About.setWindowTitle(QtCore.QCoreApplication.translate("About", u"About", None))
        self.logo.setText("")
        self.app_name_label.setText(QtCore.QCoreApplication.translate(
            "About",
            u"<html><head/><body><p><span style=\" font-weight:600;\">\
                Jamf Pro Printer Tool</span></p></body></html>",
            None
            ))
        self.version_label.setText(QtCore.QCoreApplication.translate("About", u"Version:", None))
        self.version_string_label.setText(QtCore.QCoreApplication.translate(
            "About",
            __version__,
            None
        ))
        self.copyright_label.setText(QtCore.QCoreApplication.translate(
            "About",
            u"<html><head/><body><p><span style=\" font-size:12pt;\">\
                Copyright \u00a92021 Zack Thompson</span></p></body></html>",
            None
        ))
        self.textBrowser_label.setText(QtCore.QCoreApplication.translate("About", __about__, None))


class About(QtWidgets.QDialog, Ui_About):
    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.setup_ui(self)
        self.parent = parent


class LoginWindow(QtWidgets.QDialog, Ui_LoginWindow):
    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.setup_ui(self)
        self.parent = parent

        ##### Setup actions, buttons, triggers, etc
        self.buttonOK.clicked.connect(lambda: self.parent.get_site_admin_token(self.buttonOK, self))
        self.buttonCancel.clicked.connect(
            lambda: self.parent.get_site_admin_token(self.buttonCancel, self))

        # Setup to close the login window/login prompt
        self.closeLoginWindow = WorkerSignals()
        self.closeLoginWindow.close.connect(self.close_window)

    def close_window(self):
        """
        Handles closing the window
        """
        self.close()


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.setup_ui(self)
        self.worker = None

        # Configure the window size
        self.height = 525
        self.defaultWidth = 560
        self.extendedWidth = 930
        self.setMinimumSize(QtCore.QSize(self.defaultWidth, self.height))
        self.setMaximumSize(QtCore.QSize(self.extendedWidth, self.height))

        # Create a QThreadPool Instance
        self.threadpool = QtCore.QThreadPool()
        print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())

        # Setup pausing mechanism
        self.mutex = QtCore.QMutex()
        self.condition = QtCore.QWaitCondition()

        # Create a list to add each printer into
        self.jps_printer_list = []

        ##### Setup actions, buttons, triggers, etc

        # When the Exit Action is triggered
        self.actionExit.triggered.connect(self.close_window)

        # When the About Action is triggered
        self.actionAbout.triggered.connect(self.show_about)

        # When the Show Details Action is triggered
        self.actionShow_Details.triggered.connect(self.resize_window)

        # When the Clear API Token Action is triggered
        self.actionClearAPIToken.triggered.connect(self.clear_api_token)

        # When Get Sites button is clicked
        self.button_get_sites.clicked.connect(self.run_get_site_access)

        # When a printer is selected in the QList of local printers
        self.qlist_local_printers.currentTextChanged.connect(self.display_printer_details)
        self.qlist_local_printers.currentTextChanged.connect(self.button_handler)

        # When the Site ComboBox value has changed
        self.combo_sites.currentTextChanged.connect(self.populate_printer_combo_box)
        self.combo_sites.currentTextChanged.connect(self.button_handler)

        # When a printer is selected in the ComboBox of JPS printers
        self.combo_printers.activated.connect(self.display_printer_details)
        self.combo_printers.currentTextChanged.connect(self.button_handler)

        # When the Create Printer button is clicked
        self.button_create_printers.clicked.connect(self.run_create_printer)
        # For selecting multiple printers...?
        # self.qlist_local_printers.itemSelectionChanged.connect(self.selectedLocalPrinter)

        # When the Get Printers button is clicked
        self.button_get_printers.clicked.connect(self.run_get_jps_printers)

        # When the Update Printer is clicked
        self.button_update_printer.clicked.connect(self.run_update_printer)

        # When the Delete Printer is clicked
        self.button_delete_printer.clicked.connect(self.run_delete_printer)

        # Setup to display login window/login prompt
        self.displayLoginWindow = WorkerSignals()
        self.displayLoginWindow.prompt.connect(self.login_prompt)


    ################################################################################################
    # Threading Functions

    def run_get_local_printers(self):
        self.worker_thread(self.get_local_printers)


    def run_get_site_access(self):
        self.worker_thread(self.clicked_get_sites)


    def run_create_printer(self):
        self.worker_thread(self.clicked_create_printer)


    def run_get_jps_printers(self):
        self.worker_thread(self.get_jps_printers)


    def run_update_printer(self):
        self.worker_thread(self.clicked_update_printer)


    def run_delete_printer(self):
        self.worker_thread(self.clicked_delete_printer)


    def run_get_jps_printer_details(self, id_printer):
        self.worker_thread(partial(self.get_jps_printer_details, printer_id=id_printer))


    def worker_thread(self, function):
        """
        Sets up worker threads that are added to a QThreadPool

        Args:
            function:  A function that will be executed
        """

        # Pass the function to execute
        self.worker = Worker(function)
        self.worker.signals.finished.connect(self.finished_worker)
        self.worker.signals.progress.connect(self.update_worker)
        self.worker.signals.warning.connect(self.warning_worker)
        self.worker.stopped = False
        self.threadpool.start(self.worker)


    def shutdown(self):
        """
        Called with the application is closed
        """

        print("Shutting Down!")

        background_threads = self.threadpool.activeThreadCount()

        if background_threads > 0:
            print(f"Background threads running:  {background_threads}")

            if self.worker:
                print("Terminating background threads...")
                self.worker.stopped = True
                self.threadpool.waitForDone(1000)


    def update_worker(self, notification):
        """
        Callback function to updated the progress and status bars
        """

        message = notification.get("msg")
        progressBar_type = notification.get("pb_type", None)
        total_count = notification.get("total", 0)
        current_count = notification.get("count", 0)

        self.statusBar.showMessage(message)

        if progressBar_type == "Pulse":

            # Pulse Progress Bar
            self.progress_bar.setRange(0,0)

        else:

            # Determined Progress Bar
            self.progress_bar.setMaximum(int(total_count))
            self.progress_bar.setValue(int(current_count))


    def finished_worker(self, msg):
        """
        Callback function to stop the progress bar and update the status bar
        """

        self.statusBar.showMessage(msg)

        # Stop Progress Bar
        self.progress_bar.setRange(0,1)

        # Update the Printer ComboBox
        self.populate_printer_combo_box()

        # Update Button State
        self.button_handler()


    def warning_worker(self, msg):
        """
        Callback function to stop the progress bar and update the status bar
        """

        self.statusBar.showMessage(msg)

        # Stop Progress Bar
        self.progress_bar.setRange(0,1)

        # Update Button State
        self.button_handler()


    ################################################################################################
    # Qt GUI Helpers

    def close_window(self):
        """
        Handles closing the main window
        """

        self.close()


    def resize_window(self):
        """
        Handles resizing the window to show and hide printer details
        """

        currentWidth = self.width()

        if self.defaultWidth == currentWidth:

            MainWindow.animation = QtCore.QPropertyAnimation(self, b"size")
            MainWindow.animation.setDuration(300)
            MainWindow.animation.setStartValue(QtCore.QSize(self.defaultWidth, self.height))
            MainWindow.animation.setEndValue(QtCore.QSize(self.extendedWidth, self.height))

        else:

            MainWindow.animation = QtCore.QPropertyAnimation(self, b"size")
            MainWindow.animation.setDuration(300)
            MainWindow.animation.setStartValue(QtCore.QSize(self.extendedWidth, self.height))
            MainWindow.animation.setEndValue(QtCore.QSize(self.defaultWidth, self.height))

        MainWindow.animation.start()


    def show_about(self):
        """
        Handles displaying the About UI
        """

        # Display Login UI
        self.about = About(parent=self)
        self.about.exec_()


    def login_prompt(self):
        """
        Handles displaying the Login Window UI
        """

        # Update Status Bar and Pulse Progress Bar
        self.update_worker({ "msg": "Provide your Site Admin credentials...", "pb_type": "Pulse" })

        # Display Login UI
        self.login = LoginWindow(parent=self)
        self.login.exec_()

        # Wake up
        self.condition.wakeAll()


    def selected_combo_box_value(self, combo_object):
        """
        Helper function to get the selected value of a QComboBox Widget

        Args:
            combo_object:  QComboBox Widget to get the selected value from
        Returns:
            Value of the selected item as a str or None
        """

        selection = str(combo_object.currentText())

        return selection if selection != "" else None


    def selected_list_value(self, list_object):
        """
        Helper function to get the selected value of a QListWidget

        Args:
            list_object:  QListWidget to get the selected value from
        Returns:
            Value of the selected item as a str or None
        """

        try:
            return list_object.currentItem().text()
        except Exception:
            return None

        # For selecting multiple printers...?
        # print([item.text() for item in self.qlist_local_printers.selectedItems()])


    ################################################################################################
    # Main Functions

    def get_local_printers(self, progress_callback, finished_callback, warning_callback):
        """
        Uses the Jamf Binary to collect the locally installed printers.
        Printer details are added to a class object and each object is added to a list.

        Args:
            progress_callback:  A callback function to update the progress and status bars
            finished_callback:  A callback function to update the progress and status bars
            warning_callback:  A callback function to update the progress and status bars
        """

        # Update Status Bar and Pulse Progress Bar
        progress_callback.emit({ 
            "msg": "Querying local printers...", 
            "pb_type": "Pulse" 
        })

        # Create Printer List
        self.local_printer_list = []

        try:

            # Get list of printers using the jamf binary
            results_jamf_list_printer = run_utility("/usr/local/bin/jamf listprinters")

            # Verify success
            if not results_jamf_list_printer.get("success"):
                raise RuntimeError("Jamf binary failed to report installed printers")

        except Exception:

            # Update Status Bar and Pulse Progress Bar
            warning_callback.emit("Error:  Failed to collect the locally installed printers")
            print("ERROR:  Failed to collect the locally install printers")
            print(results_jamf_list_printer.get("stderr"))

        # Remove new lines
        results_jamf_list_printer = re.sub("\n", "", str(results_jamf_list_printer.get("stdout")))

        # Parse the xml
        local_printers = ElementTree.fromstring(results_jamf_list_printer)

        # Get the number of printers and create a counter
        total_printers = len(local_printers.findall("printer"))
        local_count = 0

        # Update Status Bar and Progress Bar
        progress_callback.emit({
            "msg": f"Collecting printer details...  [0/{total_printers}]",
            "total": total_printers,
            "count": local_count
        })

        # Loop through the printers
        for printer in local_printers.findall(".//printer"):

            # Debugging
            # print("Display Name:  "  + printer.find("display_name").text)
            # print("CUPS Name:  " + printer.find("cups_name").text)
            # print("Location:  " + printer.find("location").text)
            # print("Device URI:  " + printer.find("device_uri").text)
            # print("Model:  " + printer.find("model").text)

            # Set the path to the ppd file
            ppd_path = f"/private/etc/cups/ppd/{printer.find('cups_name').text}.ppd"

            # Open the ppd file and read in it's contents
            if os.path.exists(ppd_path):
                with open(ppd_path, "rb") as f:
                    ppd_contents = f.read()

            # Convert from binary
            ppd_contents = ppd_contents.decode()

            # Create Printer Object
            printer_object = Printer(
                display_name = printer.find("display_name").text, 
                cups_name = printer.find("cups_name").text, 
                location = printer.find("location").text, 
                device_uri = printer.find("device_uri").text, 
                model = printer.find("model").text, 
                ppd_path = ppd_path,
                ppd_contents = ppd_contents
            )

            # Add printer object to list
            self.local_printer_list.append(printer_object)

            # Add each item to the QListWidget
            self.qlist_local_printers.addItem(printer_object.display_name)

            local_count = local_count + 1

            # Update Status Bar and Progress Bar
            progress_callback.emit({ 
                "msg": f"Found printer:  {printer_object.display_name}  \
                    [{local_count}/{total_printers}]", 
                "total": total_printers, 
                "count": local_count 
            })

        ##### Loop complete

        # Update Status Bar and Progress Bar
        finished_callback.emit("Querying local printers...  [COMPLETE]")


    def clicked_get_sites(self, progress_callback, finished_callback, warning_callback):
        """
        Handles the "Get Sites" button click.

        Args:
            progress_callback:  A callback function to update the progress and status bars
            finished_callback:  A callback function to update the progress and status bars
            warning_callback:  A callback function to update the progress and status bars
        """

        # If credentials were already supplied, don't prompt again.
        try:

            # Get current epoch time to compare
            if time.time() > self.api_token_results.get("api_token_expires"):
                # API Token Expired
                self.get_site_admin_token()

            # else:
                # API Token is still valid
                # print("Already have a valid API Token")

        except Exception:

            # No API Token
            # Calls self.login_prompt() to display the Ui_LoginWindow QDialog box
            self.displayLoginWindow.prompt.emit()

            # Wait here
            self.mutex.lock()
            self.condition.wait(self.mutex)
            self.mutex.unlock()

        # Update Status Bar
        progress_callback.emit({ "msg": "Requesting API Token..." })

        # Check which button was clicked
        if self.loginWindow_button == "OK":

            try:
                # Verify success
                if self.api_token_results.get("error"):

                    # Update Status Bar and Pulse Progress Bar
                    warning_callback.emit(
                        "ERROR:  Failed to authenticate the provided credentials!")
                    print("ERROR:  Failed to authenticate Site Admin Credentials!")
                    print(f"ERROR:  Return Code {self.api_token_results.get('status')}")
                    print(self.api_token_results.get("error"))
                    return

                # Update Status Bar
                progress_callback.emit({ "msg": "Requesting API Token...  [SUCCESS]" })

                # Update Status Bar
                progress_callback.emit({ "msg": "Collecting Site Access Permissions..." })

                # Get Site Access Function
                self.get_site_access(warning_callback)

                if len(self.site_names) > 1:

                    # Update Status Bar
                    progress_callback.emit({
                        "msg": "Collecting Site Access Permissions...  [SUCCESS]" })

                    # Enable the Site ComboBox, clear it,and add the Site names
                    self.combo_sites.setEnabled(True)
                    self.combo_sites.clear()
                    self.combo_sites.addItems(sorted(self.site_names))

                    # Update Status Bar and Progress Bar
                    finished_callback.emit("Sites populated")

                    # Enable Buttons
                    self.button_get_printers.setEnabled(True)

                else:
                    return

            except Exception:
                pass

        else:
            #  User clicked cancel
            finished_callback.emit("Canceled:  Site Admin credentials not provided")


    def clicked_create_printer(self, progress_callback, finished_callback, warning_callback):
        """
        Handles the Create Printer button click.

        Args:
            progress_callback:  A callback function to update the progress and status bars
            finished_callback:  A callback function to update the progress and status bars
            warning_callback:  A callback function to update the progress and status bars
        """

        # Disable Button so it can't be clicked multiple times
        self.button_create_printers.setEnabled(False)

        # Update Status Bar and Pulse Progress Bar
        progress_callback.emit({
            "msg": "Creating selected printer in Jamf Pro...", 
            "pb_type": "Pulse" 
        })

        # Get the selected values
        selected_site = self.selected_combo_box_value(self.combo_sites)
        selected_local_printer = self.selected_list_value(self.qlist_local_printers)
        print(f"Selected printer to CREATE '{selected_local_printer}' in '{selected_site}'")

        # Ensure both of the required items have a selection
        if selected_site is None or selected_local_printer is None:

            # Update Status Bar and Progress Bar
            finished_callback.emit(
                "You must select a local printer and Site to create a new printer in Jamf Pro.")

            return

        # Loop through the list of printers
        for printer in self.local_printer_list:

            if printer.display_name == selected_local_printer:

                # Build the printer payload xml
                payload = f" \
                    <printer> \
                    <name>{printer.display_name}</name> \
                    <category>Printers</category> \
                    <uri>{printer.device_uri}</uri> \
                    <CUPS_name>{printer.cups_name}</CUPS_name> \
                    <location>{printer.location}</location> \
                    <model>{printer.model}</model> \
                    <ppd>{printer.cups_name}.ppd</ppd> \
                    <ppd_contents>{escape(printer.ppd_contents)}</ppd_contents> \
                    <notes>{{ \"Site\": \"{selected_site}\", \"Created_by\": \
                        \"{self.sa_username}\", \"Updated_by\": \"\"}}</notes> \
                    <ppd_path>{printer.ppd_path}</ppd_path> \
                    </printer>"

                # Setup API Resource and Headers
                api_Resource_Printers_Create = f"{self.jps_url}JSSResource/printers/id/0"
                headers = {
                    "Content-Type": "application/xml", "Authorization": f"Basic {jps_credentials}"}

                try:

                    # POST to create a new printer in the JPS.
                    response_create_printer = requests.post(
                        url = api_Resource_Printers_Create,
                        headers = headers,
                        data = payload.encode("utf-8")
                    )

                    if response_create_printer.status_code == 409:

                        # Update Status Bar and Pulse Progress Bar
                        warning_callback.emit("ERROR:  Printer name already exists in Jamf Pro")
                        print("FAILED to create printer due duplicate name")

                    elif response_create_printer.status_code != 201:

                        # Update Status Bar and Pulse Progress Bar
                        warning_callback.emit(
                            "ERROR:  Failed to create the selected printer in Jamf Pro")
                        print("FAILED to create printer!")
                        print(f"Status Code:  {response_create_printer.status_code}")
                        print(f"URI:  {api_Resource_Printers_Create}")
                        print(response_create_printer.text)

                    else:

                        # Get the Printer ID of the newly created printer
                        response_create_printer_xml = ElementTree.fromstring(
                            response_create_printer.text)
                        printer_id = response_create_printer_xml.find("id").text

                        # Set the number of printers and create a counter
                        self.lookup_count = 0
                        self.total_jps_printers = 1

                        # Get the newly created printer details so that it can be added to the list
                        self.worker_thread(partial(
                            self.get_jps_printer_details, printer_id=printer_id))

                        # Wait here for until printer details are collected
                        self.mutex.lock()
                        self.condition.wait(self.mutex)
                        self.mutex.unlock()

                        # Update Status Bar and Progress Bar
                        finished_callback.emit(
                            "Creating selected printer in Jamf Pro...  [COMPLETE]")

                except Exception:

                    # Update Status Bar and Progress Bar
                    warning_callback.emit("Failed to connect to the Jamf Pro Server.")

        ##### End Loop


    def get_jps_printers(self, progress_callback, finished_callback, warning_callback):
        """
        Handles the Get Printers button click.

        Args:
            progress_callback:  A callback function to update the progress and status bars
            finished_callback:  A callback function to update the progress and status bars
            warning_callback:  A callback function to update the progress and status bars
        """

        # Disable Button so it can't be clicked multiple times
        self.button_get_printers.setEnabled(False)

        # Create a fail set
        self.set_of_printers_that_failed_lookup = set()

        # Update Status Bar and Pulse Progress Bar
        progress_callback.emit({
            "msg": "Fetching list of all printers in Jamf Pro...", 
            "pb_type": "Pulse" 
        })

        # Setup API Resource and Headers
        api_Resource_Printers = f"{self.jps_url}JSSResource/printers"
        headers = {"Accept": "application/xml", "Authorization": f"Basic {jps_credentials}"}

        try:
            # GET all printers from the JPS
            response_get_all_printers = requests.get(url=api_Resource_Printers, headers=headers)

            # Verify response status code
            if response_get_all_printers.status_code != 200:

                # Update Status Bar and Pulse Progress Bar
                warning_callback.emit("ERROR:  Failed to fetch printers from Jamf Pro")
                print("FAILED to get printers!")
                print(f"Status Code:  {response_get_all_printers.status_code}")
                print(response_get_all_printers.text)

                # Enable Buttons
                self.button_get_printers.setEnabled(True)

                return

        except Exception:

            # Update Status Bar and Pulse Progress Bar
            warning_callback.emit("Failed to connect to the Jamf Pro Server.")

            # Enable Buttons
            self.button_get_printers.setEnabled(True)

            return

        # Extract XML response
        all_printers = ElementTree.fromstring(response_get_all_printers.text)

        # Get the number of printers and create a counter
        self.total_jps_printers = all_printers.find("size").text
        self.lookup_count = 0

        # Update Status Bar and Progress Bar
        progress_callback.emit({ 
            "msg": f"Fetching printer details...  [0/{self.total_jps_printers}]", 
            "total": self.total_jps_printers, 
            "count": self.lookup_count 
        })

        # Clear the current list if it exists
        self.jps_printer_list = []

        # Loop through each printer
        for printer in all_printers.findall(".//printer"):

            # Check if the worker should be stopped stopped
            if self.worker.stopped == True:
                print("Exiting from loop")

                # Enable Buttons
                self.button_get_printers.setEnabled(True)

                return

            # Get the Printer ID
            printer_id = printer.find("id").text

            self.run_get_jps_printer_details(printer_id)

        ##### Loop complete

        # Wait here for all printers to be collected
        self.mutex.lock()
        self.condition.wait(self.mutex)
        self.mutex.unlock()

        # Update the Printer ComboBox
        self.populate_printer_combo_box()

        # Clear the fail list set
        self.set_of_printers_that_failed_lookup.clear()

        # Update Status Bar and Progress Bar
        finished_callback.emit("Fetching printer details...  [COMPLETE]")

        # Enable Buttons
        self.button_get_printers.setEnabled(True)


    def get_jps_printer_details(
            self, progress_callback, finished_callback, warning_callback, printer_id):
        """
        Handles the getting individual printer details

        Args:
            progress_callback:  A callback function to update the progress and status bars
            finished_callback:  A callback function to update the progress and status bars
            warning_callback:  A callback function to update the progress and status bars
            printer_id:  The id of a printer object to lookup in the JPS
        """

        # Setup API Resource and Headers
        api_Resource_Printer_ID = f"{self.jps_url}JSSResource/printers/id/{printer_id}"
        headers = { "Accept": "application/xml", "Authorization": f"Basic {jps_credentials}" }

        try:

            # GET printer details from the JPS
            response_get_printer = requests.get(url=api_Resource_Printer_ID, headers=headers)

        except Exception:

            # Update Status Bar and Pulse Progress Bar
            warning_callback.emit("Failed to connect to the Jamf Pro Server.")

            # Increment counter
            self.lookup_count = self.lookup_count + 1

            # Wait until all printers details have been fetched
            if int(self.lookup_count) == int(self.total_jps_printers):

                # Wake Up
                self.condition.wakeAll()

            return

        # Verify response status code
        if response_get_printer.status_code != 200:

            # Attempt to retry getting the printer again
            if printer_id not in self.set_of_printers_that_failed_lookup:

                # Add to set so that we only retry once.
                self.set_of_printers_that_failed_lookup.add(printer_id)

                # Attempt to query the printer again
                self.worker_thread(partial(self.get_jps_printer_details, printer_id=printer_id))

                # Started a new thread for this printer_id; stopping this thread here

            else:

                # Update Status Bar and Pulse Progress Bar
                progress_callback.emit({ 
                    "msg": f"ERROR:  Failed to get a printer from \
                        Jamf Pro  [0/{self.total_jps_printers}]", 
                    "total": self.total_jps_printers, 
                    "count": self.lookup_count 
                })
                print("FAILED to create printer!")
                print(f"Status Code:  {response_get_printer.status_code}")
                print(response_get_printer.text)

            return

        # Extract XML response
        printer_details = ElementTree.fromstring(response_get_printer.text)

        # Doing some hackery to get custom details
        try:
            embedded_json = json.loads(printer_details.find("notes").text)
        except Exception:
            pass

        try:
            site = embedded_json["Site"]
        except Exception:
            site = "unassigned"

        try:
            created_by = embedded_json["Created_by"]
        except Exception:
            created_by = "unknown"

        try:
            updated_by = embedded_json["Updated_by"]
        except Exception:
            updated_by = "unknown"

        # Debugging
        # print("ID:  "  + printer_details.find("id").text)
        # print("Display Name:  "  + printer_details.find("name").text)
        # print("CUPS Name:  " + printer_details.find("CUPS_name").text)
        # print("Location:  " + printer_details.find("location").text)
        # print("Device URI:  " + printer_details.find("uri").text)
        # print("Model:  " + printer_details.find("model").text)
        # print("Notes:  " + printer_details.find("notes").text)
        # print("Site:  " + site)
        # print("Created By:  " + created_by)
        # print("Updated By:  " + updated_by)

        # If the Printer's "assigned Site" is in the list of Sites the 
        # Site Admin has Enroll Permissions to, add it to a list.
        if site in self.site_names:

            # Create Printer Object
            printer_object = Printer( 
                printer_id = printer_details.find("id").text, 
                display_name = printer_details.find("name").text, 
                cups_name = printer_details.find("CUPS_name").text, 
                location = printer_details.find("location").text, 
                device_uri = printer_details.find("uri").text, 
                model = printer_details.find("model").text, 
                ppd_path = printer_details.find("ppd").text, 
                ppd_contents = printer_details.find("ppd_contents").text, 
                site = site, 
                created_by = created_by, 
                updated_by = updated_by )

            # Add printer to list
            self.jps_printer_list.append(printer_object)

        # Increment counter
        self.lookup_count = self.lookup_count + 1

        # Update Status Bar and Progress Bar
        progress_callback.emit({ 
            "msg": f"Fetching printer details...  [{self.lookup_count}/{self.total_jps_printers}]", 
            "total": self.total_jps_printers, 
            "count": self.lookup_count 
        })

        # Wait until all printers details have been fetched
        if int(self.lookup_count) == int(self.total_jps_printers):

            # Wake Up
            self.condition.wakeAll()


    def clicked_update_printer(self, progress_callback, finished_callback, warning_callback):
        """
        Handles the "Update Printer" in JPS button click.

        Args:
            progress_callback:  A callback function to update the progress and status bars
            finished_callback:  A callback function to update the progress and status bars
            warning_callback:  A callback function to update the progress and status bars
        """

        # Disable Buttons
        self.button_update_printer.setEnabled(False)
        self.button_delete_printer.setEnabled(False)

        # Get the selected items
        selected_site = self.selected_combo_box_value(self.combo_sites)
        selected_local_printer = self.selected_list_value(self.qlist_local_printers)
        selected_jps_printer = self.selected_combo_box_value(self.combo_printers)

        print(f"Selected printer to UPDATE '{selected_jps_printer}' in '{selected_site}'")

        # Verify all required items have a selected value
        if selected_site is None or selected_local_printer is None or selected_jps_printer is None:

            # Update Status Bar and Pulse Progress Bar
            finished_callback.emit(
                "You must select matching local and jps printers \
                    to update the printer in Jamf Pro."
            )

            return

        # Update Status Bar and Pulse Progress Bar
        progress_callback.emit({ 
            "msg": f"Updating [{selected_jps_printer}] in Jamf Pro...", 
            "pb_type": "Pulse" 
        })

        # Will need a couple details from the existing printer configuration
        jps_printer = [ 
            printer 
            for printer in self.jps_printer_list 
            if selected_jps_printer == printer.display_name 
        ]

        # Loop through the local printers to find the one that 
        # matches the jps printer that was selected to be updated
        local_printer = [ 
            printer 
            for printer in self.local_printer_list 
            if selected_local_printer == printer.display_name 
        ]

        # Ensure only one printer matched
        if len(local_printer) == len(jps_printer) == 1:

            # Pull objects out of their list
            local_printer = local_printer[0]
            jps_printer = jps_printer[0]

            # Ensure that the display names match on both printer objects
            if local_printer.display_name == jps_printer.display_name:

                # Build the printer payload xml
                payload = f" \
                    <printer> \
                    <id>{jps_printer.printer_id}</id> \
                    <name>{local_printer.display_name}</name> \
                    <category>Printers</category> \
                    <uri>{local_printer.device_uri}</uri> \
                    <CUPS_name>{selected_site}</CUPS_name> \
                    <location>{local_printer.location}</location> \
                    <model>{local_printer.model}</model> \
                    <ppd>{local_printer.cups_name}.ppd</ppd> \
                    <ppd_contents>{escape(local_printer.ppd_contents)}</ppd_contents> \
                    <notes>{{ \"Site\": \"{selected_site}\", \"Created_by\": \
                        \"{jps_printer.created_by}\", \"Updated_by\": \
                        \"{self.sa_username}\"}}</notes> \
                    <ppd_path>{local_printer.ppd_path}</ppd_path> \
                    </printer>"

                # Setup API Resource and Headers
                api_Resource_Printers_Update = f"{self.jps_url}\
                    JSSResource/printers/id/{jps_printer.printer_id}"
                headers = { 
                    "Content-Type": "application/xml", 
                    "Authorization": f"Basic {jps_credentials}" 
                }

                try:

                    # PUT to update a new printer in the JPS.
                    response_update_printer = requests.put(
                        url = api_Resource_Printers_Update, 
                        headers = headers, data = payload.encode("utf-8")
                    )

                    if response_update_printer.status_code != 201:

                        # Update Status Bar and Pulse Progress Bar
                        warning_callback.emit(
                            f"ERROR:  Failed to update [{selected_jps_printer}] in Jamf Pro")
                        print("ERROR:  Failed to update printer!")
                        print(f"Status Code:  {response_update_printer.status_code}")
                        print(f"URI:  {api_Resource_Printers_Update}")
                        print(response_update_printer.text)

                    else:
                        # Update Status Bar and Progress Bar
                        finished_callback.emit(
                            f"Updating [{selected_jps_printer}] in Jamf Pro...  [COMPLETE]"
                        )

                except Exception:
                    # Update Status Bar and Pulse Progress Bar
                    warning_callback.emit("Failed to connect to the Jamf Pro Server.")

            else:
                # Update Status Bar and Pulse Progress Bar
                warning_callback.emit(
                    "You must select matching local and jps printers \
                        to update the printer in Jamf Pro."
                )

        else:
            # Update Status Bar and Pulse Progress Bar
            warning_callback.emit(
                "You must select matching local and jps printers \
                    to update the printer in Jamf Pro."
            )


    def clicked_delete_printer(self, progress_callback, finished_callback, warning_callback):
        """
        Handles the "Delete Printer" in JPS button click.

        Args:
            progress_callback:  A callback function to update the progress and status bars
            finished_callback:  A callback function to update the progress and status bars
            warning_callback:  A callback function to update the progress and status bars
        """

        # Disable Buttons
        self.button_delete_printer.setEnabled(False)
        self.button_update_printer.setEnabled(False)

        selected_jps_printer = self.selected_combo_box_value(self.combo_printers)
        print(f"Selected printer to DELETE:  '{selected_jps_printer}'")

        # Update Status Bar and Pulse Progress Bar
        progress_callback.emit({ 
            "msg": f"Deleting [{selected_jps_printer}] in Jamf Pro...", 
            "pb_type": "Pulse" 
        })

        # Will need a couple details from the existing printer configuration
        jps_printer = [ 
            printer 
            for printer in self.jps_printer_list 
            if selected_jps_printer == printer.display_name 
        ]

        # Ensure only one matching object was found
        if len(jps_printer) == 1:

            # Pull object out of its list
            jps_printer = jps_printer[0]

            # Setup API Resource and Headers
            api_Resource_Printers_Delete = f"{self.jps_url}\
                JSSResource/printers/id/{jps_printer.printer_id}"
            headers = { 
                "Content-Type": "application/xml", 
                "Authorization": f"Basic {jps_credentials}" 
            }

            try:

                # PUT to update a new printer in the JPS.
                response_delete_printer = requests.delete(
                    url = api_Resource_Printers_Delete, 
                    headers = headers
                )

                if response_delete_printer.status_code != 200:

                    # Update Status Bar and Pulse Progress Bar
                    warning_callback.emit(
                        f"ERROR:  Failed to delete [{selected_jps_printer}] in Jamf Pro")
                    print("FAILED to delete printer!")
                    print(f"Status Code:  {response_delete_printer.status_code}")
                    print(f"URI:  {api_Resource_Printers_Delete}")
                    print(response_delete_printer.text)

                else:

                    # Remove printer from the list
                    self.jps_printer_list.remove(jps_printer)

                    # Update Status Bar and Progress Bar
                    finished_callback.emit(
                        f"Delete [{selected_jps_printer}] in Jamf Pro...  [COMPLETE]")

            except Exception:

                # Update Status Bar and Pulse Progress Bar
                warning_callback.emit("Failed to connect to the Jamf Pro Server.")

                return
        else:

            # Update Status Bar and Pulse Progress Bar
            warning_callback.emit("There was a problem finding the required printer details.")


    ################################################################################################
    # Main Helpers

    def jamf_pro_url(self):
        """
        Helper function to return the Jamf Pro URL the device is enrolled with
        """

        # Define Variables
        jamf_plist = "/Library/Preferences/com.jamfsoftware.jamf.plist"

        # Get the systems' Jamf Pro Server
        if os.path.exists(jamf_plist):

            with open(jamf_plist, "rb") as jamf_plist:

                jamf_plist_contents = plistlib.load(jamf_plist)
                self.jps_url = jamf_plist_contents.get("jss_url")
                print(f"Jamf Pro Server URL:  {self.jps_url}")

        else:
            print("ERROR:  Missing the Jamf Pro configuration file!")
            sys.exit(1)


    def display_printer_details(self):
        """
        Handles the displaying printer details in the expanded window details view.
        """

        try:
            # Get the object that called this function
            sender = self.sender().objectName()

        except Exception:
            pass

        # Determine which object to get the selected item in that object
        if sender == "qlist_local_printers":

            selected_printer = self.selected_list_value(self.qlist_local_printers)
            printer_list = self.local_printer_list

        elif sender in ( "combo_printers", "combo_sites" ):

            selected_printer = self.selected_combo_box_value(self.combo_printers)
            printer_list = self.jps_printer_list

        else:
            return

        try:
            # Loop through the list to get the printers details
            for printer in printer_list:

                if printer.display_name == selected_printer:

                    self.lineEdit_printer_display_name.setText(printer.display_name)
                    self.lineEdit_printer_location.setText(printer.location)
                    self.lineEdit_printer_model.setText(printer.model)
                    self.lineEdit_printer_device_uri.setText(printer.device_uri)
                    self.lineEdit_printer_cups_name.setText(printer.cups_name)
                    self.lineEdit_printer_ppd_file_path.setText(printer.ppd_path)
                    self.lineEdit_site.setText(printer.site)
                    self.lineEdit_created_by.setText(printer.created_by)
                    self.lineEdit_updated_by.setText(printer.updated_by)
                    self.textEdit_printer_ppd_contents.setText(printer.ppd_contents)

        except Exception:
            print("Failed to display printer details.")


    def get_site_admin_token(self, button, sender_parent):
        """
        A helper function that acquires an API Token data for the submitted credentials.

        Args:
            sender_parent:  The parent object that called this function
        """

        # Get the object that called this function
        self.loginWindow_button = button.text()

        if self.loginWindow_button == "OK":

            # Save credentials
            self.sa_username = sender_parent.lineEdit_username.text()
            self.sa_password = sender_parent.lineEdit_password.text()

            if len( self.sa_username ) and len( self.sa_password ) != 0:

                try:
                    # Create a token based on user provided credentials
                    response_get_token = requests.post(
                        url = f"{self.jps_url}/uapi/auth/tokens", 
                        auth = (self.sa_username, self.sa_password)
                    )

                    # API Token for the Site Admin
                    self.api_token_results = {
                        "success": True if response_get_token.status_code == 200 else False,
                        "error":  response_get_token.text() if 
                            response_get_token.status_code != 200 else None,
                        "status": response_get_token.status_code,
                        "api_token": response_get_token.json()["token"] if 
                            response_get_token.status_code == 200 else None,
                        "api_token_expires": response_get_token.json()["expires"] if 
                            response_get_token.status_code == 200 else None
                    }

                except Exception:
                    self.api_token_results = {
                        "success": False,
                        "error":  "Failed to connect to the Jamf Pro Server.",
                        "status": "404",
                        "api_token": None,
                        "api_token_expires": None
                    }

                # Close the Login Window QDialog Window
                sender_parent.close()

                # else:
                    # print("Credentials were not supplied")
                    # Future plans:  create cue that credentials were not provided

        elif self.loginWindow_button == "Cancel":

            # Close the Login Window QDialog Window
            sender_parent.close()


    def get_site_access(self, warning_callback):
        """
        A helper function that retrieves the Sites an account has Enroll Permissions too.

        Args:
            warning_callback:  A callback function to update the progress and status bars
        """

        # site_ids = []
        self.site_names = [""] # Add an empty value to the beginning
        sites_unauthorized = (
            "Site A",
            "Site 2",
            "Site C3"
        )

        try:
            # Setup API Resource and Headers
            url = f"{self.jps_url}/uapi/auth"
            headers = { "Authorization": f"jamf-token {self.api_token_results['api_token']}" }

            # GET All User Details
            response_user_details = requests.get( url, headers=headers )

        except Exception:
            # Update Status Bar and Pulse Progress Bar
            warning_callback.emit("ERROR:  Failed to connect to the Jamf Pro Server.")
            return

        try:
            # Get the response content from the API
            user_details = response_user_details.json()

            # Old method to limit Sites
            # Uncomment the below lines if you'd want to use this method
            # for key in user_details.get("accountGroups"):
                # for privilege in key.get("privileges"):
                #     if privilege == "Enroll Computers and Mobile Devices":
                # site_ids.append(key.get("siteId"))

            # for key in user_details.get("sites"):
            #     if key.get("id") in site_ids:
            #         self.site_names.append(key.get("name"))

            # New method to limit Sites
            self.site_names.extend(
                key.get("name")
                for key in user_details.get("sites")
                if key.get("name") not in sites_unauthorized
            )

        except Exception:
            pass


    def clear_api_token(self):
        """
        Handles clearing the API Token when the Clear API Token Action is selected
        """

        self.api_token_results = ""


    def populate_printer_combo_box(self):
        """
        Handles updating the JPS Printer ComboBox by repopulating the values when the Site 
        combobox value is changed
        """

        try:

            # Ensure there are JPS Printers before continuing.
            if len(self.jps_printer_list) > 0:

                selected_site = self.selected_combo_box_value(self.combo_sites)

                # List to collect printers that are "assigned" to the selected Site.
                matching_printers = [ 
                    printer.display_name 
                    for printer in self.jps_printer_list 
                    if printer.site == selected_site 
                ]

                # Enable ComboBox and clear its current items
                self.combo_printers.setEnabled(True)
                self.combo_printers.clear()

                # If there were printers for the select Site, add them to the ComboBox Widget
                if len(matching_printers) > 0:

                    self.combo_printers.addItems(sorted(matching_printers))

                # Run the function to update the extended GUI
                self.display_printer_details()

            else:

                # Clear the ComboBoxes current items
                self.combo_printers.clear()

        except Exception:
            pass


    def button_handler(self):
        """
        Handles enabling the Created, Update, and Delete Buttons depending on if local printers
        exist and when the JPS Printer ComboBox has a non-null selected value
        """

        # Create Button
        try:
                        
            # Get the selected values
            selected_site = self.selected_combo_box_value(self.combo_sites)
            selected_local_printer = self.selected_list_value(self.qlist_local_printers)

            if selected_site and selected_local_printer:

                # Local printers exist, enabling button
                self.button_create_printers.setEnabled(True)

            else:

                # Local printers do not exist, disabling button
                self.button_create_printers.setEnabled(False)

        except Exception:
            pass

        # Update and Delete Buttons
        try:

            # Get the current value of the combobox
            selected_printer = self.selected_combo_box_value(self.combo_printers)

            if selected_printer:

                # Printer selected, enabling buttons
                self.button_update_printer.setEnabled(True)
                self.button_delete_printer.setEnabled(True)

            else:

                # Printer is not selected, disabling buttons
                self.button_update_printer.setEnabled(False)
                self.button_delete_printer.setEnabled(False)

        except Exception:
            pass


####################################################################################################
# Classes

class WorkerSignals(QtCore.QObject):
    """
    Defines the signals available from a running worker thread.

    Supported signals are:

    close
        Close a window
    error
        `tuple` (exctype, value, traceback.format_exc() )
    finished
        `str` message to display
    progress
        `dict` message to display and value to update the progress bar
    prompt
        Open the login window
    result
        `object` data returned from processing, anything
    warning
        `str` message to display
    """

    close = QtCore.Signal()
    error = QtCore.Signal(tuple)
    finished = QtCore.Signal(str)
    progress = QtCore.Signal(dict)
    prompt = QtCore.Signal()
    result = QtCore.Signal(object)
    warning = QtCore.Signal(str)


class Worker(QtCore.QRunnable):
    """
    Worker thread

    Inherits from QRunnable to handler worker thread setup, signals and wrap-up.

    :param callback:  The function callback to run on this worker thread. Supplied args and 
                     kwargs will be passed through to the runner.
    :type callback:  function
    :param args:  Arguments to pass to the callback function
    :param kwargs:  Keywords to pass to the callback function
    """

    def __init__(self, function, *args, **kwargs):
        super(Worker, self).__init__()

        # Store constructor arguments (re-used for processing)
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

        # Add the callback to our kwargs
        self.kwargs["progress_callback"] = self.signals.progress
        self.kwargs["finished_callback"] = self.signals.finished
        self.kwargs["warning_callback"] = self.signals.warning


    @QtCore.Slot()
    def run(self):
        """
        Initialise the runner function with passed args, kwargs.
        """

        # Retrieve args/kwargs here; and fire processing using them

        try:

            result = self.function(*self.args, **self.kwargs)

        except Exception:

            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))

        else:

            # Return the result of the processing
            self.signals.result.emit(result)
        # finally:
        #     self.signals.finished.emit()  # Done


class Printer:
    """
    An object to store printer configuration details in
    """
    # Initializer / Instance Attributes
    def __init__(
        self, printer_id="local", ppd_contents="", site="", created_by="", updated_by="", **kwargs
    ):
        self.printer_id = printer_id
        self.display_name = kwargs.get("display_name")
        self.cups_name = kwargs.get("cups_name")
        self.model = kwargs.get("model")
        self.location = kwargs.get("location")
        self.device_uri = kwargs.get("device_uri")
        self.ppd_path = kwargs.get("ppd_path")
        self.ppd_contents = ppd_contents
        self.site = site
        self.created_by = created_by
        self.updated_by = updated_by


    def __repr__(self):
        return str(self.display_name)


    def __str__(self):
        return str(self.display_name)


####################################################################################################
# Utility Helpers

def run_utility(command):
    """
    A helper function for subprocess.

    Args:
        command (str):  The command line level syntax that would be 
                        written in shell or a terminal window.
    Returns:
        Results in a dictionary.
    """

    # Validate that command is not a string
    if not isinstance(command, str):
        raise TypeError("Command must be a str type")

    # Format the command
    command = shlex.split(command)

    # Run the command
    process = subprocess.Popen( 
        command, 
        stdout = subprocess.PIPE, 
        stderr = subprocess.PIPE, 
        shell = False, 
        universal_newlines = True 
    )

    (stdout, stderr) = process.communicate()

    return {
        "stdout": (stdout).strip(),
        "stderr": (stderr).strip() if stderr != None else None,
        "status": process.returncode,
        "success": True if process.returncode == 0 else False
    }


def decrypt_string(key, encrypted_string):
    """
    A helper function to decrypt a string with a given secret key.

    Args:
        key:  Secret key used to decrypt the passed string.  (str)
        string:  String to decrypt. (str)
    Returns:
        The unencrypted string as a str.
    """

    f = Fernet(key.encode())
    decrypted_string = f.decrypt(encrypted_string.encode())

    return decrypted_string.decode()


if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName("Jamf Pro Printer Tool")

    # Grab the arguments passed into the script
    cli_args = app.arguments()
    parser_args = []

    for arg in cli_args[1:]:
        if len(arg) != 0:
            parser_args.extend(arg.split(" ", 1))

    # Setup Arg Parser
    parser = argparse.ArgumentParser(
        description="This script defines a GUI application to create printers within Jamf Pro.  \
           It requires a Jamf Pro account with CRUD permissions to the Printer Object Type.")
    parser.add_argument(
        "--api-username", "-u", 
        help="Provide the encrypted string for the API Username", 
        required=True
    )
    parser.add_argument(
        "--api-password", "-p", 
        help="Provide the encrypted string for the API Password", 
        required=True
    )
    parser.add_argument("--secret", "-s", help="Provide the encrypted secret", required=True)
    args, unknown = parser.parse_known_args(parser_args)

    # Verify the proper arguments were passed
    if args.api_username and args.api_password and args.secret:

        jps_api_user = decrypt_string(args.secret.strip(), args.api_username.strip()).strip()
        jps_api_password = decrypt_string(args.secret.strip(), args.api_password.strip()).strip()
        jps_credentials = (
            base64.b64encode( f"{jps_api_user}:{jps_api_password}".encode() ) ).decode()

    else:

        parser.print_help()
        sys.exit(0)

    # Setup the GUI
    gui = MainWindow()
    app.aboutToQuit.connect(gui.shutdown)

    # Call functions on load
    gui.jamf_pro_url()

    # Set the App Icon URL
    app_icon_url = f"{gui.jps_url}ui/images/settings/Printer.png"

    # Get the App Icon from Jamf Pro
    response_image = requests.get(app_icon_url)

    if response_image.status_code == 200:

        with open("/tmp/Printer.png", "wb") as image_file:
            image_file.write(response_image.content)

        app_icon = "/tmp/Printer.png"

    else:

        # If we're unable to acquire the image from the Jamf Pro server, use a local icon
        app_icon = "/System/Library/CoreServices/CoreTypes.bundle\
            /Contents/Resources/ToolbarCustomizeIcon.icns"

    # Set an icon
    icon = QtGui.QIcon()
    icon.addPixmap(QtGui.QPixmap(app_icon), QtGui.QIcon.Normal, QtGui.QIcon.Off)
    app.setWindowIcon(icon)

    # Call functions on load
    gui.run_get_local_printers()

    # Show the GUI
    gui.show()
    sys.exit(app.exec_())
