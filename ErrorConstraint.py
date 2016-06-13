#-*- coding: utf-8
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import *

#TODO Crée la fenêtre d'erreur lors de la mauvaise sélection d'un noeud à contraindre
class ErrorConstraint(QDialog):
   def __init__(self, parent=None):
       super(ErrorConstraint, self).__init__(parent)
       self.setWindowTitle('Selection error')
       self.icon = QtGui.QIcon("iconeLSN")
       self.setWindowIcon(self.icon)
       mainBox = QVBoxLayout(self)
       boxlayout = QHBoxLayout()
       mainBox.addLayout(boxlayout)
       m1 = QVBoxLayout()
       m1.addWidget(QLabel("Wrong node. Please start again."))
       boxlayout.addLayout(m1)

       buttons = QDialogButtonBox(QDialogButtonBox.Ok, QtCore.Qt.Horizontal, self)
       buttons.accepted.connect(self.accept)
       buttons.rejected.connect(self.reject)

       mainBox.addWidget(buttons)

   def params(self):
       return 0

   @staticmethod
   def get_params():
       error = ErrorConstraint()
       message = error.exec_()
       param = error.params()
       return (message, param)