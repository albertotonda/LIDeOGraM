import numpy as np
import pandas as pd

class Dataset:

    def __init__(self,datafile):
        datafileReader = open(datafile)
        line = datafileReader.readline()  # First line are the variables name
        self.varnames = []
        for i in line.split(','):
            self.varnames.append(i.strip())
        self.varnames=np.array(self.varnames)
        self.nbVar = len(self.varnames)
        line = datafileReader.readline()  # Second line is variables scale/step identifiers
        identvar = []
        for i in line.split(','):
            identvar.append(i.strip())
        self.variablesClass = {}
        for i in range(len(self.varnames)):
            self.variablesClass[self.varnames[i]] = identvar[i]

        self.data = []
        for line in datafileReader:
            linedata=[]
            for i in line.split(','):
                try:
                    linedata.append(float(i.strip()))
                except ValueError as ve:
                    print("{}".format(ve))
                    print(linedata)
            self.data.append(linedata)
        self.nbExp = len(self.data)
        self.data=np.array(self.data)

        self.nodeDescription = pd.read_csv("data/full_new2_metatranscriptome_Marc_Kegg_COG_ds_21nov16.csv", index_col=0, header=0, sep=";")
        self.nodeDescription = self.nodeDescription[["EC number", 'Product']]
        print("3")




    def getAllExpsforVar(self,getvar):
        return self.data[:,self.varnames==getvar].flatten()

    def getAllVarsforExp(self,getexp):
        return dict(zip(self.varnames,self.data[getexp]))
