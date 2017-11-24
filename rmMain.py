#-*- coding: utf-8
from randomModels import RandomModels
import argparse
import os
from multiprocessing import Pool
from RFGraph_Controller import RFGraph_Controller

parser = argparse.ArgumentParser()
parser.add_argument("folder")
args = parser.parse_args([r"""C:\Users\marc\CloudStation\alberto\RandomModels\rModels"""])
folder = r"""C:\Users\marc\CloudStation\alberto\RandomModels\rModels"""
#p = Pool(4)

lst = os.listdir(folder+r"\data_std")[1:5]
argsMap = map(lambda x : (folder+"\\data_std\\"+x, folder+r'\opt',(folder+"\\data_std\\"+x+"_cmdl").replace("data_std","ctgraph")), lst)
#print(list(argsMap))
#map(lambda x : RandomModels(x[0], output=x[1], cgraph=x[2]), filter(lambda x: not ".log" in x, argsMap))

largs = list(filter(lambda x: not ".log" in x, argsMap))
s = RandomModels(largs[1][0], largs[1][1], largs[1][2])

#for _ in lst:
#    _ = args.folder+"\\" +"data_std\\" + _
#    RandomModels(_, output=args.folder+r'\opt', cgraph=(_+"_cmdl").replace("data_std","ctgraph"))

#modApp=RandomModels(args.mdl, output=args.folder+'/opt')
#vwApp = RFGraph_View(modApp)
#cntrApp=RFGraph_Controller(modApp,vwApp)
#vwApp.cntrApp=cntrApp
#vwApp.eqTableGUI.cntrApp=cntrApp
#vwApp.updateMenuBar(cntrApp)
#qtconnector=QtConnector(vwApp,cntrApp)
