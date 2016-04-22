#-*- coding: utf-8

from PyQt4 import QtGui
import Optimisation
import RFGraph_View as vw
from RFGraph_Model import RFGraph_Model


modApp=RFGraph_Model()
vwApp = vw.RFGraph_View(modApp)


