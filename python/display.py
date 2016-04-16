#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
import time
import os
import signal

from PyQt4 import QtGui, QtCore

#import socket

class GUI(QtGui.QMainWindow):
    def __init__(self, rsock, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        try: self.setAttribute(QtCore.Qt.WA_Maemo5StackedWindow)
        except: pass
        self.setWindowTitle("Test GUI")
        self.cw = QtGui.QWidget(self)
        self.setCentralWidget(self.cw)
        self.sigusr = QtCore.QSocketNotifier(rsock.fileno(), QtCore.QSocketNotifier.Read)
        self.connect(self.sigusr, QtCore.SIGNAL("activated(int)"), self.show)
        print("GUI is set up")


def listSignals(signal):
    signals_to_names = {}
    for n in dir(signal):
        if n.startswith('SIG') and not n.startswith('SIG_'):
            signals_to_names[getattr(signal, n)] = n

    for s, name in sorted(signals_to_names.items()):
        handler = signal.getsignal(s)
        if handler is signal.SIG_DFL:
            handler = 'SIG_DFL'
        elif handler is signal.SIG_IGN:
            handler = 'SIG_IGN'
        print '%-10s (%2d):' % (name, s), handler


def statusupdate( ):
    """
    Writes the time update into the status line
    """
    t = time.strftime("%Y-%m-%d %H:%M:%S ")
    window.statusBar().showMessage( t )
    #print "statusupdate", t


def check4pic( ):
    global sig1, picid
    if sig1:
        #if picid == 0:
        #    picid = 1
        #else:
        #    picid = 0
        LoadPicture()
        sig1 = False




def LoadPicture():
    t = time.strftime("%Y-%m-%d %H:%M:%S ")
    qp = QtGui.QPixmap(pic[picid])
    if qp.depth() > 0: #depth is 0 if pic does not exist or cannot be loaded, then don't change picture
        #print "qpdepth=", qp.depth()
        lpic.setPixmap(qp)
        window.statusBar().showMessage( t + "picture reloaded" )
    else:
        #print "qpdepth=", qp.depth()
        window.statusBar().showMessage( t + "picture NOT found" )
    #time.sleep(1.2)
    window.setWindowTitle(sys.argv[0] + "  pic: "+pic[picid] +" , pid:"+ str(os.getpid()))


# handler for SIGUSR1
def sigusr1_handler(signum, stack):
    global sig1
    #print ' sigusr1_handler Received:', signum,
    sig1 = True
    #print "set sig1 to:", sig1


# handler for SIGINT
def sigint_handler(signum, stack):
    sys.exit(0)


########################################################################################################

if __name__ == "__main__":

    sig1 = False
    picid = 0
    pic=[]
    pic.append(sys.path[0] +"/temp/temp.jpg")
    #pic.append(sys.path[0] +"/temp/my600x400.png")

    app = QtGui.QApplication([""])
    app.setStyleSheet("QLabel {background:pink; color:black ; border-top: 1px solid #000; border-right: 1px solid #bbb} ")

    # Create a new window
    window = QtGui.QMainWindow()
    window.setGeometry(0,00, 200, 100)

    # Set the window title
    window.setWindowTitle(sys.argv[0] + "  pic: "+pic[picid] +" , pid:"+ str(os.getpid()))

    lpic = QtGui.QLabel()
    lpic.setPixmap(QtGui.QPixmap(pic[picid]))

    cw = QtGui.QWidget()

    vbox = QtGui.QVBoxLayout()
    cw.setLayout(vbox)
    vbox.addWidget(lpic)

    #btn = QtGui.QPushButton('Button')
    #btn.setToolTip('This is a <b>QPushButton</b> widget')
    #vbox.addWidget(btn)

    window.setCentralWidget(cw)

    window.statusBar().showMessage(time.strftime("%Y-%m-%d %H:%M:%S"))
    window.show()

    signal.signal(signal.SIGUSR1, sigusr1_handler)
    signal.signal(signal.SIGINT, sigint_handler)


    timer = QtCore.QTimer()
    timer.connect(timer, QtCore.SIGNAL("timeout()"), statusupdate)
    timer.start(1000)

    #listSignals(signal)
    timer2 = QtCore.QTimer()
    timer2.connect(timer2, QtCore.SIGNAL("timeout()"), check4pic)
    timer2.start(50)

    app.exec_()
