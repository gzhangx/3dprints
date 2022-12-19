# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import division
"""
***************************************************************************
*   Copyright (c) 2014-2015-2016-2017 2018 2019 2020 2022 <mario52>       *
*                                                                         *
*   This file is a supplement to the FreeCAD CAx development system.      *
*                                                                         *
*   This program is free software; you can redistribute it and/or modify  *
*   it under the terms of the GNU Lesser General Public License (LGPL)    *
*   as published by the Free Software Foundation; either version 2 of     *
*   the License, or (at your option) any later version.                   *
*   for detail see the LICENCE text file.                                 *
**                                                                       **
*   Use at your own risk. The author assumes no liability for data loss.  *
*              It is advised to backup your data frequently.              *
*             If you do not trust the software do not use it.             *
**                                                                       **
*   This software is distributed in the hope that it will be useful,      *
*   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
*   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
*   GNU Library General Public License for more details.                  *
*                                                                         *
*   You should have received a copy of the GNU Library General Public     *
*   License along with this macro; if not, write to the Free Software     *
*   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  *
*   USA                                                                   *
***************************************************************************
*           WARNING! All changes in this file will be lost and            *  
*                  may cause malfunction of the program                   *
***************************************************************************
"""
#
#OS: Windows 10 (10.0)
#Word size of FreeCAD: 64-bit
#Version: 0.20.27809 (Git)
#Build type: Release
#Python 3.8.12, Qt 5.12.9, Coin 4.0.0, OCC 7.5.3
#Locale: French/Mars (fr_MA)
#
#
__Title__   = "FCSpring_Helix_Variable"
__Author__  = "Mario52"
__Url__     = "http://www.freecadweb.org/index-fr.html"
__Wiki__    = "http://www.freecadweb.org/wiki/index.php?title=Macro_FCSpring_Helix_Variable"
__GitHub__  = "https://gist.github.com/mario52a/68c81c32a0727a693d3a"
__Version__ = "01.18"
__Date__    = "2022/03/16" # YYYY/MM/DD
#
#

import PySide2
from PySide2 import (QtWidgets, QtCore, QtGui)
from PySide2.QtWidgets import (QWidget, QApplication, QSlider, QGraphicsView, QGraphicsScene, QVBoxLayout, QStyle)
from PySide2.QtGui import (QPainter, QColor, QIcon)
#from PySide2.QtSvg import *
from PySide2.QtGui import *
from PySide2.QtCore import *
import WebGui

import os, sys #, time
import Draft, Part, FreeCAD, math, PartGui, FreeCADGui, FreeCAD
from math import sqrt, pi, sin, cos, asin, tan, degrees, radians, sqrt
from FreeCAD import Base
App = FreeCAD

####chrono################
import time
global depart ; depart  = 0.0
global arrivee; arrivee = 0.0
def chrono(switch):    # 0=depart autre=stop
#time.strftime('%X %x %Z')#'15:44:07 12/14/19 Paris, Madrid'
    global depart
    global arrivee
    try:
        if switch == 0:
            depart = time.time()#time.clock()
            App.Console.PrintMessage("Chrono begin   : "+str(time.strftime('%X'))+"\n")
        else:
            arrivee = time.time()#time.clock()
            App.Console.PrintMessage("Chrono end     : "+str(time.strftime('%X'))+"\n")
            parcouru = ((arrivee - depart)/60.0)
            App.Console.PrintError("Time execution : "+str("%.3f" % parcouru)+" min"+"\n\n")
        return parcouru
        FreeCADGui.updateGui()    
    except Exception: None
####chrono################

##path###########################################################################
global path
#path = FreeCAD.ConfigGet("AppHomePath")
#path = FreeCAD.ConfigGet("UserAppData")
#path = "your path"
param = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Macro")# macro path
path = param.GetString("MacroPath","") + "/"                        # macro path
path = path.replace("\\","/")                                       # convert the "\" to "/"
#print( "Path for the icons : " , path )
##path###########################################################################
                                                 
global numberSpires        ;numberSpires         = 10     # number Spires of spring
global rayon               ;rayon                = 20.0   # radius of spring
global pas                 ;pas                  = 15.0   # " ! float " (pas) pitch of spire
global precision           ;precision            = 5.0    # " ! float " 360/precision number points for 1 turn
global typeLine            ;typeLine             = 0      # typeLine 0=BSpline or 1=Wire
global helixS              ;helixS               = 0.0    # tableau
global numberSpiresModified;numberSpiresModified = 1      # number (pas) pitch to modify
global pasSpire            ;pasSpire             = 0      #pas    # (pas) pitch of spire to modify
global radiusS             ;radiusS              = 0.0    # tableau radius to modify
global rayonSpire          ;rayonSpire           = 0      #rayon  # new radius
global affPoint            ;affPoint             = 0      # aff points
global debutAngle          ;debutAngle           = 0      # begin angle rotation
global finAngle            ;finAngle             = 360    # end angle rotation
global modifyAngle         ;modifyAngle          = 0      # interrupteur angle
global radius_2_Cone       ;radius_2_Cone        = rayon  # radius_2_Cone en cas d'helice
global spireConeUne        ;spireConeUne         = 0      # interrupteur cone si une seule spire spireConeUne = 1
global spireConeComp       ;spireConeComp        = 0      # compensation pour cone
global spireReverse        ;spireReverse         = 0      # 0 = sens antihoraire si = 1 sens horaire
global lissageSpire        ;lissageSpire         = 0      # niveau de lissage
global lissageS            ;lissageS             = 0      # tableau
global fichierOpen         ;fichierOpen          = 0      # switch fichier precision
global nomF                ;nomF                 = "Name File" # name file
global points              ;points               = []     # tableau points
global zoom                ;zoom                 = 0      # zoom textEdit
global ressort             ;ressort              = ""

global s                   ;s                    = ""     # resident
global ui                  ;ui                   = ""     # resident
global sel                 ;sel                  = ""     # resident selection

global pointsDirection     ;pointsDirection      = []     # tableau direction
global Direction_Begin     ;Direction_Begin      = 0      # direction tableau 0
global Direction_Distance  ;Direction_Distance   = 0.1    # precision Distance coupure et deplacement
global plr                 ;plr                  = ""     # placement sur selection
global coor_Z              ;coor_Z               = 0.0    # pour calcul placement
global hauteurCylindre     ;hauteurCylindre      = 0.0    # adapter la hauteur du ressort
global vecteurSouris       ;vecteurSouris        = ""     # vecteur Selobserver
global centerFaceOrPoint   ;centerFaceOrPoint    = 0      # centrage de l'axe sur face ou au point souris
global axisSpring          ;axisSpring           = ""     # axe de l'objet pour le ressort
global switchReverse       ;switchReverse        = 0      # switchReverse
global switchAdaptRadius   ;switchAdaptRadius    = 0      # switchAdaptRadius
global selectedCircle      ;selectedCircle       = []     # tableau Circle


#### Configuration begin ################################################
#### NOT MODIFY THE CODE HERE ####
#### for modify : go to : FreeCAD >Menu >Tools >Edit parameters... >BaseApp/Preferences/Macros/FCMmacros/FCInfo ####
##
FreeCAD.ParamGet(u"User parameter:BaseApp/Preferences/Macros/FCMmacros/" + __Title__).SetString(u"Version", __Version__ + " (" + __Date__ + ")")
##
global seTPositionFlyRightLeft  #; seTPositionFlyRightLeft  = 2    # 1 = fly, 2 = RightDock other= LeftDock
seTPositionFlyRightLeft = FreeCAD.ParamGet(u"User parameter:BaseApp/Preferences/Macros/FCMmacros/" + __Title__).GetInt(u"seTPositionFlyRightLeft")
if seTPositionFlyRightLeft == 0: seTPositionFlyRightLeft = 1
FreeCAD.ParamGet(u"User parameter:BaseApp/Preferences/Macros/FCMmacros/" + __Title__).SetInt(u"seTPositionFlyRightLeft", seTPositionFlyRightLeft)                           #*1, 2, other
##
global seTWidgetPosition        #; seTWidgetPosition        = 0   # position the widget Left or Right
seTWidgetPosition = FreeCAD.ParamGet(u"User parameter:BaseApp/Preferences/Macros/FCMmacros/" + __Title__).GetBool(u"seTWidgetPosition")
FreeCAD.ParamGet(u"User parameter:BaseApp/Preferences/Macros/FCMmacros/" + __Title__).SetBool(u"seTWidgetPosition", seTWidgetPosition)                # True or False
##
global switchQFileDialogMint    # special LinuxMint
switchQFileDialogMint = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Macros/FCMmacros/" + __Title__).GetBool("switchQFileDialogMint")
if switchQFileDialogMint == 0:
    FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Macros/FCMmacros/" + __Title__).SetBool("switchQFileDialogMint", switchQFileDialogMint)
try:
    if os.uname()[1] == "mint":
        switchQFileDialogMint = 1
        FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Macros/FCMmacros/" + __Title__).SetBool("switchQFileDialogMint", switchQFileDialogMint)  #*Special Mint
except Exception:
    None
##
global setPathLatestDirectory   #; setPathLatestDirectory   = "C:\ ???"
setPathLatestDirectory = FreeCAD.ParamGet(u"User parameter:BaseApp/Preferences/Macros/FCMmacros/" + __Title__).GetString(u"setPathLatestDirectory")
if setPathLatestDirectory == "": setPathLatestDirectory = path
FreeCAD.ParamGet(u"User parameter:BaseApp/Preferences/Macros/FCMmacros/" + __Title__).SetString(u"setPathLatestDirectory", setPathLatestDirectory)    #*"C:\ ???"
##
#### Configuration end ################################################
##
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

def errorDialog(msg):
    diag = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Critical,u"Error Message",msg )
    diag.setWindowFlags(PySide2.QtCore.Qt.WindowStaysOnTopHint) # PySide #cette fonction met la fenetre en avant
#    diag.setWindowModality(QtCore.Qt.ApplicationModal)         # la fonction a ete desactivee pour favoriser "WindowStaysOnTopHint"
    diag.exec_()

class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        global path
        global numberSpires
        global rayon
        global pas
        global precision
        global typeLine
        global helixS
        global pasSpire
        global radiusS
        global spireReverse
        global nomF
        global zoom
        global sel
        global Direction_Distance
        global seTPositionFlyRightLeft
        global seTWidgetPosition

        self.window = MainWindow
        ####
        if seTPositionFlyRightLeft == 1:
            MainWindow.setObjectName(_fromUtf8(u"MainWindow"))    # volant
#            MainWindow.resize(500, 503)
#            MainWindow.setMinimumSize(QtCore.QSize(500, 503))
            #MainWindow.setMaximumSize(QtCore.QSize(380, 590))
            #MainWindow.move(1300, 120)                           # deplace la fenetre

#        MainWindow.setMinimumSize(QtCore.QSize(250, 600))
#        MainWindow.resize(300, 650)
#        MainWindow.setGeometry(960, 160, 270, 660)
#        MainWindow.setMaximumSize(QtCore.QSize(270, 660))

        self.centralWidget = QtWidgets.QWidget(MainWindow)

        ###################
        grid = QtWidgets.QGridLayout()
        self.centralWidget.setLayout(grid)
        ####
        self.scrollArea = QtWidgets.QScrollArea(self.centralWidget)    # cadre scrollarea contenant le widget GUI
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.scrollArea.setWidgetResizable(True)
        grid.addWidget(self.scrollArea, 0, 0)
        vbox = QtWidgets.QVBoxLayout()
        self.scrollArea.setLayout(vbox)
        ####
        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()          #widget contenant le GUI
        vbox.addWidget(self.scrollAreaWidgetContents_2)
        vbox = QtWidgets.QVBoxLayout()
        self.scrollAreaWidgetContents_2.setLayout(vbox)
        ###################

        self.groupBox0 = QtWidgets.QGroupBox()  #self.centralWidget
        self.groupBox0.setFlat(False)
        self.groupBox_01 = QtWidgets.QGroupBox() #self.groupBox0
        self.groupBox_01.setFlat(False)

        self.DS_Numb_Spires = QtWidgets.QSpinBox()
        self.DS_Numb_Spires.setMinimum(1)
        self.DS_Numb_Spires.setMaximum(9999999)
        self.DS_Numb_Spires.setValue(numberSpires)
        self.DS_Numb_Spires.valueChanged.connect(self.on_DS_Numb_Spires)       #connection doubleSpinBox

        self.DS_Pas_Spring = QtWidgets.QDoubleSpinBox()
        self.DS_Pas_Spring.setDecimals(3)
#        self.DS_Pas_Spring.setMinimum(0.001)
        self.DS_Pas_Spring.setMaximum(9999999.99)
        self.DS_Pas_Spring.setValue(pas)
        self.DS_Pas_Spring.valueChanged.connect(self.on_DS_Pas_Spring)         #connection doubleSpinBox

        self.DS_Radius_Sping = QtWidgets.QDoubleSpinBox()
        self.DS_Radius_Sping.setDecimals(3)
#        self.DS_Radius_Sping.setMinimum(0.001)
        self.DS_Radius_Sping.setMaximum(9999999.99)
        self.DS_Radius_Sping.setValue(rayon)
        self.DS_Radius_Sping.valueChanged.connect(self.on_DS_Radius_Sping)     #connection doubleSpinBox

        self.DS_Precision_Turn = QtWidgets.QSpinBox()
        self.DS_Precision_Turn.setMinimum(1)
        self.DS_Precision_Turn.setMaximum(360)
        self.DS_Precision_Turn.setValue(precision)
        self.DS_Precision_Turn.valueChanged.connect(self.on_DS_Precision_Turn) #connection doubleSpinBox

        self.DS_Radius_2_Cone = QtWidgets.QDoubleSpinBox()
        self.DS_Radius_2_Cone.setEnabled(False)
        self.DS_Radius_2_Cone.setDecimals(3)
        self.DS_Radius_2_Cone.setMaximum(9999999.99)
#        self.DS_Radius_2_Cone.setMinimum(rayon)
        self.DS_Radius_2_Cone.setValue(rayon)
        self.DS_Radius_2_Cone.valueChanged.connect(self.on_DS_Radius_2_Cone)   # connection

        self.CH_Cone = QtWidgets.QCheckBox()
        self.CH_Cone.setEnabled(True)
        self.CH_Cone.clicked.connect(self.on_CH_Cone)                          # connection
        
        self.LAB_Numb_Spires = QtWidgets.QLabel()
        self.LAB_Pas_Spring = QtWidgets.QLabel()
        self.LAB_Radius_Spring = QtWidgets.QLabel()
        self.LAB_Precision_Turn = QtWidgets.QLabel()
        self.LAB_Radius_2_Cone = QtWidgets.QLabel()
        self.LAB_Radius_2_Cone.setVisible(False)

        self.SP_Begin_Angle = QtWidgets.QSpinBox()
        self.SP_Begin_Angle.setEnabled(False)
        self.SP_Begin_Angle.setMinimum(0)
        self.SP_Begin_Angle.setMaximum(360)
        self.SP_Begin_Angle.setValue(0)
        self.SP_Begin_Angle.valueChanged.connect(self.on_SP_Begin_Angle)       # connection

        self.SP_End_Angle = QtWidgets.QSpinBox()
        self.SP_End_Angle.setEnabled(False)
        self.SP_End_Angle.setMinimum(1)
        self.SP_End_Angle.setMaximum(360)
        self.SP_End_Angle.setValue(360)
        self.SP_End_Angle.valueChanged.connect(self.on_SP_End_Angle)           # connection

        self.LAB_Begin_Angle = QtWidgets.QLabel()
        self.LAB_End_Angle = QtWidgets.QLabel()

        self.CB_B_E_Angle = QtWidgets.QCheckBox()
        self.CB_B_E_Angle.clicked.connect(self.on_CB_B_E_Angle)                # connection radioButton

        ####

        self.groupBox_02 = QtWidgets.QGroupBox()

        self.RA_Wire = QtWidgets.QRadioButton()
#        self.RA_Wire.setChecked(True)
        self.RA_Wire.setIcon(QtGui.QIcon.fromTheme("Draft",QtGui.QIcon(":/icons/Draft_Wire.svg")))
        self.RA_Wire.clicked.connect(self.on_RA_Wire)                          #connection radioButton

        self.RA_BSpline = QtWidgets.QRadioButton()
        self.RA_BSpline.setChecked(True)
        self.RA_BSpline.setIcon(QtGui.QIcon.fromTheme("Draft",QtGui.QIcon(":/icons/Draft_BSpline.svg")))
        self.RA_BSpline.clicked.connect(self.on_RA_BSpline)                    #connection radioButton

        self.CH_Points = QtWidgets.QCheckBox()
        self.CH_Points.setEnabled(True)
#        self.CH_Points.setStatusTip(_fromUtf8(""))
        self.CH_Points.setChecked(False)
        self.CH_Points.setIcon(QtGui.QIcon.fromTheme("Draft",QtGui.QIcon(":/icons/Draft_Point.svg")))
        self.CH_Points.clicked.connect(self.on_CH_Points) #

        self.CH_Reverse = QtWidgets.QCheckBox()
        self.CH_Reverse.setEnabled(True)
#        self.CH_Reverse.setStatusTip(_fromUtf8(""))
        self.CH_Reverse.setChecked(False)
        self.CH_Reverse.clicked.connect(self.on_CH_Reverse)                    #
        ####

        self.groupBox_03 = QtWidgets.QGroupBox()

        self.PB_Adapt_Radius = QtWidgets.QPushButton()
        self.PB_Adapt_Radius.setEnabled(False)
        self.PB_Adapt_Radius.clicked.connect(self.on_PB_Adapt_Radius)          #

        self.PB_Center_Point = QtWidgets.QPushButton()
        self.PB_Center_Point.setEnabled(False)
        self.PB_Center_Point.clicked.connect(self.on_PB_Center_Point)          #

        self.CB_Position = QtWidgets.QCheckBox()
        self.CB_Position.setEnabled(False)
        self.CB_Position.clicked.connect(self.on_CB_Position)                  #

        self.PB_CreaCircle = QtWidgets.QPushButton()
        self.PB_CreaCircle.setEnabled(False)
        self.PB_CreaCircle.clicked.connect(self.on_PB_CreaCircle)              #
        ####

        self.groupBox_04 = QtWidgets.QGroupBox()
        self.groupBox_04.setEnabled(False)
        #self.groupBox_04.setCheckable(True)
        #self.groupBox_04.setChecked(False)
        self.groupBox_04.setStyleSheet("background-color: QPalette.Base")      # origin system

        self.PB_Begin_End = QtWidgets.QPushButton()
        self.PB_Begin_End.clicked.connect(self.on_PB_Begin_End)                # connection

        self.PB_Reverse_Spr = QtWidgets.QPushButton()
        self.PB_Reverse_Spr.clicked.connect(self.on_PB_Reverse_Spr)            # connection

        self.DS_horizontalSlider = QtWidgets.QDoubleSpinBox()
        self.DS_horizontalSlider.setDecimals(1)
        self.DS_horizontalSlider.setMinimum(0)
        self.DS_horizontalSlider.setMaximum(9999999999.0)
        self.DS_horizontalSlider.setValue(0)
        self.DS_horizontalSlider.setSingleStep(Direction_Distance)
        self.DS_horizontalSlider.stepUp()
        #self.DS_horizontalSlider.stepDown()
        self.DS_horizontalSlider.valueChanged.connect(self.on_DS_horizontalSlider) #connection doubleSpinBox

        self.PB_Reverse_Com = QtWidgets.QPushButton()
        self.PB_Reverse_Com.clicked.connect(self.on_PB_Reverse_Com)

        self.horizontalSlider = QtWidgets.QSlider()
        self.horizontalSlider.setMaximum(100)
        self.horizontalSlider.setMinimum(0)
        self.horizontalSlider.setSliderPosition(0)
        self.horizontalSlider.setSingleStep(Direction_Distance)
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.valueChanged.connect(self.on_horizontal_slider)  # connection
        ####

        self.groupBox_05 = QtWidgets.QGroupBox()
        self.groupBox_05.setCheckable(False)
        self.groupBox_05.setChecked(False)

        self.SP_Numbering_Spire = QtWidgets.QSpinBox()
        self.SP_Numbering_Spire.setMinimum(1)
        self.SP_Numbering_Spire.setMaximum(numberSpires)
        self.SP_Numbering_Spire.setPrefix("Num: ")
        self.SP_Numbering_Spire.valueChanged.connect(self.on_S_Numbering_Spire) #connection SpinBox

        self.CH_Smooting = QtWidgets.QCheckBox()
        self.CH_Smooting.setEnabled(True)

        self.CH_Smooting.clicked.connect(self.on_CH_Smooting)                  # connection
        
        self.SP_Lissage = QtWidgets.QSpinBox()
        self.SP_Lissage.setVisible(False)
        self.SP_Lissage.setMinimum(0)
        self.SP_Lissage.setMaximum(int(360/precision)-1)
        self.SP_Lissage.valueChanged.connect(self.on_S_Lissage)                #connection SpinBox

        self.DS_Pas_Spire = QtWidgets.QDoubleSpinBox()
        self.DS_Pas_Spire.setValue(0) #pas
        self.DS_Pas_Spire.setDecimals(3)
        self.DS_Pas_Spire.setMaximum(9999999.99)
        self.DS_Pas_Spire.valueChanged.connect(self.on_DS_Pas_Spire)           #connection doubleSpinBox

        self.PU_To_Pas = QtWidgets.QPushButton()
        self.PU_To_Pas.clicked.connect(self.on_PU_To_Pas)                      # connection

        self.DS_Radius_Spire = QtWidgets.QDoubleSpinBox()
        self.DS_Radius_Spire.setDecimals(3)
        self.DS_Radius_Spire.setValue(0) #rayon
#        self.DS_Radius_Spire.setMinimum(0.001)
        self.DS_Radius_Spire.setMaximum(9999999.99)
        self.DS_Radius_Spire.valueChanged.connect(self.on_DS_Radius_Spire)     # connection doubleSpinBox

        self.PU_To_Radius = QtWidgets.QPushButton()
        self.PU_To_Radius.clicked.connect(self.on_PU_To_Radius)                # connection

#        section progressBar 1
        self.PBA_progressBar = QtWidgets.QProgressBar()
        self.PBA_progressBar.setCursor(QtCore.Qt.WaitCursor)
        self.PBA_progressBar.setValue(0)
        self.PBA_progressBar.setVisible(False)
        self.PBA_progressBar.setOrientation(QtCore.Qt.Horizontal)
        self.PBA_progressBar.setAlignment(QtCore.Qt.AlignCenter)

        self.LAB_Numbering_Spire = QtWidgets.QLabel()
        self.LAB_Pas_Spire = QtWidgets.QLabel()
        self.LAB_Radius_Spire = QtWidgets.QLabel()

        self.PU_Accept_Value = QtWidgets.QPushButton()
        self.PU_Accept_Value.setIcon(QIcon(QApplication.style().standardIcon(QStyle.SP_DialogApplyButton))) #
        self.PU_Accept_Value.clicked.connect(self.on_PU_Accept_Value)          # connection

        self.PB_Clear = QtWidgets.QPushButton()
        self.PB_Clear.setIcon(QIcon(QApplication.style().standardIcon(QStyle.SP_DialogResetButton))) #
        self.PB_Clear.clicked.connect(self.on_PB_Clear)                        # connection

        self.PB_Zoom = QtWidgets.QPushButton()
        self.PB_Zoom.setIcon(QIcon(QApplication.style().standardIcon(QStyle.SP_FileDialogContentsView))) #
        self.PB_Zoom.clicked.connect(self.on_PB_Zoom)                          # connection

        self.textEdit = QtWidgets.QTextEdit()
        self.textEdit.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)

        ####
        self.groupBox_06 = QtWidgets.QGroupBox()

        #self.label_11_Name = QtWidgets.QLabel()

        self.PU_Read = QtWidgets.QPushButton()
        self.image_02 = path+"FCSpring_Helix_Variable_Icon_02.png"                          # image
        icon02 = QtGui.QIcon()                                                              #
        icon02.addPixmap(QtGui.QPixmap(self.image_02),QtGui.QIcon.Normal, QtGui.QIcon.Off)  #
        self.PU_Read.setIcon(icon02)                                                        #
        self.PU_Read.clicked.connect(self.on_PU_Read)                          # connection

        self.PU_Save = QtWidgets.QPushButton()
        self.image_03 = path+"FCSpring_Helix_Variable_Icon_03.png"                          # image
        icon03 = QtGui.QIcon()                                                              #
        icon03.addPixmap(QtGui.QPixmap(self.image_03),QtGui.QIcon.Normal, QtGui.QIcon.Off)  #
        self.PU_Save.setIcon(icon03)                                                        #
        self.PU_Save.clicked.connect(self.on_PU_Save)

        self.PU_Read_Coord = QtWidgets.QPushButton()
        self.PU_Read_Coord.setEnabled(True)
        self.image_02b = path+"FCSpring_Helix_Variable_Icon_02b.png"                         # image
        icon02b = QtGui.QIcon()                                                              #
        icon02b.addPixmap(QtGui.QPixmap(self.image_02b),QtGui.QIcon.Normal, QtGui.QIcon.Off) #
        self.PU_Read_Coord.setIcon(icon02b)                                                  #
        self.PU_Read_Coord.clicked.connect(self.on_PU_Read_Coord)              # connection

        self.PU_Save_Coord = QtWidgets.QPushButton()
        self.image_03b = path+"FCSpring_Helix_Variable_Icon_03b.png"                         # image
        icon03b = QtGui.QIcon()                                                              #
        icon03b.addPixmap(QtGui.QPixmap(self.image_03b),QtGui.QIcon.Normal, QtGui.QIcon.Off) #
        self.PU_Save_Coord.setIcon(icon03b)                                                  #
        self.PU_Save_Coord.clicked.connect(self.on_PU_Save_Coord)              # connection
        ####
        self.CB_05_Position = QtWidgets.QCheckBox()
        if seTPositionFlyRightLeft == 1:
            self.CB_05_Position.setVisible(False)
        self.CB_05_Position.setChecked(seTWidgetPosition)
        self.CB_05_Position.clicked.connect(self.on_CB_05_Position)            #connection checkBox

        self.PU_Quit = QtWidgets.QPushButton()
        self.image_04 = path+"FCSpring_Helix_Variable_Icon_04.png"                          # image
        icon04 = QtGui.QIcon()                                                              #
        icon04.addPixmap(QtGui.QPixmap(self.image_04),QtGui.QIcon.Normal, QtGui.QIcon.Off)  #
        self.PU_Quit.setIcon(icon04)                                                        #
        self.PU_Quit.clicked.connect(self.on_PU_Quit)                          # connection

        self.PU_Reset = QtWidgets.QPushButton()
        self.image_05 = path+"FCSpring_Helix_Variable_Icon_05.png"                          # image
        icon05 = QtGui.QIcon()                                                              #
        icon05.addPixmap(QtGui.QPixmap(self.image_05),QtGui.QIcon.Normal, QtGui.QIcon.Off)  #
        self.PU_Reset.setIcon(icon05)                                                       #
        self.PU_Reset.clicked.connect(self.on_PU_Reset)                        # connection

        self.PU_Launch = QtWidgets.QPushButton()
        self.PU_Launch.setIcon(QIcon(QApplication.style().standardIcon(QStyle.SP_DialogOkButton))) #
        self.PU_Launch.clicked.connect(self.on_PU_Launch)                      # connection

        self.PU_Help = QtWidgets.QPushButton()
        self.PU_Help.setIcon(QIcon(QApplication.style().standardIcon(QStyle.SP_MessageBoxQuestion))) # image
        self.PU_Help.clicked.connect(self.on_PU_Help)                          # connection
        
        #### Layout debut ########################
        self.grid0 = QtWidgets.QGridLayout() #self.centralWidget
        self.grid0.setContentsMargins(10, 10, 10, 10)
        self.grid0.addWidget(self.groupBox0, 0, 0, 1, 1)
        ####
        self.grid_00 = QtWidgets.QGridLayout(self.groupBox0)
        #self.grid_00.setContentsMargins(10, 10, 10, 10)
        self.grid_00.addWidget(self.groupBox_01, 0, 0, 1, 1)
        vbox.addWidget(self.groupBox0)      # englobe le cadre principal (titre + date)
        ####
        self.grid_01 = QtWidgets.QGridLayout(self.groupBox_01)
        #self.grid_01.setContentsMargins(10, 10, 10, 10)
        self.grid_01.addWidget(self.DS_Numb_Spires, 0, 0, 1, 1)
        self.grid_01.addWidget(self.LAB_Numb_Spires, 0, 1, 1, 1)
        self.grid_01.addWidget(self.DS_Pas_Spring, 0, 2, 1, 1)
        self.grid_01.addWidget(self.LAB_Pas_Spring, 0, 3, 1, 1)
        self.grid_01.addWidget(self.DS_Radius_Sping, 2, 0, 1, 1)
        self.grid_01.addWidget(self.LAB_Radius_Spring, 2, 1, 1, 2)
        self.grid_01.addWidget(self.DS_Precision_Turn, 2, 2, 1, 1)
        self.grid_01.addWidget(self.LAB_Precision_Turn, 2, 3, 1, 1)
        self.grid_01.addWidget(self.DS_Radius_2_Cone, 4, 0, 1, 1)
        self.grid_01.addWidget(self.CH_Cone, 4, 1, 1, 1)
        self.grid_01.addWidget(self.LAB_Radius_2_Cone, 4, 2, 1, 1)
        self.grid_01.addWidget(self.SP_Begin_Angle, 5, 0, 1, 1)
        self.grid_01.addWidget(self.LAB_Begin_Angle, 5, 1, 1, 1)
        self.grid_01.addWidget(self.SP_End_Angle, 5, 2, 1, 1)
        self.grid_01.addWidget(self.LAB_End_Angle, 5, 3, 1, 1)
        self.grid_01.addWidget(self.CB_B_E_Angle, 4, 2, 1, 1)
        ####
        self.grid_00.addWidget(self.groupBox_02, 1, 0, 1, 1)
        self.grid_02 = QtWidgets.QGridLayout(self.groupBox_02)
        #self.grid_02.setContentsMargins(10, 10, 10, 10)
        self.grid_02.addWidget(self.RA_BSpline, 0, 0, 1, 1)
        self.grid_02.addWidget(self.RA_Wire, 0, 1, 1, 1)
        self.grid_02.addWidget(self.CH_Points, 0, 2, 1, 1)
        self.grid_02.addWidget(self.CH_Reverse, 0, 3, 1, 1)
        ####
        self.grid_00.addWidget(self.groupBox_03, 2, 0, 1, 1)
        self.grid_03 = QtWidgets.QGridLayout(self.groupBox_03)
        #self.grid_03.setContentsMargins(10, 10, 10, 10)
        self.grid_03.addWidget(self.PB_Adapt_Radius, 0, 0, 1, 1)
        self.grid_03.addWidget(self.PB_Center_Point, 0, 1, 1, 1)
        self.grid_03.addWidget(self.CB_Position, 0, 2, 1, 1)
        self.grid_03.addWidget(self.PB_CreaCircle, 0, 3, 1, 1)
        ####☺
        self.grid_00.addWidget(self.groupBox_04, 3, 0, 1, 1)
        self.grid_04 = QtWidgets.QGridLayout(self.groupBox_04)
        #self.grid_04.setContentsMargins(10, 10, 10, 10)
        self.grid_04.addWidget(self.PB_Begin_End, 0, 0, 1, 1)
        self.grid_04.addWidget(self.PB_Reverse_Spr, 0, 1, 1, 1)
        self.grid_04.addWidget(self.DS_horizontalSlider, 0, 2, 1, 1)
        self.grid_04.addWidget(self.PB_Reverse_Com, 0, 3, 1, 1)
        self.grid_04.addWidget(self.horizontalSlider, 1, 0, 1, 4)
        ####
        self.grid_00.addWidget(self.groupBox_05, 4, 0, 1, 1)
        self.grid_05 = QtWidgets.QGridLayout(self.groupBox_05)
        #self.grid_05.setContentsMargins(10, 10, 10, 10)
        self.grid_05.addWidget(self.SP_Numbering_Spire, 0, 0, 1, 1)
        self.grid_05.addWidget(self.LAB_Numbering_Spire, 0, 1, 1, 1)
        self.grid_05.addWidget(self.SP_Lissage, 0, 3, 1, 1)
        self.grid_05.addWidget(self.CH_Smooting, 0, 3, 1, 1)
        self.grid_05.addWidget(self.DS_Pas_Spire, 1, 0, 1, 1)
        self.grid_05.addWidget(self.LAB_Pas_Spire, 1, 1, 1, 1)
        self.grid_05.addWidget(self.PU_To_Pas, 1, 3, 1, 1)
        self.grid_05.addWidget(self.DS_Radius_Spire, 2, 0, 1, 1)
        self.grid_05.addWidget(self.LAB_Radius_Spire, 2, 1, 1, 1)
        self.grid_05.addWidget(self.PU_To_Radius, 2, 3, 1, 1)
        ####
        self.grid_05.addWidget(self.PU_Accept_Value, 3, 0, 1, 4)
        self.grid_05.addWidget(self.PBA_progressBar, 4, 0, 1, 4)
        self.grid_05.addWidget(self.textEdit, 5, 0, 2, 3)
        self.grid_05.addWidget(self.PB_Clear, 5, 3, 1, 1)
        self.grid_05.addWidget(self.PB_Zoom,6 ,3, 1, 1)
        ####
        self.grid_00.addWidget(self.groupBox_06, 5, 0, 1, 1)
        self.grid_06 = QtWidgets.QGridLayout(self.groupBox_06)
        #self.grid_06.setContentsMargins(10, 10, 10, 10)
        self.grid_06.addWidget(self.PU_Read, 0, 0, 1, 2)
        self.grid_06.addWidget(self.PU_Save, 0, 2, 1, 2)
        self.grid_06.addWidget(self.PU_Read_Coord, 1, 0, 1, 2)
        self.grid_06.addWidget(self.PU_Save_Coord, 1, 2, 1, 2)
        ##
        self.grid_06.addWidget(self.CB_05_Position, 2, 0)
        ##
        self.grid_06.addWidget(self.PU_Quit, 3, 0, 1, 1)
        self.grid_06.addWidget(self.PU_Reset, 3, 1, 1, 1)
        self.grid_06.addWidget(self.PU_Launch,3, 2, 1, 1)
        self.grid_06.addWidget(self.PU_Help, 3, 3, 1, 1)
        #### GridLayout fin

        ###########################################################scrollArea
        self.scrollArea.setWidget(self.scrollAreaWidgetContents_2)
        ###########################################################scrollArea

        if seTPositionFlyRightLeft == 1:                                                 # 1=MainWindow separate
            MainWindow.setWindowTitle(__Title__  + u" rmu (" + __Version__ + ") (" + __Date__ + ")")
            MainWindow.setCentralWidget(self.centralWidget)
            #MainWindow.move(1000, 120)                           # deplace la fenetre
        else:
            MainWindow.setWindowTitle(__Title__  + u" rmu (" + __Version__ + ") (" + __Date__ + ")")
            MainWindow.setWidget(self.centralWidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        global sel
        MainWindow.setWindowFlags(PySide2.QtCore.Qt.WindowStaysOnTopHint)     # PySide cette fonction met la fenetre en avant

        MainWindow.setWindowIcon(QtGui.QIcon(path+'FCSpring_Helix_Variable.png'))# change l'icone de la fenetre principale
        MainWindow.setWindowTitle("FCSpring Helix Variable")
####
        self.groupBox0.setTitle("ver : " + __Version__ + " : " + __Date__ + " (rmu)" )
        self.groupBox_01.setTitle(_fromUtf8("Configure"))
        self.DS_Numb_Spires.setToolTip(_fromUtf8("Number total of coil of the spring"))
        self.DS_Numb_Spires.setSuffix(" coils")
        self.LAB_Numb_Spires.setText(_fromUtf8("Number of coil"))
        self.LAB_Numb_Spires.setToolTip(_fromUtf8("Number total of coil of the spring"))
        self.LAB_Pas_Spring.setText(_fromUtf8("Pitch of spring"))
        self.LAB_Pas_Spring.setToolTip(_fromUtf8("Pitch of spring (distance between two vertices)"))
        self.DS_Pas_Spring.setToolTip(_fromUtf8("Pitch of spring (distance between two vertices)"))
        self.DS_Pas_Spring.setSuffix(" mm")
        self.DS_Radius_Sping.setToolTip(_fromUtf8("Radius of spring"))
        self.DS_Radius_Sping.setSuffix(" mm")
        self.LAB_Radius_Spring.setText(_fromUtf8("Radius of spring"))
        self.LAB_Radius_Spring.setToolTip(_fromUtf8("Radius of spring"))
        self.DS_Precision_Turn.setSuffix("  ( " + str(int(360/precision)) + " points )")
        self.DS_Precision_Turn.setToolTip(_fromUtf8("Precision for the line (points = (360/precision))"+"\n"+
                                                    "Actual: " + str(int(360/precision)) + " points for 1 turn"+"\n"+
                                                    "Loading a file or angle checked the value displayd change color in blue just to inform"))
        self.LAB_Precision_Turn.setText(_fromUtf8("Precision"))
        self.LAB_Precision_Turn.setToolTip(_fromUtf8("The precision is the number point (360/precision) for create one turn of the spring"+"\n"+
                                          "Loading a file or angle checked the value displayed change color in blue just to inform"))
        self.DS_Radius_2_Cone.setToolTip(_fromUtf8("Radius for make a cone"+"\n"+
                                                   "This radius is always greater than the principal radius"))
        self.DS_Radius_2_Cone.setSuffix(" mm")
        self.CH_Cone.setText(_fromUtf8("Spring conical"))
        self.CH_Cone.setToolTip(_fromUtf8("Check for create one conical helix"))
        self.LAB_Radius_2_Cone.setText(_fromUtf8("Radius 2 of the cone"))
        self.SP_Begin_Angle.setToolTip(_fromUtf8("Begin angle first coil"))
        self.SP_Begin_Angle.setSuffix(_fromUtf8(" deg"))
        self.LAB_Begin_Angle.setText(_fromUtf8("Begin"))
        self.SP_End_Angle.setToolTip(_fromUtf8("End angle ultimate coil"))
        self.SP_End_Angle.setStatusTip(_fromUtf8("End angle to ultimate coil"))
        self.SP_End_Angle.setSuffix(_fromUtf8(" deg"))
        self.LAB_End_Angle.setText(_fromUtf8("End"))
        self.CB_B_E_Angle.setText(_fromUtf8("Angles")) #Beg/End
        self.CB_B_E_Angle.setToolTip(_fromUtf8("Check the option modify to begin and ultimate angle of coils"+"\n"+
                                               "The final result depend on the level of precision given"+"\n"+
                                               "Optimal : 1 , Precision = 360 points (1 point by degree)"))
#####
        self.groupBox_02.setTitle(_fromUtf8("Type line"))
        self.RA_BSpline.setToolTip(_fromUtf8("Type line BSpline"))
        self.RA_BSpline.setText(_fromUtf8("BSpline"))
        self.RA_Wire.setText(_fromUtf8("Wire"))
        self.RA_Wire.setToolTip(_fromUtf8("Type line Wire"))
        self.CH_Points.setToolTip(_fromUtf8("Check to create points to alls nodes of the precision of turn"))
        self.CH_Points.setText(_fromUtf8("Points"))
        self.CH_Reverse.setToolTip(_fromUtf8("Check to create spring clockwise direction"))
        self.CH_Reverse.setText(_fromUtf8("Reverse"))
#####
        self.groupBox_03.setTitle(_fromUtf8("Options"))
        self.PB_Adapt_Radius.setText(_fromUtf8("Normal")) #AdpRa
        self.PB_Adapt_Radius.setToolTip(_fromUtf8("Mode normal"+"\n"+
                                                  ""+"\n"+
                                                  "For create the spring to the circle radius selected:"+"\n"+
                                                  "1: configure the complete spring"+"\n"+
                                                  "2: select the circle, arc ... to work"+"\n"+
                                                  "  (are detected : Circle, Arc, Ellipse, Sphere, Toroid, Cone, Ellipse (minor radius))"+"\n"+ 
                                                  "3: push this mode Normal button (it change to Adapt Rad.)"+"\n"+
                                                  "4: push the Launch button"))#adapt radius
        self.PB_Center_Point.setText(_fromUtf8("Point Mouse")) #CFace
        self.PB_Center_Point.setToolTip(_fromUtf8("Create Spring to the point mouse (Default)"+"\n"+
                                                  ""+"\n"+
                                                  "For create the spring to center face:"+"\n"+
                                                  "1: configure the complete spring"+"\n"+
                                                  "2: select the face to work"+"\n"+
                                                  "3: push this Point Mouse button (it change to Center Face)"+"\n"+
                                                  "4: push the Launch button"))#center face
        self.CB_Position.setText(_fromUtf8("Position"))
        self.CB_Position.setToolTip(_fromUtf8("Move the position of the spring selected along the axis selected  "+"\n"+
                                              ""+"\n"+
                                              "For use this option:"+"\n"+
                                              "1: select the axis to work"+"\n"+
                                              "2: select the spring to move (or object)"+"\n"+
                                              "This command not verify the objects selected  "
                                              "(Give always the number selection)"+"\n"))
        self.CB_Position.setText(_fromUtf8("Position"))
        self.PB_CreaCircle.setText(_fromUtf8("Circle"))
        self.PB_CreaCircle.setToolTip(_fromUtf8("Create a circle on 3 points selected  "+"\n"+
                                                "First select tree points  "+"\n"))
#####
        self.groupBox_04.setTitle(_fromUtf8("Position ( " + str(len(sel)) + " )"))
        self.groupBox_04.setToolTip(_fromUtf8("Position (number selection) number of points"))
        self.PB_Begin_End.setToolTip(_fromUtf8("Align the spring to begin , end or center axis "+"\n"))
        self.PB_Begin_End.setText(_fromUtf8("Begin / End"))
        self.PB_Reverse_Spr.setText(_fromUtf8("Reverse Spr."))
        self.PB_Reverse_Spr.setToolTip(_fromUtf8("Reverse the spring on its axis "+"\n"))
        self.DS_horizontalSlider.setToolTip(_fromUtf8("Placement spring along the axis"+"\n"))
        self.DS_horizontalSlider.setSuffix(" mm")
        self.PB_Reverse_Com.setText(_fromUtf8("Reverse Count."))
        self.PB_Reverse_Com.setToolTip(_fromUtf8("Reverse the counter of the spring on its axis "+"\n"))
#####
        self.groupBox_05.setTitle(_fromUtf8("Coil special dimension"))
        self.groupBox_05.setToolTip(_fromUtf8("This section allows you to adjust the distance from the coil named. EX: 1 spire = 2 mm"))
        self.SP_Numbering_Spire.setToolTip(_fromUtf8("Numbering of coil for 1 to max = Number of coil ("+str(numberSpires)+")"))
        self.LAB_Numbering_Spire.setToolTip(_fromUtf8("Numbering of coil for 1 to max =  Number of coil"))
        self.LAB_Numbering_Spire.setText(_fromUtf8("Number of coil"))
        self.SP_Lissage.setToolTip(_fromUtf8("Smoothing the line if the difference between two coils"+"\n"+
                                            "The maximum value is egual of the precision number point given -1 (" + str(int(360/precision)-1)+")"+"\n"+
                                            "The finish and precision are influenced by this value"+"\n"+
                                            "PS: The result can be satisfying or completely wrong (prototype state)"))
        self.CH_Smooting.setText(_fromUtf8("Smooting"))
        self.CH_Smooting.setToolTip(_fromUtf8("Smoothing the line if the difference between two coils"+"\n"+
                                              "The maximum value is egual of the precision number point given -1 (" + str(int(360/precision)-1)+")"+"\n"+
                                              "The finish and precision are influenced by this value"+"\n"+
                                              "PS: The result can be satisfying or completely wrong (prototype state)"))
        self.DS_Pas_Spire.setToolTip(_fromUtf8("Pitch of the coil (The pitch is the distance betwen 2 vertices)"))
        self.DS_Pas_Spire.setSuffix(" mm")
        self.LAB_Pas_Spire.setToolTip(_fromUtf8("Pitch of the coil (The pitch is the distance betwen 2 vertices)"))
        self.LAB_Pas_Spire.setText(_fromUtf8("Pitch of coil"))
        self.PU_To_Pas.setText(str(pas) + " mm")
        self.PU_To_Pas.setToolTip(_fromUtf8("Align the value to pitch global configured"))
        self.DS_Radius_Spire.setToolTip(_fromUtf8("Radius of coil "))
        self.DS_Radius_Spire.setSuffix(" mm")
        self.PU_To_Radius.setText(str(rayon) + " mm")
        self.PU_To_Radius.setToolTip(_fromUtf8("Align the value to radius global configured"))
        self.LAB_Radius_Spire.setToolTip(_fromUtf8("Radius of coil "))
        self.LAB_Radius_Spire.setText(_fromUtf8("Radius of coil"))
        #self.PBA_progressBar.setToolTip(_fromUtf8(" "))
        self.PU_Accept_Value.setText(_fromUtf8("Accept the value modified"))
        self.PU_Accept_Value.setToolTip(_fromUtf8("Accept the value for the coil "))
        self.PB_Clear.setText(_fromUtf8("Clear"))
        self.PB_Clear.setToolTip(_fromUtf8("Clear text edit"))
        self.PB_Zoom.setText(_fromUtf8("Zoom"))
        self.PB_Zoom.setToolTip(_fromUtf8("Zoom the text edit window"))
        self.textEdit.setText(_fromUtf8(""))
        self.textEdit.setToolTip(_fromUtf8("List alls modification of coil "))
####
        self.groupBox_06.setTitle(_fromUtf8("Command"))
        self.groupBox_06.setToolTip(_fromUtf8("Menu command"))
        self.PU_Read.setText(_fromUtf8("Load"))
        self.PU_Read.setToolTip(_fromUtf8("Read the file "))
        self.PU_Save.setText(_fromUtf8("Save"))
        self.PU_Save.setToolTip(_fromUtf8("Save the file"))
        self.PU_Read_Coord.setText(_fromUtf8("Load coordinates"))
        self.PU_Read_Coord.setToolTip(_fromUtf8("Load the coordinates file "))
        self.PU_Save_Coord.setText(_fromUtf8("Save coordinates"))
        self.PU_Save_Coord.setToolTip(_fromUtf8("Save the coordinates file "))
        ##
        self.CB_05_Position.setText(u"Left/Right")
        self.CB_05_Position.setToolTip(u"Change the window macro position Right of Left")
        ##
        self.PU_Quit.setText(_fromUtf8("Quit"))
        self.PU_Quit.setToolTip(_fromUtf8("Quit the macro"))
        self.PU_Reset.setText(_fromUtf8("Reset"))
        self.PU_Reset.setToolTip(_fromUtf8("Reset complete the data "))
        self.PU_Launch.setText(_fromUtf8("Launch "))
        self.PU_Launch.setToolTip(_fromUtf8("Launch the macro and create the spring"))
        self.PU_Help.setText(_fromUtf8("Help "))
        self.PU_Help.setToolTip(_fromUtf8("Dislay the wiki page in the FreeCAD browser"))
####
    def on_PU_Reset(self, zero = 0):                                           # Reset 0=Reset total 1=Reset mise a jour
        global numberSpires
        global rayon
        global pas
        global precision
        global typeLine
        global affPoint
        global helixS
        global numberSpiresModified
        global pasSpire
        global radiusS
        global rayonSpire
        global affPoint
        global debutAngle
        global finAngle
        global modifyAngle
        global radius_2_Cone
        global spireConeUne
        global spireConeComp
        global spireReverse
        global lissageSpire
        global lissageS
        global fichierOpen
        global nomF
        global zoom
        global pointsDirection
        global Direction_Begin
        global plr
        global sel
        global switchAdaptRadius
        global centerFaceOrPoint
        global selectedCircle

        if zero == 0:                                                          # 0 = Reset total
            numberSpires         = 10
            rayon                = 20.0
            pas                  = 15.0
            precision            = 5.0
            typeLine             = 0
            affPoint             = 0
            helixS               = 0.0
            radiusS              = 0.0
            numberSpiresModified = 1
            pasSpire             = 0 #pas
            rayonSpire           = 0 #rayon
            modifyAngle          = 0
            radius_2_Cone        = rayon
            fichierOpen          = 0
            nomF                 = "Name File"

        self.DS_Numb_Spires.setValue(numberSpires)
        self.DS_Radius_Sping.setValue(rayon)
        self.DS_Pas_Spring.setValue(pas)
        self.DS_Precision_Turn.setValue(precision)
        self.DS_Precision_Turn.setEnabled(True)
        self.DS_Precision_Turn.setToolTip(_fromUtf8("Precision for the line (points = (360/precision))"+"\n"+
                                                    "Actual: " + str(int(360/precision)) + " points for 1 turn"+"\n"+
                                                    "Loading a file or angle checked the value displayd change color in blue just to inform"))
        self.LAB_Numb_Spires.setText("Number of coil")

        ############### font and color Label
        font = QtGui.QFont()
        self.LAB_Precision_Turn.setFont(font)
        self.LAB_Precision_Turn.setStyleSheet("Base")
        ############### font and color

        ############### font and color
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor("Base"))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        self.DS_Precision_Turn.setPalette(palette)
        font = QtGui.QFont()
        font.setBold(False)
        self.DS_Precision_Turn.setFont(font)
        ###############

        self.CB_B_E_Angle.setChecked(False)
        self.SP_Begin_Angle.setEnabled(False)
        debutAngle = 0
        self.SP_Begin_Angle.setValue(debutAngle)
        self.SP_End_Angle.setEnabled(False)
        finAngle   = 360
        self.SP_End_Angle.setValue(finAngle)
        modifyAngle = 0

        self.CH_Points.setChecked(False)
        affPoint = 0
        self.CH_Reverse.setChecked(False)
        spireReverse = 0
        ###############
        sel = ""
        del pointsDirection[:]
        plr = ""
        Direction_Begin = 0

        switchAdaptRadius  = 0
        self.PB_Adapt_Radius.setEnabled(False)
        self.PB_Adapt_Radius.setStyleSheet("background-color: QPalette.Base")  # origin system
        self.PB_Adapt_Radius.setText("Normal")

        self.PB_Center_Point.setEnabled(False)
        self.PB_Center_Point.setStyleSheet("background-color: QPalette.Base")  # origin system
        centerFaceOrPoint = 0
        self.PB_Center_Point.setText(_fromUtf8("Point Mouse"))

        self.CB_Position.setEnabled(False)
        self.CB_Position.setStyleSheet("background-color: QPalette.Base")      # origin system

        self.PB_CreaCircle.setEnabled(False)
        self.PB_CreaCircle.setStyleSheet("background-color: QPalette.Base")    # origin system
        del selectedCircle[:]

        self.DS_horizontalSlider.setValue(0)
        self.horizontalSlider.setValue(0)
        self.groupBox_04.setEnabled(False)
        self.groupBox_04.setStyleSheet("background-color: QPalette.Base")      # origin system
        self.groupBox_04.setTitle("Position (" + str(len(sel)) + ")")

        ###############
        self.SP_Numbering_Spire.setValue(numberSpiresModified)
        self.SP_Numbering_Spire.setMaximum(numberSpires)
        self.DS_Pas_Spire.setValue(0)    #pas
        self.DS_Radius_Spire.setValue(0) #rayon
        self.textEdit.setText("")
        self.textEdit.clear()

        lissageSpire = 0
        self.SP_Lissage.setValue(0)
        self.SP_Lissage.setVisible(False)
        self.SP_Lissage.setMaximum(int(360/precision)-1)
        self.SP_Lissage.setToolTip(_fromUtf8("Smoothing the line if the difference between two coils"+"\n"+
                                            "The maximum value is egual of the precision number point given -1 (" + str(int(360/precision)-1)+")"+"\n"+
                                            "The finish and precision are influenced by this value"+"\n"+
                                            "PS: The result can be satisfying or completely wrong (prototype state)"))
        self.CH_Smooting.setChecked(False)
        self.CH_Smooting.setVisible(True)
        self.CH_Smooting.setToolTip(_fromUtf8("Smoothing the line if the difference between two coils"+"\n"+
                                              "The maximum value is egual of the precision number point given -1 (" + str(int(360/precision)-1)+")"+"\n"+
                                              "The finish and precision are influenced by this value"+"\n"+
                                              "PS: The result can be satisfying or completely wrong (prototype state)"))
        lissageS = []
        del lissageS[:]
        lissageS = numberSpires*[0]
        self.SP_Lissage.setValue(0)

        self.PBA_progressBar.setVisible(False)
        self.PU_Accept_Value.setVisible(True)

        zoom = 140
        self.textEdit.setGeometry(QtCore.QRect(20, zoom, 211, 51))

        helixS = []
        del helixS[:]
        helixS = numberSpires*[pas]

        radiusS = []
        del radiusS[:]
        radiusS = numberSpires*[rayon]

        self.CH_Cone.setChecked(False)
        self.DS_Radius_2_Cone.setValue(rayon)
        self.DS_Radius_2_Cone.setEnabled(False)
        spireConeUne  = 0
        spireConeComp = 0
#        App.Console.PrintMessage("on_PU_Reset "+"\n")

    def on_DS_Numb_Spires(self,value):                                         # nombre de spire total
        global pas
        global numberSpires
        numberSpires = value
        a = ui
        a.on_PU_Reset(1)
        self.SP_Numbering_Spire.setToolTip(_fromUtf8("Numbering of coil for 1 to max = Number of spires ("+str(numberSpires)+")"))
#        App.Console.PrintMessage("on_DS_Numb_Spires "+str(numberSpires)+"\n")

    def on_DS_Radius_Sping(self,value):                                        # rayon axial du ressort
        global rayon
        rayon = value
        self.PU_To_Radius.setText(str(rayon) + " mm")
        a = ui
        a.on_PU_Reset(1)
#        App.Console.PrintMessage("on_DS_Radius_Sping "+str(rayon)+"\n")

    def on_DS_Pas_Spring(self,value):                                          # pas (pitch) du ressort
        global pas
        global numberSpires
        global numberSpiresModified
        global pasSpire
        pas = value
        self.PU_To_Pas.setText(str(pas) + " mm")
        a = ui
        a.on_PU_Reset(1)
#        App.Console.PrintMessage("on_DS_Pas_Spring "+str(pas)+"\n")

    def on_DS_Precision_Turn(self,value):                                      # " ! float " 360/precision number points for 1 turn
        global precision
        precision = value
        ############### font and color Label
        font = QtGui.QFont()
        self.LAB_Precision_Turn.setFont(font)
        self.LAB_Precision_Turn.setStyleSheet("Base")
        ############### font and color
        ############### font and color
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor("Base"))
        brush.setStyle(QtCore.Qt.SolidPattern)
#        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        self.DS_Precision_Turn.setPalette(palette)
        font = QtGui.QFont()
        font.setBold(False)
#        font.setWeight(75)
        self.DS_Precision_Turn.setFont(font)
        ###############
        self.DS_Precision_Turn.setSuffix("  ( " + str(int(360/precision)) + " points )")
        self.DS_Precision_Turn.setToolTip(_fromUtf8("Precision for the line (points = (360/precision))"+"\n"+
                                                    "Actual: " + str(int(360/precision)) + " points for 1 turn"+"\n"+
                                                    "Loading a file or angle checked the value displayd change color in blue just to inform"))
        self.SP_Lissage.setMaximum(int(360/precision)-1)
        self.CH_Smooting.setToolTip(_fromUtf8("Smoothing the line if the difference between two coils"+"\n"+
                                              "The maximum value is egual of the precision number point given -1 (" + str(int(360/precision)-1)+")"+"\n"+
                                              "The finish and precision are influenced by this value"+"\n"+
                                              "PS: The result can be satisfying or completely wrong (prototype state)"))
#        App.Console.PrintMessage("on_DS_Precision_Turn "+str(precision)+"\n")

    def on_CH_Cone(self):                                                      # Cone
        global radius_2_Cone
        global rayon
        if self.CH_Cone.isChecked():
            self.DS_Radius_2_Cone.setEnabled(True)
#            self.LAB_Radius_2_Cone.setVisible(True)
        else:
            self.DS_Radius_2_Cone.setEnabled(False)
#            self.LAB_Radius_2_Cone.setVisible(False)
        radius_2_Cone = rayon
        self.DS_Radius_2_Cone.setValue(radius_2_Cone)
#        App.Console.PrintMessage("on_CH_Cone"+"\n")

    def on_SP_Begin_Angle(self,value):                                          # 
        global debutAngle
        debutAngle = value
#        App.Console.PrintMessage("on_SP_Begin_Angle "+str(debutAngle)+"\n")

    def on_SP_End_Angle(self,value):                                            # 
        global finAngle
        finAngle = value
#        App.Console.PrintMessage("on_SP_End_Angle "+str(finAngle)+"\n")

    def on_CB_B_E_Angle(self):                                                 # 
        global debutAngle
        global finAngle
        global modifyAngle
        global precision
        global fichierOpen
        if self.CB_B_E_Angle.isChecked(): 
            modifyAngle = 1
            self.SP_Begin_Angle.setEnabled(True)
            self.SP_End_Angle.setEnabled(True)
            if fichierOpen == 0:
                precision = 1
            fichierOpen = 0
            self.DS_Precision_Turn.setValue(precision)

            ############### font and color Label
            font = QtGui.QFont()
            self.LAB_Precision_Turn.setFont(font)
            self.LAB_Precision_Turn.setStyleSheet("color : #0000ff")
            ############### font and color
            ############### font and color DoubleSpinBox
            palette = QtGui.QPalette()
            brush = QtGui.QBrush(QtGui.QColor( 0, 0, 255))
            brush.setStyle(QtCore.Qt.SolidPattern)
#            palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
            palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
            self.DS_Precision_Turn.setPalette(palette)
            font = QtGui.QFont()
            font.setBold(True)
            font.setWeight(75)
            self.DS_Precision_Turn.setFont(font)
            ###############

        else:
            modifyAngle = 0
#            self.DS_Precision_Turn.setEnabled(True)
            self.SP_Begin_Angle.setEnabled(False)
            self.SP_End_Angle.setEnabled(False)
            self.CB_B_E_Angle.setChecked(False)
            self.SP_Begin_Angle.setEnabled(False)
            debutAngle = 0
            self.SP_Begin_Angle.setValue(debutAngle)
            self.SP_End_Angle.setEnabled(False)
            finAngle   = 360
            self.SP_End_Angle.setValue(finAngle)
#        App.Console.PrintMessage("CB_B_E_Angle "+"\n")

    def on_RA_Wire(self):                                                      # 
        global typeLine
        typeLine = 1
#        App.Console.PrintMessage("on_RA_Wire "+str(typeLine)+"\n")

    def on_RA_BSpline(self):                                                   # 
        global typeLine
        typeLine = 0
#        App.Console.PrintMessage("on_RA_BSpline "+str(typeLine)+"\n")

    def on_CH_Points(self):                                                    # 
        global affPoint
        if self.CH_Points.isChecked(): 
            affPoint = 1
        else:
            affPoint = 0
#        App.Console.PrintMessage("on_CH_Points "+"\n")

    def on_CH_Reverse(self):                                                   # reverse the rotation Rigth/Left
        global spireReverse
        if self.CH_Reverse.isChecked(): 
            spireReverse = 1
        else:
            spireReverse = 0
#        App.Console.PrintMessage("on_CH_Reverse " + str(spireReverse)+"\n")

    def on_DS_Radius_2_Cone(self,value):                                       # Diametre num 2 , Helix Conique
        global rayon
        global numberSpires
        global helixS
        global radiusS
        global radius_2_Cone
        global spireConeUne
        global spireConeComp
        global lissageS

        if self.CH_Cone.isChecked():
            numberSpires = self.DS_Numb_Spires.value()

            numberSpires += 1
            self.SP_Numbering_Spire.setMaximum(numberSpires)
            helixS = []
            del helixS[:]
            helixS = (numberSpires)*[pas]
            radiusS = []
            del radiusS[:]
            radiusS = (numberSpires)*[rayon]
            lissageS = []
            del lissageS[:]
            lissageS = numberSpires*[0]

            if value < rayon:
                radius_2_Cone = value = rayon
            radius_2_Cone = value
            self.DS_Radius_2_Cone.setValue(radius_2_Cone)
            if numberSpires != 1:
                spireConeUne = 0
                cone = (radius_2_Cone - rayon) / (numberSpires -1)# +1 
                for i in range(numberSpires):
                    radiusS[i] = rayon + (cone * (i)) #  
            else:
                spireConeUne = 1
            spireConeComp = 1
#        App.Console.PrintMessage("on_DS_Radius_2_Cone "+str(radius_2_Cone)+" "+str(spireConeUne)+"\n")

    ####
    def on_PB_Adapt_Radius(self):                                              # Adapt circle
        global switchAdaptRadius
        if switchAdaptRadius == 0:
            switchAdaptRadius = 1
            self.PB_Adapt_Radius.setText("Adapt Rad.")
        else:
            switchAdaptRadius = 0
            self.PB_Adapt_Radius.setText("Normal")
#        App.Console.PrintMessage("on_CB_Adapt_Radius "+str(switchAdaptRadius)+"\n")

    def on_PB_Center_Point(self):                                              # Center Face or Point
        global centerFaceOrPoint
        if centerFaceOrPoint == 0:
            centerFaceOrPoint = 1
            self.PB_Center_Point.setText(_fromUtf8("Center Face"))
        else:
            centerFaceOrPoint = 0
            self.PB_Center_Point.setText(_fromUtf8("Point Mouse"))
#        App.Console.PrintMessage("on_CB_Center_Point "+str(centerFaceOrPoint)+"\n")

    def on_PB_Begin_End(self):                                                 # place the spring to left center rigth
        global Direction_Begin
        global pointsDirection
        global ressort
        global coor_Z
        self.horizontalSlider.setMaximum(len(pointsDirection))
        ressort.Placement.Base = pointsDirection[0]
        if (Direction_Begin == 0):
            Direction_Begin = 1
            ressort.Placement.Base = pointsDirection[0]
            self.horizontalSlider.setValue(0)
        elif (Direction_Begin == 1):
            ressort.Placement.Base = pointsDirection[int((len(pointsDirection) / 2))]
            self.horizontalSlider.setValue(int((len(pointsDirection) / 2)))
            Direction_Begin = 2
        elif (Direction_Begin == 2):
            Direction_Begin = 0
            ressort.Placement.Base = pointsDirection[-1]
            self.horizontalSlider.setValue(len(pointsDirection))
    
        FreeCAD.ActiveDocument.recompute()
#        App.Console.PrintMessage("on_CB_01_Begin_End"+"\n") FreeCAD.Vector(

    def on_PB_Reverse_Spr(self):                                               # reverse the spring
        global ressort
        a = FreeCAD.ActiveDocument.getObject(ressort.Name).Placement
        b = App.Placement(App.Vector(0.0,0.0,0.0), App.Rotation(App.Vector(0.0,1.0,0.0),180.0), App.Vector(0,0,0))
        c = a.multiply(b)
        FreeCAD.ActiveDocument.getObject(ressort.Name).Placement = c
#        App.Console.PrintMessage("on_PB_Reverse_Spr"+"\n")

    def on_DS_horizontalSlider(self,val):                                      # 
        global pointsDirection
        global ressort
        global Direction_Distance
        if len(pointsDirection) != 0:
            self.DS_horizontalSlider.setSingleStep(Direction_Distance)
            self.horizontalSlider.setValue(val*10)
            try:
                ressort.Placement.Base = FreeCAD.Vector(pointsDirection[int(val*10)])
            except Exception:
                None
            FreeCAD.ActiveDocument.recompute()
#        App.Console.PrintMessage("on_DS_horizontalSlider"+"\n")

    def on_PB_Reverse_Com(self):                                               # reverse the compteur
        global pointsDirection
        global ressort
        pointsDirection.reverse()
        self.DS_horizontalSlider.setValue(0)
        self.horizontalSlider.setValue(0)
        ressort.Placement.Base = pointsDirection[0]
#        App.Console.PrintMessage("on_PB_Reverse_Com"+"\n")

    def on_horizontal_slider(self, val):                                       # connection on_horizontal_slider
        global pointsDirection
        if len(pointsDirection) != 0:
            self.DS_horizontalSlider.setValue(val/10)
#        App.Console.PrintMessage("on_horizontal_slider " + str(val/10)+"\n")

    def on_CB_Position(self):                                                  # Position
        global switchAdaptRadius
        global centerFaceOrPoint
        global Direction_Distance
        global Direction_Begin
        global pointsDirection
        global ressort
        global sel

        if self.CB_Position.isChecked():
            self.PB_Adapt_Radius.setEnabled(False)
            self.PB_Adapt_Radius.setChecked(False)
            self.PB_Adapt_Radius.setStyleSheet("background-color: QPalette.Base")   # origin system
            switchAdaptRadius = 0
            self.PB_Center_Point.setEnabled(False)
            self.PB_Center_Point.setChecked(False)
            self.PB_Center_Point.setStyleSheet("background-color: QPalette.Base")   # origin system
            centerFaceOrPoint = 0
            self.groupBox_04.setEnabled(True)
            self.groupBox_04.setStyleSheet("background-color: white;\n"
                                           "border:2px solid rgb(0, 187, 0);")      # bord white and green

            selobject = FreeCADGui.Selection.getSelection()                         # Select an object
            del pointsDirection[:]
            sel = FreeCADGui.Selection.getSelectionEx()
            self.groupBox_04.setTitle("Position (" + str(len(sel)) + ")")
            try:
                Direction_Begin = 0
                pointsDirection = sel[0].Object.Shape.discretize(Distance = Direction_Distance) #
    
                ressort = selobject[1]
                self.horizontalSlider.setValue(0)
    
                self.groupBox_04.setTitle("Position (" + str(len(sel)) + ")(Points: " + str(len(pointsDirection)) + ")")
                self.horizontalSlider.setMaximum(len(pointsDirection))
                self.DS_horizontalSlider.setMaximum(int(len(pointsDirection)/10))
                self.DS_horizontalSlider.setValue(len(pointsDirection)/10)
            except Exception:
                del pointsDirection[:]
                self.groupBox_04.setTitle("Position (" + str(0) + ")")
                App.Console.PrintError("Wrong selection"+"\n")
        else:
#            centerFaceOrPoint = 0
            self.groupBox_04.setEnabled(False)
            self.groupBox_04.setStyleSheet("background-color: QPalette.Base")       # origin system

            FreeCADGui.Selection.clearSelection() 
            sel = selobject = ""
            del pointsDirection[:]
            self.groupBox_04.setTitle("Position (" + str(len(sel)) + ")")
            None
#        App.Console.PrintMessage("on_CB_Position "+"\n")

    def on_PB_CreaCircle(self):                                                # create circle on 3 points
        global selectedCircle

        if len(selectedCircle) == 3:
            if (selectedCircle[0]==selectedCircle[1]) or (selectedCircle[0]==selectedCircle[2]) or selectedCircle[1]==selectedCircle[2] :
                App.Console.PrintError("Bad selection the points are egual"+"\n")
            else:
                try:
                    C1 = Part.Arc(FreeCAD.Vector(selectedCircle[0]),FreeCAD.Vector(selectedCircle[1]),FreeCAD.Vector(selectedCircle[2]))
                    S1 = Part.Shape([C1])                                      # create arc base
                    Part.show(S1)
 
                    obj = App.ActiveDocument.ActiveObject                      # select the object created
                    Gui.Selection.addSelection(obj)
                    sel = obj.Shape
        
                    CircleDirection = sel.Curve.Axis                           # decode the datas
                    CircleRayon     = sel.Curve.Radius
                    CircleAxis      = sel.Curve.Center
        
                    App.ActiveDocument.removeObject(obj.Label)                 # remove arc master
        
                    v = CircleDirection                                        # give direction to circle
                    r = App.Rotation(App.Vector(0,0,1),v)
                    pl=FreeCAD.Placement()
                    pl.Base=FreeCAD.Vector(CircleAxis)
                    pl.Rotation.Q = r.Q
                    circle3Points = Draft.makeCircle(radius=CircleRayon, placement=pl, face=False, support=None)
                    circle3Points.ViewObject.LineColor = (1.0,0.0,0.0)         # give color
                    circle3Points.Label = "SpringCircle (" + str(round(CircleRayon,3)) + " r)" # give label
                except Exception:
                    App.Console.PrintError("Three points are collinear or bad selection"+"\n")
            del selectedCircle[:]
            FreeCAD.ActiveDocument.recompute()
        #self.PB_CreaCircle.setEnabled(False)
#        App.Console.PrintMessage("on_PB_CreaCircle "+"\n")
        ####

    def on_S_Numbering_Spire(self,value):                                      # numero de la spire a modifier
        global numberSpires
        global numberSpiresModified
        global lissageSpire

        self.SP_Numbering_Spire.setMaximum(numberSpires)
        numberSpiresModified = value
        lissageSpire = 0
        self.SP_Lissage.setValue(lissageSpire)
        self.SP_Lissage.setVisible(False)
        self.CH_Smooting.setVisible(True)
        self.CH_Smooting.setChecked(False)
#        App.Console.PrintMessage("on_S_Nubering_Spire "+str(numberSpiresModified)+"\n")

    def on_CH_Smooting(self):                                                  # lissage precision
        global lissageSpire
        global precision

        self.SP_Lissage.setVisible(True)
        self.CH_Smooting.setVisible(False)
        self.CH_Smooting.setToolTip(_fromUtf8("Smoothing the line if the difference between two coils"+"\n"+
                                              "The maximum value is egual of the precision number point given -1 (" + str(int(360/precision)-1)+")"+"\n"+
                                              "The finish and precision are influenced by this value"+"\n"+
                                              "PS: The result can be satisfying or completely wrong (prototype state)"))
        lissageSpire = 0
#        App.Console.PrintMessage("on_CH_Smooting "+str(lissageSpire)+"\n")

    def on_S_Lissage(self,value):                                              # option lissageS des raccords
        global lissageSpire
        global precision

        lissageSpire = value
        self.SP_Lissage.setMaximum(int(360/precision)-1)
        self.SP_Lissage.setToolTip(_fromUtf8("Smoothing the line if the difference between two coils"+"\n"+
                                            "The maximum value is egual of the precision number point given -1 (" + str(int(360/precision)-1)+")"+"\n"+
                                            "The finish and precision are influenced by this value"+"\n"+
                                            "PS: The result can be satisfying or completely wrong (prototype state)"))
#        App.Console.PrintMessage("on_S_Lissage "+str(lissageSpire)+"\n")

    def on_DS_Pas_Spire(self,value):                                           # pas (pitch) de la spire a modifier
        global pasSpire

        pasSpire = value
#        App.Console.PrintMessage("on_DS_Pas_Spire "+str(pasSpire)+"\n")

    def on_PU_To_Pas(self):                                                    # aligne le pas (pitch) de la spire
        global pasSpire
        global pas

        pasSpire = pas
        self.DS_Pas_Spire.setValue(pasSpire)
#        App.Console.PrintMessage("on_PU_To_Pas "+str(pasSpire)+"\n")

    def on_DS_Radius_Spire(self,value):                                        # pas (pitch) du rayon a modifier
        global rayonSpire
        rayonSpire = value
#        App.Console.PrintMessage("on_DS_Radius_Spire "+str(rayonSpire)+"\n")

    def on_PU_To_Radius(self):                                                 # aligne le rayon
        global rayonSpire
        global rayon

        rayonSpire = rayon
        self.DS_Radius_Spire.setValue(rayonSpire)
#        App.Console.PrintMessage("on_PU_To_Radius_Value "+str(rayonSpire)+"\n")

    def on_PU_Accept_Value(self):                                              # accepter la modification de la spire
        global numberSpiresModified
        global numberSpires
        global pasSpire
        global rayonSpire
        global helixS
        global radiusS
        global lissageSpire
        global lissageS

        if rayonSpire != 0:
            if numberSpiresModified == 1:
                helixS[0] = pasSpire
                radiusS[0]= rayonSpire
                lissageS[0] = lissageSpire
                self.textEdit.append("Coil number " + str(numberSpiresModified) + " = " + str(helixS[0]) + " " + str(radiusS[0]) + " " + str(lissageS[0]))
                App.Console.PrintMessage("Coil number " + str(numberSpiresModified) + " = " + str(helixS[0]) + " " + str(radiusS[0]) + " " + str(lissageS[0])+"\n")
            else:
                helixS[numberSpiresModified-1] = pasSpire
                radiusS[numberSpiresModified-1]= rayonSpire
                lissageS[numberSpiresModified-1] = lissageSpire
                self.textEdit.append("Coil number " + str(numberSpiresModified) + " = " + str(helixS[numberSpiresModified-1]) + " " + str(radiusS[numberSpiresModified-1]) + " " + str(lissageS[numberSpiresModified-1]))
                App.Console.PrintMessage("Coil number " + str(numberSpiresModified) + " = " + str(helixS[numberSpiresModified-1]) + " " + str(radiusS[numberSpiresModified-1]) + " " + str(lissageS[numberSpiresModified-1])+"\n")
    
            self.SP_Lissage.setValue(0)
            self.SP_Lissage.setVisible(False)
            self.CH_Smooting.setVisible(True)
            self.CH_Smooting.setChecked(False)
            lissageSpire = 0
        else:
            self.textEdit.setTextColor(QColor("red"))
            self.textEdit.append("Coil number " + str(numberSpiresModified) + " Radius zero not allowed do " )
            self.textEdit.setTextColor(QColor("Base"))
            App.Console.PrintError("Coil number " + str(numberSpiresModified) + " Radius zero not allowed do "+"\n")
#        App.Console.PrintMessage("on_PU_Accept_Value "+"\n")

    def on_PB_Clear(self):                                                     # 
        self.textEdit.setText("")
        self.textEdit.clear()
#        App.Console.PrintMessage("on_PB_Clear "+"\n")

    def on_PB_Zoom(self):                                                     # 
        global zoom

        if zoom == 0:
            zoom = 1
            self.PU_Accept_Value.setText(_fromUtf8("Accept"))
            self.grid_05.addWidget(self.PU_Accept_Value, 3, 3, 1, 1)
            self.grid_05.addWidget(self.textEdit, 0, 0, 7, 3)
        else:
            zoom = 0
            self.grid_05.addWidget(self.PU_Accept_Value, 3, 0, 1, 4)
            self.PU_Accept_Value.setText(_fromUtf8("Accept the value modified"))
            self.grid_05.addWidget(self.textEdit, 5, 0, 2, 3)
#        App.Console.PrintMessage("on_PB_Loupe "+"\n")

    def on_PU_Quit(self):                                                      # Quit
        global s

        App.Console.PrintMessage("\n"+"Fin FCSpring_Helix_Variable"+"\n"+"___________________________"+"\n")
        FreeCADGui.Selection.removeObserver(s)                                 # desinstalle la fonction residente
        try:
            self.window.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)    # destroy
            self.window.deleteLater()                                     # destroy
            self.window.destroy()                                         # destroy
        except Exception:
            self.window.hide()
            None
#        App.Console.PrintMessage(" "+"\n")

    def on_PU_Read(self):                                                      # lecture
        global path
        global numberSpires
        global rayon
        global pas
        global precision
        global typeLine
        global affPoint
        global helixS
        global radiusS
        global debutAngle
        global finAngle
        global modifyAngle
        global radius_2_Cone
        global spireConeUne
        global spireConeComp
        global spireReverse
        global lissageS
        global fichierOpen
        global nomF
        global setPathLatestDirectory

        OpenName = ""
        ####  mint
        if switchQFileDialogMint == True:   # Mint
            OpenName, Filter = PySide2.QtWidgets.QFileDialog.getOpenFileName(None, u"Read a file FCSpring", setPathLatestDirectory, "(FCSpring *.FCSpring);;")#PySide2 Mint
        ####  mint
        else:
            OpenName, Filter = PySide2.QtWidgets.QFileDialog.getOpenFileName(None, u"Read a file FCSpring", setPathLatestDirectory, "*.FCSpring;;")#PySide2

        try:
            if OpenName != "":
                ####new2
                pathFile      = os.path.dirname(OpenName) + "/"  #1# = C:/Provisoire400/
                setPathLatestDirectory = pathFile
                FreeCAD.ParamGet(u"User parameter:BaseApp/Preferences/Macros/FCMmacros/" + __Title__).SetString(u"setPathLatestDirectory", setPathLatestDirectory)    #*"C:\ ???"
                #racineDrive   = os.path.splitdrive(OpenName)[0]  #2# = C:
                #formatFichier = os.path.splitext(OpenName)[1]    #4# = .png
                #OpenName      = os.path.splitext(OpenName)[0]    #5# = /home/kubuntu/.FreeCAD/Macro/Texture_007_H #= C:/Provisoire400/image3D
                #nomFichier    = os.path.basename(OpenName)       #3# = image3D
                #SaveNameformatFichier = OpenName + formatFichier #6# = C:/Provisoire400/image3D.png
                #pathFileSaveNameformatFichier = pathFile + nomFichier + formatFichier #7# = C:/Provisoire400/image3D.png
                ####new2

                try:

                    #### Chrono begin ##################################
                    chrono(0)                 # chrono begin          ##
                    ####################################################

                    file = open(OpenName, "r") # read
                    Header = file.readline().rstrip('\n\r')                                                                #1
                    if (Header == "FCString") or (Header == "FCString2") or (Header == "FCString3") or (Header == "FCString4"):
                        a = ui
                        a.on_PU_Reset(0)
                        App.Console.PrintMessage("____________________"+"\n")

                        self.textEdit.clear()
                        op = OpenName.split("/")
                        op2 = op[-1].split(".")
                        nomF = op2[0]

                        App.Console.PrintMessage(nomF+"\n")
                        App.Console.PrintMessage(str(Header)+"\n")
                        numberSpires = file.readline().rstrip('\n\r')                                                      # 2
                        numberSpires = int(numberSpires)
                        self.DS_Numb_Spires.setValue(numberSpires)
                        App.Console.PrintMessage(str(numberSpires)+"\t"+"Number coil"+"\n")

                        rayon = file.readline().rstrip('\n\r')                                                             # 3
                        rayon = float(rayon)
                        radiusS = numberSpires*[rayon]
                        self.DS_Radius_Sping.setValue(rayon)
                        App.Console.PrintMessage(str(rayon)+"\t"+"Radius"+"\n")

                        pas = file.readline().rstrip('\n\r')                                                               # 4
                        pas = float(pas)
                        helixS = numberSpires*[pas]
                        self.DS_Pas_Spring.setValue(pas)
                        App.Console.PrintMessage(str(pas)+"\t"+"Pitch"+"\n")

                        precision = file.readline().rstrip('\n\r')                                                         # 5
                        precision = float(precision)
                        self.DS_Precision_Turn.setValue(precision)
                        App.Console.PrintMessage(str(precision)+"\t"+"Precision"+"\n")

                        if (Header == "FCString3") or (Header == "FCString4"):
                            typeLine, spireReverse = file.readline().rstrip(',\n\r').split()                               # 6 
                            spireReverse = int(spireReverse)
                            if spireReverse == 0:
                                self.CH_Reverse.setChecked(False)
                            else:
                                self.CH_Reverse.setChecked(True)
                        else:
                            typeLine = file.readline().rstrip('\n\r')

                        typeLine = int(typeLine)
                        if typeLine == 0:
                            self.RA_BSpline.setChecked(True)
                        else:
                            self.RA_Wire.setChecked(True)
                        if (Header == "FCString2") or (Header == "FCString3") or (Header == "FCString4"):
                            self.CH_Points.setChecked(False) # reset point
                            affPoint = 0

                            debutAngle = file.readline().rstrip('\n\r')                                                     # 7
                            debutAngle = int(debutAngle)
                            self.SP_Begin_Angle.setValue(int(debutAngle))

                            finAngle = file.readline().rstrip('\n\r')                                                       # 8
                            finAngle = int(finAngle)
                            self.SP_End_Angle.setValue(int(finAngle))

                            modifyAngle = file.readline().rstrip('\n\r')                                                    # 9
                            modifyAngle = int(modifyAngle)
                            if modifyAngle == 1:
                                self.CB_B_E_Angle.setChecked(True) 
                                fichierOpen = 1
                            else:
                                self.CB_B_E_Angle.setChecked(False)
                                fichierOpen = 0
                            a = ui
                            a.on_CB_B_E_Angle()
                            try:
                                sp, sc, ra = file.readline().rstrip(',\n\r').split()                                        # 10
                                spireConeUne  = int(sp)   # cone
                                spireConeComp = int(sc)   # compensation
                                radius_2_Cone = float(ra) # radius 2 cone
                            except Exception:
                                spireConeUne  = 0
                                spireConeComp = 0
                                radius_2_Cone = 0

                            if (spireConeUne == 1) or (spireConeComp == 1):
                                self.DS_Radius_2_Cone.setEnabled(True)
                                self.DS_Radius_2_Cone.setValue(radius_2_Cone)
                                self.CH_Cone.setChecked(True)
                                self.LAB_Numb_Spires.setText("Number real ("+str(numberSpires - 1)+")")
                                self.LAB_Numb_Spires.setToolTip(_fromUtf8("The number of coil for a spring conical registered"+"\n" 
                                                                  "is number of coil displayed minus 1"))
                            else:
                                self.DS_Radius_2_Cone.setEnabled(False)
                                self.DS_Radius_2_Cone.setValue(rayon)
                                self.CH_Cone.setChecked(False)
#                                self.CH_Cone.setEnabled(False)
                                self.LAB_Numb_Spires.setText("Number of coil")
                                self.LAB_Numb_Spires.setToolTip(_fromUtf8("Number of coil"))
                            App.Console.PrintMessage(str(spireConeUne)+" "+str(radius_2_Cone)+"\t"+"Radius cone"+"\n\n")
                      
                        dummy = file.readline().rstrip('\n\r')                                                               # 11

                        del lissageS[:]
                        lissageS = numberSpires*[0]

                        i = 0
                        for ligne in file:
                            if (Header == "FCString4"):
                                a , b , c = ligne.rstrip('\n\r').split()
                                helixS[i]   = float(a)
                                radiusS[i]  = float(b)
                                lissageS[i] = int(c)
                                App.Console.PrintMessage(str(i+1)+":  "+str(helixS[i])+"   "+str(radiusS[i])+"   "+str(lissageS[i])+"\n")
                                self.textEdit.append("Coil number " + str(i+1) + " = " + str(helixS[i]) + " " + str(radiusS[i])+"   "+str(lissageS[i])) # 12
                            else:
                                a , b = ligne.rstrip('\n\r').split()
                                helixS[i] = float(a)
                                radiusS[i] = float(b)
                                App.Console.PrintMessage(str(i+1)+":  "+str(helixS[i])+"   "+str(radiusS[i])+"\n")
                                self.textEdit.append("Coil number " + str(i+1) + " = " + str(helixS[i]) + " " + str(radiusS[i]))                        # 12
                            i += 1
                        App.Console.PrintMessage("____________________"+"\n")
                        self.textEdit.verticalScrollBar().setValue(0)          # 
                        self.textEdit.verticalScrollBar().setSliderPosition(0) #

                    else:
                        self.PU_Reload.setEnabled(False)
                        App.Console.PrintMessage("Error file not FCSpring or not FCSpring2.3.4"+"\n")
                        errorDialog("Error file not FCSpring or not FCSpring2.3.4 "+"\n")
                finally:
                    file.close()

                #### Chrono(1) end #################################
                chrono(1)                 # chrono(1) end         ##
                ####################################################

                #self.label_11_Name.setText(nomF)
        except Exception:
            App.Console.PrintMessage("Error in reading the file "+OpenName+"\n")
            errorDialog("Error in reading the file "+OpenName)

    def on_PU_Save(self):                                                      # enregistrement
        global path
        global numberSpires
        global rayon
        global pas
        global precision
        global typeLine
        global helixS
        global radiusS
        global debutAngle
        global finAngle
        global modifyAngle
        global radius_2_Cone
        global spireConeUne
        global spireConeComp
        global spireReverse
        global lissageS
        global setPathLatestDirectory

        SaveName = ""
        ####  mint
        if switchQFileDialogMint == True:   # Mint
            SaveName, Filter = PySide2.QtWidgets.QFileDialog.getSaveFileName(None, "Save a file FCSpring", setPathLatestDirectory, " (FCSpring *.FCSpring);;")#PySide2 Mint
            Filter = Filter[Filter.find("."):Filter.find(")")]
            SaveName = SaveName + Filter
        ####  mint
        else:
            SaveName, Filter = PySide2.QtWidgets.QFileDialog.getSaveFileName(None, "Save a file FCSpring", setPathLatestDirectory, "*.FCSpring;;FCSpring (*.FCSpring);;")#PySide2

        if SaveName == "":
            App.Console.PrintMessage(u"Process aborted" + "\n")
            errorDialog(u"Process aborted")
        else:
            App.Console.PrintMessage(u"Registration of " + SaveName + "\n")
            ####new2
            pathFile      = os.path.dirname(SaveName) + "/"  #1# = C:/Provisoire400/
            setPathLatestDirectory = pathFile
            FreeCAD.ParamGet(u"User parameter:BaseApp/Preferences/Macros/FCMmacros/" + __Title__).SetString(u"setPathLatestDirectory", setPathLatestDirectory)    #*"C:\ ???"
            #racineDrive   = os.path.splitdrive(SaveName)[0]  #2# = C:
            #formatFichier = os.path.splitext(SaveName)[1]    #4# = .png
            #SaveName      = os.path.splitext(SaveName)[0]    #5# = /home/kubuntu/.FreeCAD/Macro/Texture_007_H #= C:/Provisoire400/image3D
            #nomFichier    = os.path.basename(SaveName)       #3# = image3D
            #SaveNameformatFichier = SaveName + formatFichier #6# = C:/Provisoire400/image3D.png
            #pathFileSaveNameformatFichier = pathFile + nomFichier + formatFichier #7# = C:/Provisoire400/image3D.png
            ####new2

            #self.label_11_Name.setText(SaveName)
            try:
                file = open(SaveName, 'w') # write
                try:
                    file.write("FCString4"+"\n")                               # 1
                    file.write(str(numberSpires)+"\n")                         # 2
                    file.write(str(rayon)+"\n")                                # 3
                    file.write(str(pas)+"\n")                                  # 4
                    file.write(str(precision)+"\n")                            # 5
                    file.write(str(typeLine)+"\t"+str(spireReverse)+"\n")      # 6
                    file.write(str(debutAngle)+"\n")                           # 7
                    file.write(str(finAngle)+"\n")                             # 8
                    file.write(str(modifyAngle)+"\n")                          # 9
                    file.write(str(spireConeUne)+"\t"+str(spireConeComp)+"\t"+str(radius_2_Cone)+"\n")             # 10
                    file.write("Coil"+"\t"+"Radius"+"\t"+"Smooting"+"\t"+"(If you change the file, always use Tab no space)"+"\n") # 11
                    for i in range(numberSpires):
                        file.write(str(helixS[i])+"\t"+str(radiusS[i])+"\t"+str(lissageS[i])+"\n")                 # 12
                finally:
                    file.close()
            except Exception:
                App.Console.PrintError("Error Registration file "+SaveName+"\n")
                errorDialog("Error Registration file "+SaveName)

    def on_PU_Save_Coord(self):                                                # Save coordinates x y z
        global points
        global setPathLatestDirectory

        if len(points) > 2:
            SaveName = ""
            ####  mint
            if switchQFileDialogMint == True:   # Mint
                SaveName, Filter = PySide2.QtWidgets.QFileDialog.getSaveFileName(None, "Save a file FCSpringCoor", setPathLatestDirectory, "(FCSpringCoor *.FCSpringCoor);;)")#PySide2 Mint
                Filter = Filter[Filter.find("."):Filter.find(")")]
                SaveName = SaveName + Filter
            ####  mint
            else:
                SaveName, Filter = PySide2.QtWidgets.QFileDialog.getSaveFileName(None, "Save a file FCSpringCoor", setPathLatestDirectory, "*.FCSpringCoor;;FCSpringCoor (*.FCSpringCoor);;")#PySide2

            if SaveName == "":
                App.Console.PrintMessage(u"Process aborted" + "\n")
                errorDialog(u"Process aborted")
            else:
                App.Console.PrintMessage(u"Registration of " + SaveName + "\n")
                ####new2
                pathFile      = os.path.dirname(SaveName) + "/"  #1# = C:/Provisoire400/
                setPathLatestDirectory = pathFile
                FreeCAD.ParamGet(u"User parameter:BaseApp/Preferences/Macros/FCMmacros/" + __Title__).SetString(u"setPathLatestDirectory", setPathLatestDirectory)    #*"C:\ ???"
                #racineDrive   = os.path.splitdrive(SaveName)[0]  #2# = C:
                #formatFichier = os.path.splitext(SaveName)[1]    #4# = .png
                #SaveName      = os.path.splitext(SaveName)[0]    #5# = /home/kubuntu/.FreeCAD/Macro/Texture_007_H #= C:/Provisoire400/image3D
                #nomFichier    = os.path.basename(SaveName)       #3# = image3D
                #SaveNameformatFichier = SaveName + formatFichier #6# = C:/Provisoire400/image3D.png
                #pathFileSaveNameformatFichier = pathFile + nomFichier + formatFichier #7# = C:/Provisoire400/image3D.png
                ####new2
                #self.label_11_Name.setText(SaveName)
                try:
                    file = open(SaveName, 'w') # write
                    try:
                        for i in points:
                            file.write(str(i[0])+" "+str(i[1])+" "+str(i[2])+"\n") # save the coordinates x y z
                    finally:
                        file.close()
                except Exception:
                    App.Console.PrintMessage("Error Registration file "+SaveName+"\n")
                    errorDialog("Error Registration file "+SaveName)
        else:
            App.Console.PrintError("Not data to save"+"\n")
#        App.Console.PrintMessage("on_PU_Save_Coord"+"\n")

    def on_PU_Read_Coord(self):                                                # Read coordinates x y z
        global typeLine
        global nomF
        global points
        global setPathLatestDirectory

        OpenName = ""
        ####  mint
        if switchQFileDialogMint == True:   # Mint
            OpenName, Filter = PySide2.QtWidgets.QFileDialog.getOpenFileName(None, u"Read a file FCSpringCoor", setPathLatestDirectory, "(FCSpringCoor *.FCSpringCoor);;")#PySide2 Mint
        ####  mint
        else:
            OpenName, Filter = PySide2.QtWidgets.QFileDialog.getOpenFileName(None, u"Read a file FCSpringCoor", setPathLatestDirectory, "*.FCSpringCoor")#PySide2

        try:
            if OpenName != "":
                ####new2
                pathFile      = os.path.dirname(OpenName) + "/"  #1# = C:/Provisoire400/
                setPathLatestDirectory = pathFile
                FreeCAD.ParamGet(u"User parameter:BaseApp/Preferences/Macros/FCMmacros/" + __Title__).SetString(u"setPathLatestDirectory", setPathLatestDirectory)    #*"C:\ ???"
                #racineDrive   = os.path.splitdrive(OpenName)[0]  #2# = C:
                #formatFichier = os.path.splitext(OpenName)[1]    #4# = .png
                #OpenName      = os.path.splitext(OpenName)[0]    #5# = /home/kubuntu/.FreeCAD/Macro/Texture_007_H #= C:/Provisoire400/image3D
                #nomFichier    = os.path.basename(OpenName)       #3# = image3D
                #SaveNameformatFichier = OpenName + formatFichier #6# = C:/Provisoire400/image3D.png
                #pathFileSaveNameformatFichier = pathFile + nomFichier + formatFichier #7# = C:/Provisoire400/image3D.png
                ####new2

                try:

                    #### Chrono(0) begin ###############################
                    chrono(0)                 # chrono(0) begin       ##
                    ####################################################

                    file = open(OpenName, "r") # read
                    a = ui
                    a.on_PU_Reset(0)
                    App.Console.PrintMessage("____________________"+"\n")

                    self.DS_Numb_Spires.setValue(numberSpires)
                    self.DS_Pas_Spring.setValue(pas)
                    self.DS_Radius_Sping.setValue(rayon)
                    self.textEdit.clear()
                    op = OpenName.split("/")
                    op2 = op[-1].split(".")
                    nomF = op2[0]
                    points = []
                    del points[:]
                    App.Console.PrintMessage(nomF+"\n")

                    self.PU_Accept_Value.setVisible(False)
                    self.PBA_progressBar.setVisible(True)
                    self.PBA_progressBar.setMaximum(0)
                    self.PBA_progressBar.setMinimum(0)
#                    self.PBA_progressBar.setValue(0)
                    X = Y = Z = 0.0
                    for ligne in file:
                        X , Y , Z = ligne.rstrip('\n\r').split()
                        points.append(FreeCAD.Vector(float(X),float(Y),float(Z)))            # append the coordinates

                    if typeLine == 1:
                        ressort = Draft.makeWire(points,closed=False,face=False,support=None)# creation spring makeWire
                    else:
                        ressort = Draft.makeBSpline(points,closed=False)                     # creation spring Draft " makeBSpline " remis pour facilite avec axes
#                        ressort = Part.BSplineCurve()                                        # creation spring Part  " BSplineCurve "
#                        ressort.interpolate(points,False)
#                        ressort0 = Part.Edge(ressort)
#                        Part.show(ressort0)
            
                    try:
                        App.ActiveDocument.ActiveObject.Label =  "Spring_" + unicode(nomF)
                    except Exception:
                        try:
                            App.ActiveDocument.ActiveObject.Label =  "Spring_" + nomF
                        except Exception:
                            App.ActiveDocument.ActiveObject.Label =  "Spring_XX"
                    
                    FreeCAD.ActiveDocument.recompute()
            
                    self.PBA_progressBar.setVisible(False)
                    self.PU_Accept_Value.setVisible(True)

                    #### Chrono(1) end #################################
                    chrono(1)                 # chrono(1) end         ##
                    ####################################################

                finally:
                    file.close()
 
                #self.label_11_Name.setText(nomF)
                self.textEdit.append("Coordinates file")# + "\n")
                self.textEdit.setTextColor(QColor("blue"))
                self.textEdit.append("PS: For Info The values showing in the configuration menu do not match the data of the spring"+"\n")
                self.textEdit.setTextColor(QColor("Base"))

        except Exception:
            App.Console.PrintMessage("Error in reading the file "+OpenName+"\n")
            errorDialog("Error in reading the file "+OpenName)
        App.Console.PrintMessage("on_PU_Read_Coord"+"\n")

    def on_PU_Launch(self):                                                    # Execute
        global numberSpires
        global rayon
        global pas
        global precision
        global typeLine
        global helixS
        global pasSpire
        global radiusS
        global affPoint
        global debutAngle
        global finAngle
        global modifyAngle
        global radius_2_Cone
        global spireConeUne
        global spireConeComp
        global spireReverse
        global lissageSpire
        global lissageS
        global points
        global nomF
        global ressort

        global pointsDirection
        global Direction_Begin
        global Direction_Distance
        global plr
        global coor_Z
        global ui
        global sel
        global hauteurCylindre
        global vecteurSouris
        global centerFaceOrPoint
        global axisSpring
        global switchReverse
        global switchAdaptRadius

        if rayon != 0:
            doc = FreeCAD.ActiveDocument
            if doc == None:
                doc = FreeCAD.newDocument()

            ressort = ""

        ############ Section object selected Begin ####################################################
            sel = FreeCADGui.Selection.getSelectionEx()                        #0# Select an object or sub object
            try:
                if len(sel) != 0:

                    #### Chrono begin ##################################
                    chrono(0)                 # chrono begin          ##
                    ####################################################

                    subObjet = sel[0].SubObjects[0]
                    selobject = FreeCADGui.Selection.getSelection()            # Select an object
    
                    FCSpring = doc.addObject("App::DocumentObjectGroup","FCSpring")
                    switchReverse = 0
                    xL = yL = 0.0
                    hauteurCylindre = sum(helixS)                              # calcul hauteur Cylindre / axe

                    if hasattr(sel[0].SubObjects[0],"Surface"):
                        subObjet = sel[0].SubObjects[0]
                        if (str(subObjet.Surface) == "<Cylinder object>") or (str(subObjet.Surface) == "<SurfaceOfExtrusion object>"):      # face
                            try:
                                GlobalCenter = LineCoorX = LineCoorY = CircleCenter = CircleRadius = EllipseCenter = EllipseRadius = 0.0
                                for a0 in subObjet.Edges:
                                    if (str(a0.Curve)[1:5]) == "Line" :
#                                        print( "xLine" )
                                        LineCoorX = a0.Vertexes[1].Point
                                        LineCoorY = a0.Vertexes[0].Point
                                    if (str(a0.Curve)[0:6]) == "Circle" :
#                                        print( "xCircle" )
                                        GlobalCenter = CircleCenter = a0.Curve.Center
                                        CircleRadius = a0.Curve.Radius
                                        xL = CircleCenter
                                        rayonX = CircleRadius
                                    if (str(a0.Curve)[1:8]) == "Ellipse" :
#                                        print( "xEllipse" )
                                        GlobalCenter = EllipseCenter = a0.Curve.Center
                                        EllipseRadius = a0.Curve.MinorRadius
                                        #EllipseRadius = a0.Curve.MajorRadius   #option
                                        rayonX = EllipseRadius
                                        xL = EllipseCenter
    
                                if LineCoorX.distanceToPoint(GlobalCenter) > LineCoorY.distanceToPoint(GlobalCenter):
                                    Direction = LineCoorX.sub(LineCoorY)
                                else:
                                    Direction = LineCoorY.sub(LineCoorX)
                                if switchAdaptRadius == 1:
                                    rayon = rayonX
                                    self.DS_Radius_Sping.setValue(rayon)
                                yL = Direction + xL
                                points=[xL,yL]
                            except Exception:
                                App.Console.PrintError("<Cylinder object> + <SurfaceOfExtrusion object"+"\n")

                        elif str(subObjet.Surface) == "<Plane object>":        # extremites
                            try:
#                                print( "<Plane object>" )
                                subObjet = sel[0].SubObjects[0]
                                obj  = selobject[0]
                                comp = subObjet
                                if centerFaceOrPoint != 0:
                                    yL = sel[0].SubObjects[0].CenterOfMass     # Center Of face
                                else:
                                    yL = vecteurSouris                         # clic point
                                uv = comp.Surface.parameter((yL))
                                nv = comp.normalAt(uv[0], uv[1]).normalize().multiply(hauteurCylindre)
                                xL = nv + yL
                                points=[xL,yL]
                            except Exception:
                                App.Console.PrintError("<Plane object>"+"\n")

                        elif (str(subObjet.Surface)[0:6] == "Sphere"):         # Sphere
                            try:
#                                print( "Sphere" )
                                subObjet = sel[0].SubObjects[0]
                                if switchAdaptRadius == 1:
                                    rayon = selobject[0].Radius.Value          # selobject[0].Radius2.Value # option
                                    self.DS_Radius_Sping.setValue(rayon)

                                obj  = selobject[0]
                                comp = subObjet
                                if centerFaceOrPoint != 0:
                                    xL = subObjet.Surface.Center               # Center
                                    direction = subObjet.Surface.Axis.normalize().multiply(hauteurCylindre)
                                    yL = direction + xL
                                else:
                                    xL = vecteurSouris                         # clic point
                                    uv = comp.Surface.parameter((xL))
                                    nv = comp.normalAt(uv[0], uv[1]).normalize().multiply(hauteurCylindre)
                                    yL = nv + xL
                                points=[xL,yL]
                            except Exception:
                                App.Console.PrintError("Sphere"+"\n")

                        elif (str(subObjet.Surface) == "<Toroid object>") or (str(subObjet.Surface) == "<Cone object>"):   # Toroid + Cone
                            try:
#                                print( str(subObjet.Surface) )
                                subObjet = sel[0].SubObjects[0]
                                if switchAdaptRadius == 1:
                                    rayon = selobject[0].Radius1.Value         # selobject[0].Radius2.Value # option
                                    self.DS_Radius_Sping.setValue(rayon)
                                obj  = selobject[0]
                                comp = subObjet
                                if centerFaceOrPoint != 0:
                                    xL = subObjet.Surface.Center               # Center
                                    direction = subObjet.Surface.Axis.normalize().multiply(hauteurCylindre)
                                    yL = direction + xL
                                else:
                                    xL = vecteurSouris                         # clic point
                                    uv = comp.Surface.parameter((xL))
                                    nv = comp.normalAt(uv[0], uv[1]).normalize().multiply(hauteurCylindre)
                                    yL = nv + xL
                                points=[xL,yL]
                            except Exception:
                                App.Console.PrintError(str(subObjet.Surface)+"\n")
                        else:
                            try:
#                                print( "Terminus" )
                                obj  = selobject[0]
                                comp = subObjet
                                xL = vecteurSouris                             # clic point
                                uv = comp.Surface.parameter((xL))
                                nv = comp.normalAt(uv[0], uv[1]).normalize().multiply(hauteurCylindre)#hauteurCylindre
                                yL = nv + xL
                                points=[xL,yL]
                            except Exception:
                                App.Console.PrintError("Face"+"\n")

                    else:
                        ###OK tous points############################################# 
                        if (len(sel[0].SubObjects) == 2):
                            xL = sel[0].SubObjects[0].Vertexes[0].Point
                            yL = sel[0].SubObjects[1].Vertexes[0].Point
                            points=[xL,yL]
                        elif (len(sel) == 2):
                            xL = sel[0].SubObjects[0].Vertexes[0].Point
                            yL = sel[1].SubObjects[0].Vertexes[0].Point
                            points=[xL,yL]
                        elif (len(sel) == 1):
                            try:
                                if (hasattr(subObjet.Curve,"Center")) and (hasattr(subObjet.Curve,"Radius")):       # arc or circle
#                                    print( "Circle/Arc" )
                                    subObjet = sel[0].SubObjects[0]
                                    if switchAdaptRadius == 1:
                                        rayon = subObjet.Curve.Radius
                                        self.DS_Radius_Sping.setValue(rayon)
                                    yL = subObjet.Curve.Center
                                    direction = subObjet.Curve.Axis.normalize().multiply(hauteurCylindre)                      # option
                                    edgeO = selobject[0]                       # edge
                                    edgeObject = edgeO.Shape.Edges[0]
                                    e = edgeObject
                                    xL = direction + yL
                                    points=[xL,yL]
                                elif (str(subObjet.Curve)[1:5]) == "Line" :
#                                    print( "Line" )
                                    xL = subObjet.Vertexes[1].Point
                                    yL = subObjet.Vertexes[0].Point
                                    points=[xL,yL]
                                elif (str(subObjet.Curve) == "<Ellipse object>"): # Ellipse
#                                    print( "Ellipse" )
                                    subObjet = sel[0].SubObjects[0]
                                    if switchAdaptRadius == 1:
                                        rayon = subObjet.Curve.MinorRadius
                                        self.DS_Radius_Sping.setValue(rayon)
                                    xL = subObjet.Curve.Center
                                    direction = subObjet.Curve.Axis.normalize().multiply(hauteurCylindre)                      # option
                                    edgeO = selobject[0]                       # edge
                                    edgeObject = edgeO.Shape.Edges[0]
                                    e = edgeObject
                                    yL = direction + xL
                                    points=[xL,yL]
                                else:
#                                    print( "Ouf.Curve" )
                                    xL = sel[0].SubObjects[0].Vertexes[0].Point
                                    yL = xL + (FreeCAD.Vector(0.0, 0.0, hauteurCylindre))
                                    points=[xL,yL]
                            except Exception:
                                xL = sel[0].SubObjects[0].Vertexes[0].Point
                                try:
                                    yL = sel[0].SubObjects[0].Vertexes[1].Point
                                except Exception:
                                    yL = xL + (FreeCAD.Vector(0.0, 0.0, hauteurCylindre))
                                points=[xL,yL]
                        ###OK tous points############################################# 
    
                    axisSpring = sel = ""
                    axisSpring = Draft.makeWire(points,closed=False,face=False,support=None)  # make line
                    axisSpring.ViewObject.LineColor  = (1.0,0.0,0.0)                          # give axis LineColor
                    axisSpring.ViewObject.DrawStyle  = "Dashdot"
                    axisSpring.Label = "Spring Axis (" + str(axisSpring.Length.Value) + ")"
                    FCSpring.addObject(axisSpring)
                    FreeCADGui.updateGui()                                     # rafraichi l'ecran
                    FreeCAD.ActiveDocument.recompute()
                    #doc.removeObject(axisSpring.Name)                          # remove axis if .. option
    
                    obj = App.ActiveDocument.getObject(axisSpring.Name)
                    Gui.Selection.addSelection(obj)                            # select the object 
                    sel = FreeCADGui.Selection.getSelectionEx()
                    pointsDirection = sel[0].Object.Shape.discretize(Distance = Direction_Distance) # discretize
    
                    v=pointsDirection[0].sub(pointsDirection[1])
                    r=App.Rotation(App.Vector(0,0,1),v)
                    plr=FreeCAD.Placement()
                    plr.Rotation.Q = r.Q
    
                    self.horizontalSlider.setMaximum(len(pointsDirection))
                    self.DS_horizontalSlider.setMaximum(int(len(pointsDirection)/10))
                    self.DS_horizontalSlider.setValue(len(pointsDirection)/10)
    
#                    self.groupBox_04.setEnabled(True)
#                    self.groupBox_04.setStyleSheet("background-color: white;\n"
#                                                   "border:2px solid rgb(0, 187, 0);")   # bord white and green
                else:
                    plr = "xx"
    
#                self.groupBox_04.setTitle("Position (" + str(len(sel)) + ")(Points: " + str(len(pointsDirection)) + ")")
            except Exception:
                App.Console.PrintError("Error selection " + "\n")
                switchReverse = 0
                sel = ""
            FreeCAD.ActiveDocument.recompute()
            FreeCADGui.updateGui()                                             # rafraichi l'ecran
            Gui.updateGui()                                                    # rafraichi l'ecran
        ############ Section object selected End ######################################################

            self.PU_Accept_Value.setVisible(False)
            self.PBA_progressBar.setVisible(True)
            self.PBA_progressBar.setMaximum(numberSpires * (360 / int(precision)))
            self.PBA_progressBar.setValue(0)
    
            coor_X = coor_Y = coor_Z = 0.0
            angleTr  = 0
            points   = []
            del   points[:]
            pas2 = 0.0
            PBA = 0                                                            # compteur PgrogressBar
            App.Console.PrintMessage("____________________"+"\n")
            App.Console.PrintMessage("Pitch       " + str(pas)+"\n")
            App.Console.PrintMessage("Radius      " + str(rayon)+"\n")
            App.Console.PrintMessage("Precision   " + str(precision)+"\n")
            App.Console.PrintMessage("DebutAngle  " + str(debutAngle)+"\n")
            App.Console.PrintMessage("FinAngle    " + str(finAngle)+"\n")
            App.Console.PrintMessage("List Helix  " + str(helixS)+"\n")
            App.Console.PrintMessage("List Radius " + str(radiusS)+"\n")
            App.Console.PrintMessage("List Smoot1 " + str(lissageS)+"\n")
    
            for spir in range(numberSpires-spireConeComp):                     # number spires Helix
                pas2 = helixS[spir]
                PBA += 1
    
                if spir != numberSpires - 1:                                   # pas travail normal
                    pastr = ((radiusS[spir + 1]-radiusS[spir]) / (360/precision))
                elif spireConeUne == 1:                                        # cone une seule spire
                    pastr = (radius_2_Cone / (360/precision))
                else:
                    pastr = 0.0
    
                pasRadius = radiusS[spir]                                      # pas pour le rayon
                i = 0
                debutAngleX = 0
                finAngleX   = 360
    
                if modifyAngle == 1:
                    if (spir == 0) :
                        debutAngleX = debutAngle
    
                if (spir == numberSpires - 1 - spireConeComp): #or (spir == numberSpires):
                    finAngleX  = finAngle + int(precision)
    
                for angleTr in range(0,finAngleX,int(precision)):              # boucle for 1 turn (360/precision) degrees
                    pasRadius = radiusS[spir]+((pastr*i))
                    i+=1
                    self.PBA_progressBar.setValue( PBA )
                    PBA += 1
                    
                    vecligne=[FreeCAD.Vector(0,0,0),FreeCAD.Vector(pasRadius ,0.0,0.0)]
                    ligne = Draft.makeWire(vecligne,closed=False,face=False,support=None) #creation de la ligne de base
                    #ligneName = ligne.Name

                    if spireReverse == 0:                                      # counterclockwise
                        ligne.Placement = FreeCAD.ActiveDocument.Line.Placement=App.Placement(App.Vector(0.0,0.0,0.0), App.Rotation(App.Vector(0,0,1),angleTr), App.Vector(0,0,0))
                    else:                                                      # clockwise direction
                        ligne.Placement = FreeCAD.ActiveDocument.Line.Placement=App.Placement(App.Vector(0.0,0.0,0.0), App.Rotation(App.Vector(0,0,1),-angleTr), App.Vector(0,0,0))

                    try:
                        a = ligne.Shape.Edges[0].Vertexes[1]                       # fin de ligne
                    except Exception:
                        a = ligne.End                                              # fin de ligne

                    try:
                        coor_X = (a.Point.x)
                        coor_Y = (a.Point.y)
                    except Exception:
                        coor_X = (a.x)
                        coor_Y = (a.y)
    
                    if angleTr >= debutAngleX:
                        points += [FreeCAD.Vector(coor_X,coor_Y,coor_Z)]       # coordinates makeBSpline contener
    
                    if (affPoint == 1) and (angleTr >= debutAngleX):
                        point = Draft.makePoint(coor_X,coor_Y,coor_Z)          # create point repere for test
                        FreeCADGui.activeDocument().getObject(point.Name).PointColor = (1.0,0.0,0.0)
    
                    coor_Z += (pas2 / (360/precision))                         # pas of spring
                    
                    App.ActiveDocument.removeObject(ligne.Name)                # remove ligne de base directrice
                    #App.ActiveDocument.removeObject(ligneName)                # remove ligne de base directrice

            ############# Smooting begin  ### prototype#############################################################################################
    
            if (numberSpires >= 2) and (sum(lissageS[:]) != 0):
    
                compBar = compBar1 = 0                                         # progressBar
                compBar = sum(lissageS[:])                                     # progressBar
                self.PBA_progressBar.setMaximum(compBar)                       # progressBar
                self.PBA_progressBar.setValue(0)                               # progressBar
        
                decalageM = 0                                                  # decalage montant
                pointTravailBase = int(360/precision)                          # nombre de points dans la boucle
        
                if debutAngle != 0:
                    decalageM = (pointTravailBase - int((360-debutAngle)/precision)) # decalageM debutAngle
                    if lissageS[0] != 0:                                                           # lissage spire 1
                        if lissageS[0] > int((360-debutAngle)/precision):
                            lissageS[0] = int((360-debutAngle)/precision) - 1

                    if (lissageS[1] != 0):                                                         # lissage spire 2
                        if lissageS[1] > int((360-debutAngle)/precision):
                            lissageS[1] = int((360-debutAngle)/precision) - 1
    
                if finAngle != 360:
                    if lissageS[-1] != 0:                                                          # lissage derniere spire 
                        if lissageS[-1] > (pointTravailBase - int((360-finAngle)/precision)):
                            lissageS[-1] = (pointTravailBase - int((360-finAngle)/precision)) - 1
    
                    if lissageS[-2] != 0:                                                          # lissage avant derniere spire 
                        if lissageS[-2] > (pointTravailBase - int((360-finAngle)/precision)):
                            lissageS[-2] = (pointTravailBase - int((360-finAngle)/precision)) - 1

                    try:
                        if (lissageS[-3] != 0) and ((spireConeUne == 1) or (spireConeComp == 1)):  # lissage avant derniere spire cas cone (N_spire-1)
                            if lissageS[-3] > (pointTravailBase - int((360-finAngle)/precision)):
                                lissageS[-3] = (pointTravailBase - int((360-finAngle)/precision)) - 1
                    except Exception:
                        None
                        App.Console.PrintError("Error0 smooting"+"\n")

                ############################################# lissage Gauche Superieur
    
                x0 = 2                                                         # division premiere spire
                x1 = 0                                                         # avance G/D
                x2 = 1                                                         # largeur en points
                x3 = 2                                                         # division  

                for ii in range(1 , numberSpires):
                    pointTravail = pointTravailBase * ii
                    compBar1 += 1                                              # progressBar
                    self.PBA_progressBar.setValue(compBar1)                    # progressBar
                   
                    if lissageS[ii-1] != 0:
                        x1 = 0    # avance G/D
                        boucler = lissageS[ii-1]
    
                        if (ii-1 == 0) and (debutAngle != 0):                  # nombre de points
                            if (boucler) > (pointTravailBase - int((360-debutAngle)/precision)):
                                boucler = lissageS[0] - (pointTravailBase - int((360-debutAngle)/precision))
    
                        try:
                            for i in (range(boucler)):
                                compBar1 += 1                                             # progressBar
                                self.PBA_progressBar.setValue(compBar1)                   # progressBar
                                if i == 0:
                                    a = points[pointTravail-1-decalageM][2]  # G          # C
                                    b = points[pointTravail+1-decalageM][2]  # D          # C
                                    c = (((b - a)/x0) + a)                                # C
                                    points[pointTravail+(i)-decalageM][2] = c             # C
                                else:
                                    x1 += 1
                                    a = points[pointTravail+(x1-x2)-decalageM][2]  # G    # D
                                    b = points[pointTravail+(x1+x2)-decalageM][2]  # D    # D
                                    c = (((b - a)/x3) + a)                      # D
                                    points[pointTravail+(x1)-decalageM][2] = c            # D
            
                                    a = points[pointTravail+(-x1-x2)-decalageM][2]  # G   # G
                                    b = points[pointTravail+(-x1+x2)-decalageM][2]  # D   # G
                                    c = (((b - a)/x3) + a)                                # G
                                    points[pointTravail+(-x1)-decalageM][2] = c           # G
                        except Exception:
                            App.Console.PrintError("Error1 smooting coil num : "+str(ii)+"  value : "+str(lissageS[ii-1])+"\n"+
                                                   "Choose a lower smoothing value"+"\n")
        
                ############################################# lissage Droit Inferieur

                compBar1 = 0
                for ii in range(1 , numberSpires):
                    pointTravail = pointTravailBase * (ii )
                    compBar1 += 1                                              # progressBar
                    self.PBA_progressBar.setValue(compBar1)                    # progressBar
        
                    if lissageS[ii] != 0:
                        x1 = 0    # avance G/D
                        boucler = lissageS[ii]
        
                        try:
                            for i in (range(boucler)):
                                compBar1 += 1                                  # progressBar
                                self.PBA_progressBar.setValue(compBar1)        # progressBar
                                if i == 0:
                                    a = points[pointTravail-1-decalageM][2]  # G         # C
                                    b = points[pointTravail+1-decalageM][2]  # D         # C
                                    c = (((a - b)/x0) + b)                               # C
                                    points[pointTravail+(i)-decalageM][2] = c            # C
                                else:
                                    #############################################             # lissage Gauche Sup
                                    x1 += 1
                                    a = points[pointTravail+(x1-x2)-decalageM][2]  # G   # D
                                    b = points[pointTravail+(x1+x2)-decalageM][2]  # D   # D
                                    c = (((a - b)/x3) + b)                         # D
                                    points[pointTravail+(x1)-decalageM][2] = c           # D
            
                                    a = points[pointTravail+(-x1-x2)-decalageM][2]  # G  # G
                                    b = points[pointTravail+(-x1+x2)-decalageM][2]  # D  # G
                                    c = (((a - b)/x3) + b)                          # G
                                    points[pointTravail+(-x1)-decalageM][2] = c          # G
                        except Exception:
                            App.Console.PrintError("Error2 smooting coil num : "+str(ii)+"  value : "+str(lissageS[ii-1])+"\n"+
                                                   "Choose a lower smoothing value"+"\n")
    
                App.Console.PrintMessage("List Smoot2 " + str(lissageS)+"\n")
                App.Console.PrintMessage("____________________"+"\n")
    
            ############ Smooting end ##########################################################################################################
    
            if typeLine == 1:
                ressort = Draft.makeWire(points,closed=False,face=False,support=None)# creation spring makeWire
            else:
                ressort = Draft.makeBSpline(points,closed=False)               # creation spring Draft " makeBSpline " remis pour facilite avec axes
#                ressortT = Part.BSplineCurve()          ##                    # creation spring Part  " BSplineCurve "
#                ressortT.interpolate(points,False)      ##
#                ressort = Part.Edge(ressortT)           ##
#                Part.show(ressort)                      ##

            if (plr != "xx") and (len(pointsDirection)!= 0):                   # placement if axis selected
                pointsDirection.reverse()
                plr.Base = pointsDirection[-1]#
                ressort.Placement = plr
                self.horizontalSlider.setValue(0)

            if nomF != "Name File": # name file
                App.ActiveDocument.ActiveObject.Label =  "Spring_" + nomF
            else:
                App.ActiveDocument.ActiveObject.Label =  "Spring (" + str(rayon) + " r)"

            try:
                FCSpring.addObject(ressort)
                FCSpring.Label = "Spring (" + str(rayon) + " r)"
            except Exception:
                None
            FreeCAD.ActiveDocument.recompute()
    
            self.PBA_progressBar.setVisible(False)
            self.PU_Accept_Value.setVisible(True)

            #### Chrono(1) end #################################
            chrono(1)                 # chrono(1) end         ##
            ####################################################

        else:
            App.Console.PrintError("Radius zero not allowed do"+"\n")
            self.textEdit.setTextColor(QColor("red"))
            self.textEdit.append("Radius zero not allowed do " )
            self.textEdit.setTextColor(QColor("Base"))
####on_PU_Launch end ###################################################################################

    def selectOk(self, val):
        global switchAdaptRadius
        global centerFaceOrPoint
        global sel
        global vecteurSouris
        global selectedCircle

        try:
            sel = FreeCADGui.Selection.getSelectionEx()                                # display the type line selected
            self.textEdit.append(str(sel[0].SubObjects[0].Curve))
        except Exception:
            try:
                self.textEdit.append(str(sel[0].SubObjects[0].Surface))
            except Exception:
                None
        if val == 1:
            self.PB_Adapt_Radius.setEnabled(True)
            self.PB_Adapt_Radius.setStyleSheet("background-color: white;\n"
                                               "border:2px solid rgb(0, 187, 0);")     # bord white and green
            self.PB_Center_Point.setEnabled(True)
            self.PB_Center_Point.setStyleSheet("background-color: white;\n"
                                               "border:2px solid rgb(0, 187, 0);")     # bord white and green
            if len(sel) == 2:
                self.CB_Position.setEnabled(True)
                self.CB_Position.setStyleSheet("background-color: white;\n"
                                               "border:2px solid rgb(0, 187, 0);")     # bord white and green
            if len(selectedCircle) == 3:
                self.PB_CreaCircle.setEnabled(True)
                self.PB_CreaCircle.setStyleSheet("background-color: white;\n"
                                               "border:2px solid rgb(0, 187, 0);")     # bord white and green
            elif len(selectedCircle) > 3:
                self.PB_CreaCircle.setEnabled(False)
                self.PB_CreaCircle.setStyleSheet("background-color: QPalette.Base")    # origin system
                del selectedCircle[:]
        else:
            self.PB_Adapt_Radius.setEnabled(False)
            self.PB_Adapt_Radius.setChecked(False)
            self.PB_Adapt_Radius.setStyleSheet("background-color: QPalette.Base")      # origin system
            self.PB_Adapt_Radius.setText("Normal")
            switchAdaptRadius = 0
            self.PB_Center_Point.setEnabled(False)
            self.PB_Center_Point.setChecked(False)
            self.PB_Center_Point.setStyleSheet("background-color: QPalette.Base")      # origin system
            self.PB_Center_Point.setText(_fromUtf8("Point Mouse"))
            centerFaceOrPoint = 0
            self.CB_Position.setEnabled(False)
            self.CB_Position.setChecked(False)
            self.CB_Position.setStyleSheet("background-color: QPalette.Base")          # origin system
            self.PB_CreaCircle.setEnabled(False)
            self.PB_CreaCircle.setChecked(False)
            self.PB_CreaCircle.setStyleSheet("background-color: QPalette.Base")        # origin system
        switchAdaptRadius = 0
        self.groupBox_04.setTitle("Position (" + str(len(sel)) + ")") #(Points: " + str(len(pointsDirection)) + ")

    def on_CB_05_Position(self):
        global FCmw
        global seTPositionFlyRightLeft
        global seTWidgetPosition

        if seTPositionFlyRightLeft != 1:
            if self.CB_05_Position.isChecked():
                FCmw.addDockWidget(QtCore.Qt.LeftDockWidgetArea,myNewFreeCADWidget) # add the widget to the main window Left
                FreeCAD.ParamGet(u"User parameter:BaseApp/Preferences/Macros/FCMmacros/" + __Title__).SetInt(u"seTPositionFlyRightLeft", 3)     #*1, 2, other
                FreeCAD.ParamGet(u"User parameter:BaseApp/Preferences/Macros/FCMmacros/" + __Title__).SetBool(u"seTWidgetPosition", True)       # True or False
            else:
                FCmw.addDockWidget(QtCore.Qt.RightDockWidgetArea,myNewFreeCADWidget)# add the widget to the main window Right
                FreeCAD.ParamGet(u"User parameter:BaseApp/Preferences/Macros/FCMmacros/" + __Title__).SetInt(u"seTPositionFlyRightLeft", 2)     #*1, 2, other
                FreeCAD.ParamGet(u"User parameter:BaseApp/Preferences/Macros/FCMmacros/" + __Title__).SetBool(u"seTWidgetPosition", False)      # True or False

    def on_PU_Help(self):
        WebGui.openBrowser("http://www.freecadweb.org/wiki/index.php?title=Macro_FCSpring_Helix_Variable")
        App.Console.PrintMessage("http://www.freecadweb.org/wiki/index.php?title=Macro_FCSpring_Helix_Variable" + "\n")
    
class SelObserver:
    print( "run.." )
    def addSelection(self,document, object, element, position):                # Selection
        global ui
        global vecteurSouris
        global selectedCircle

        vecteurSouris = FreeCAD.Vector(position)
        selectedCircle.append(vecteurSouris)
        ff = ui
        ff.selectOk(1)
#        App.Console.PrintMessage("addSelection"+"\n")
    def clearSelection(self,doc):                                              # Si clic sur l'ecran, effacer la selection
        global ui
        global selectedCircle

        del selectedCircle[:]
        ff = ui
        ff.selectOk(0)

doc = FreeCAD.ActiveDocument
if doc == None:
    doc = FreeCAD.newDocument(__Title__)

helixS = []
del helixS[:]
helixS = numberSpires*[pas]
radiusS = []
del radiusS[:]
radiusS = numberSpires*[rayon]
lissageS = []
del lissageS[:]
lissageS = numberSpires*[0]

s=SelObserver()
FreeCADGui.Selection.addObserver(s)          # installe the function in resident mode

#MainWindow = QtWidgets.QMainWindow()
#MainWindow.setObjectName(__Title__)          # macro internal Name
#ui = Ui_MainWindow()
#ui.setupUi(MainWindow)
#MainWindow.show()

mw = FreeCADGui.getMainWindow()
dw=mw.findChildren(QtWidgets.QDockWidget)

for i in dw:
    if str(i.objectName()) == __Title__:
        if i.isVisible():
            i.setVisible(False)
        else:
            if seTPositionFlyRightLeft == 1:                 # MainWindow
                None
            else:
                myNewFreeCADWidget = QtWidgets.QDockWidget() # create (restore) a new dockwidget
                myNewFreeCADWidget.setObjectName(__Title__)
                ui = Ui_MainWindow()
                ui.setupUi(myNewFreeCADWidget)
                FCmw = FreeCADGui.getMainWindow()
                i.setVisible(True)
        break

if i.objectName() != __Title__:                              # macro internal Name
    #
    #####MainWindow################################################################################
    if seTPositionFlyRightLeft == 1:                 # MainWindow
        MainWindow = QtWidgets.QMainWindow()         # create a new window volant
        MainWindow.setObjectName(__Title__)          # macro internal Name
        ui = Ui_MainWindow()
        ui.setupUi(MainWindow)
        MainWindow.show()
    #####DockWidget################################################################################
    #
    else:
        myNewFreeCADWidget = QtWidgets.QDockWidget() # create a new dockwidget
        myNewFreeCADWidget.setObjectName(__Title__)
        ui = Ui_MainWindow()
        ui.setupUi(myNewFreeCADWidget)
        FCmw = FreeCADGui.getMainWindow()
        if seTPositionFlyRightLeft == 2:             # RightDock
            FCmw.addDockWidget(QtCore.Qt.RightDockWidgetArea,myNewFreeCADWidget) # add the widget to the main window Right
        else:                                        # LeftDock
            FCmw.addDockWidget(QtCore.Qt.LeftDockWidgetArea,myNewFreeCADWidget)  # add the widget to the main window Left

