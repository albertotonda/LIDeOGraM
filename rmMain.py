#-*- coding: utf-8
from randomModels import RandomModels
import argparse
import os
from RFGraph_Controller import RFGraph_Controller

parser = argparse.ArgumentParser()
parser.add_argument("folder")
args = parser.parse_args([r"""C:\Users\marc\CloudStation\alberto\RandomModels\rModels"""])

lst = os.listdir(args.folder+r"\data_std")

for _ in lst:
    _ = args.folder+"\\" +"data_std\\" + _
    RandomModels(_, output=args.folder+r'\opt', cgraph=(_+"_cmdl").replace("data_std","ctgraph"))

#modApp=RandomModels(args.mdl, output=args.folder+'/opt')
#vwApp = RFGraph_View(modApp)
#cntrApp=RFGraph_Controller(modApp,vwApp)
#vwApp.cntrApp=cntrApp
#vwApp.eqTableGUI.cntrApp=cntrApp
#vwApp.updateMenuBar(cntrApp)
#qtconnector=QtConnector(vwApp,cntrApp)
