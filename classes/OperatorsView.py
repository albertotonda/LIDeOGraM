from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import *

from PyQt4.QtGui import *

class OperatorsView(QtGui.QMainWindow,QtGui.QGraphicsItem):
    def __init__(self, classnode):

        QtGui.QMainWindow.__init__(self)
        QtGui.QGraphicsItem.__init__(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.classnode=classnode
        self.setWindowTitle("Choose operators for " + classnode.name)
        self.icon = QtGui.QIcon("Icone.png")
        self.setWindowIcon(self.icon)

        self.main_widget = QtGui.QWidget(self)

        self.gridLayout = QtGui.QGridLayout(self.main_widget)
        self.gridLayout.setSpacing(5)

        self.CBexp=QCheckBox()
        self.gridLayout.addWidget(self.CBexp, 0, 0, 1, 1)
        self.Lexp = QtGui.QLabel('Exponentiel')
        self.gridLayout.addWidget(self.Lexp, 0, 1, 1, 1)
        self.CBlog = QCheckBox()
        self.gridLayout.addWidget(self.CBlog, 1, 0, 1, 1)
        self.Llog = QtGui.QLabel('Logarithm')
        self.gridLayout.addWidget(self.Llog, 1, 1, 1, 1)
        self.CBdiv = QCheckBox()
        self.gridLayout.addWidget(self.CBdiv, 2, 0, 1, 1)
        self.Ldiv = QtGui.QLabel('Inverse')
        self.gridLayout.addWidget(self.Ldiv, 2, 1, 1, 1)
        self.CBsq = QCheckBox()
        self.gridLayout.addWidget(self.CBsq, 3, 0, 1, 1)
        self.Lsq = QtGui.QLabel('Square')
        self.gridLayout.addWidget(self.Lsq, 3, 1, 1, 1)
        self.CBmult = QCheckBox()
        self.gridLayout.addWidget(self.CBmult, 4, 0, 1, 1)
        self.Lmult = QtGui.QLabel('Multiplication(x1 * x2)')
        self.gridLayout.addWidget(self.Lmult, 4, 1, 1, 1)

        self.buttonOk = QtGui.QPushButton('Ok', self)
        self.gridLayout.addWidget(self.buttonOk, 5, 1, 1, 1)
        self.buttonCancel = QtGui.QPushButton('Cancel', self)
        self.gridLayout.addWidget(self.buttonCancel, 5, 0, 1, 1)

        if('Exponentiel' in self.classnode.operators):
            self.CBexp.setChecked(True)
        if ('Logarithm' in self.classnode.operators):
            self.CBlog.setChecked(True)
        if ('Inverse' in self.classnode.operators):
            self.CBdiv.setChecked(True)
        if ('Square' in self.classnode.operators):
            self.CBsq.setChecked(True)
        if ('Multiplication(x1 * x2)' in self.classnode.operators):
            self.CBmult.setChecked(True)
        self.buttonOk.clicked.connect(self.OkClicked)
        self.buttonCancel.clicked.connect(self.CancelClicked)

        self.setCentralWidget(self.main_widget)
        QtGui.QMainWindow.show(self)


    def OkClicked(self):
        newOps=[]
        if(self.CBexp.isChecked()):
            newOps.append('Exponentiel')
        if(self.CBlog.isChecked()):
            newOps.append('Logarithm')
        if (self.CBdiv.isChecked()):
            newOps.append('Inverse')
        if (self.CBsq.isChecked()):
            newOps.append('Square')
        if (self.CBsq.isChecked()):
            newOps.append('Multiplication(x1 * x2)')

        self.classnode.operators=newOps
        self.close()



    def CancelClicked(self):
        self.close()