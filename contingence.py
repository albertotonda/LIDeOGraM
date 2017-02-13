#-*- coding: utf-8
import sys
from collections import Counter

import pandas as pd
from PyQt4.QtCore import *
from PyQt4.QtGui import *

import pandas as pd

import re
col=['cmplx','fit','varcalc','eq','num']
datum = pd.read_csv("data/equa_with_col_Parent_withMol.csv",header=None)
datum = datum.sort(2)
variables = ["Temperature", "Age"]+sorted(datum[2].unique().tolist())



def getV(variables, line, v):
    table = []
    for i in variables:
        #g = "\W"+i+"\W"
        #if re.search(g, line):
        if(re.findall(r'\b%s\b' % re.escape(i),line)):
        #if i in line:
            table.append(1)
        elif v == i:
            table.append(-1)
        else:
            table.append(0)
    #print(v)
    #print(table)
    return table

df_ = pd.DataFrame(index=datum[2], columns=["Temperature", "Age"]+datum[2].unique().tolist())
for row in range (df_.shape[0]):
    v = df_.index.values[row]
    print(v)
    print(datum.irow(row)[3])
    df_.ix[row] = getV(df_.columns.values,datum.irow(row)[3],v)


data = df_
app = QApplication(sys.argv)
table = QTableWidget()
tableItem = QTableWidgetItem()

shape = data.shape

    # initiate table
table.setWindowTitle("Tableau de correspondance")
table.resize(*shape)
table.setRowCount(len(data.index))
table.setColumnCount(len(data.columns))

    # set label
table.setHorizontalHeaderLabels(data.columns.values)
table.setVerticalHeaderLabels(data.index.tolist())


for i in range(shape[0]):
    table.setRowHeight(i,15)
    for j in range(shape[1]):
        table.setColumnWidth(j,15)
        fnt = QFont()
        fnt.setPointSize(5)
        value = data.ix[i,j]
        cell = QTableWidgetItem(value)
        cell.setFont(fnt)
        color = None
        if value == 1:
            color = QColor.fromRgb(255,0,0)
        elif value == -1:
            color = QColor.fromRgb(0,0,255)
        else:
            color = QColor.fromRgb(255,255,255)
        cell.setBackgroundColor(color)
        cell.setToolTip(datum.irow(i)[3])
        table.setItem(i,j,cell)

 # tooltip text
table.horizontalHeaderItem(0).setToolTip("Column 1 ")
table.horizontalHeaderItem(1).setToolTip("Column 2 ")

# show table
table.show()
app.exec_()
