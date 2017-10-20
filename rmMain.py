#-*- coding: utf-8
from randomModels import RandomModels
import argparse
from RFGraph_Controller import RFGraph_Controller

parser = argparse.ArgumentParser()
parser.add_argument("mdl")
args = parser.parse_args(["data/outbig.mdl"])

modApp=RandomModels(args.mdl)
#vwApp = RFGraph_View(modApp)
#cntrApp=RFGraph_Controller(modApp,vwApp)
#vwApp.cntrApp=cntrApp
#vwApp.eqTableGUI.cntrApp=cntrApp
#vwApp.updateMenuBar(cntrApp)
#qtconnector=QtConnector(vwApp,cntrApp)
