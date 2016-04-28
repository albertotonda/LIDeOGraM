#-*- coding: utf-8
from RFGraph_View import RFGraph_View
from RFGraph_Model import RFGraph_Model
from RFGraph_Controller import RFGraph_Controller

modApp=RFGraph_Model()
vwApp = RFGraph_View(modApp)
cntrApp=RFGraph_Controller(modApp,vwApp)


