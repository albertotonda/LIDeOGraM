import numpy as np


class Dataset:

    def __init__(self,datafile, constmodel="data/cmdl"):
        self.ctmod = constmodel
        datafileReader = open(datafile)
        line = datafileReader.readline()  # First line are the variables name
        self.varnames = []
        for i in line.split(','):
            self.varnames.append(i.strip())
        print(len(self.varnames))
        self.varnames=np.array(self.varnames)
        self.nbVar = len(self.varnames)
        line = datafileReader.readline()  # Second line is variables scale/step identifiers
        identvar = []
        for i in line.split(','):
            identvar.append(i.strip())
        print(len(identvar))
        self.variablesClass = {}
        for i in range(len(self.varnames)):
            self.variablesClass[self.varnames[i]] = identvar[i]

        line = datafileReader.readline() # Third line is the variable uncertainty of measurement
        uncertVar=[]
        for i in line.split(','):
            print(i)
            uncertVar.append((float(i.strip())))
        self.variablesUncertainty={}
        for i in range(len(self.varnames)):
            self.variablesUncertainty[self.varnames[i]] = uncertVar[i]

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

        self.classesIn=[]
        self.varsIn=[]

        self.true_varnames=self.varnames
        self.true_nbVar = self.nbVar
        self.true_variablesClass=self.variablesClass
        self.true_data=self.data
        self.true_nbExp=self.nbExp
        self.varnames_extd = None
        self.data_extd = None





    def getAllExpsforVar(self,getvar):
        return self.data[:,self.varnames==getvar].flatten()

    def getAllVarsforExp(self,getexp):
        return dict(zip(self.varnames,self.data[getexp]))
