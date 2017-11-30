#-*- coding: utf-8
import sys
from collections import Counter

import pandas as pd
from PyQt4.QtCore import *
from PyQt4.QtGui import *

import pandas as pd

import re


from PyQt4.QtGui import *
from PyQt4.QtCore import Qt


class MyHeaderView(QHeaderView):

     def __init__(self, parent=None):
         super().__init__(Qt.Horizontal, parent)
         self._font = QFont("helvetica", 8)
         self._metrics = QFontMetrics(self._font)
         self._descent = self._metrics.descent()
         self._margin = 10

     def paintSection(self, painter, rect, index):
         data = self._get_data(index)
         painter.rotate(-90)
         painter.setFont(self._font)
         painter.drawText(- rect.height() + self._margin,
                          rect.left() + (rect.width() + self._descent) / 2, data)

     def sizeHint(self):
         return QSize(0, self._get_text_width() + 2 * self._margin)

     def _get_text_width(self):
         return max([self._metrics.width(self._get_data(i))
                     for i in range(0, self.model().columnCount())])

     def _get_data(self, index):
         return self.model().headerData(index, self.orientation())


class IncMatrixCanvas(QTableWidget):
    def __init__(self, modApp, vwApp):
        self.modApp = modApp
        self.vwApp = vwApp
        QTableWidget.__init__(self)
        #self.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.lastSelected = ""
        self.lastSelectedRows = ""

        self.setSelectionMode(QAbstractItemView.NoSelection)

        #style = """
        #QTableWidget::item{ background-color: rgba(255, 0, 0, 50%);
        #"""

        #self.setStyleSheet("QTableView::item:selected{  background: rgba(255, 0, 0, 50%); }")
        #self.setStyleSheet("QTableView{background-color: rgba(255, 255, 255, 50%)};")


        # initiate table
        self.setWindowTitle("Tableau de correspondance")
        self.setRowCount(len(self.modApp.dataIncMat.index))
        self.setColumnCount(len(self.modApp.dataIncMat.columns)+3)

        # set label
        headerView = MyHeaderView()
        self.setHorizontalHeader(headerView)
        self.setHorizontalHeaderLabels(["Complexity","Fitness","Name"]+self.modApp.dataIncMat.columns.values.tolist())
        self.verticalHeader().hide()

        self.order = self.modApp.dataIncMat.index
        self.colorClasses = dict(zip(self.modApp.dataset.varnames, self.modApp.nodeColor))

        self.newOrder = list(range(self.modApp.shapeIncMat[0]))


        for i in range(self.modApp.shapeIncMat[0]):
            self.setRowHeight(i, 15)
            for j in range(self.modApp.shapeIncMat[1]+3):
                if j == 0:
                    self.setColumnWidth(j, 15)
                    cmap = self.modApp.colors.get("complexity",self.modApp.data[i][0]/self.modApp.cmplxMax)
                    color = QColor.fromRgb(*cmap)
                    cell = QTableWidgetItem(self.modApp.dataIncMat.index.tolist()[i])
                    cell.setBackgroundColor(color)
                    cell.setToolTip(self.modApp.datumIncMat.iloc[i][3])
                    self.setItem(i, j, cell)
                    continue
                if j == 1:
                    self.setColumnWidth(j, 15)
                    color = QColor.fromRgb(0, 255, 0)
                    cell = QTableWidgetItem(self.modApp.dataIncMat.index.tolist()[i])
                    cell.setBackgroundColor(color)
                    cell.setToolTip(self.modApp.datumIncMat.iloc[i][3])
                    self.setItem(i, j, cell)
                    continue

                if j == 2:
                    cell = QTableWidgetItem(self.modApp.dataIncMat.index.tolist()[i])
                    cell.setBackgroundColor(QColor.fromRgb(255,255,255,255))
                    self.setItem(i, j, cell)
                    continue
                self.setColumnWidth(j, 15)
                fnt = QFont()
                fnt.setPointSize(5)
                value = self.modApp.dataIncMat.ix[i, j-3]
                cell = QTableWidgetItem(value)
                cell.setFont(fnt)
                if value == 1:
                    color = QColor.fromRgb(180,180,180)
                elif value == -1:
                    try:
                        c = self.colorClasses[self.order[i]]
                    except:
                        pass
                    color = QColor.fromRgb(*[int(i * 255) for i in c])
                else:
                    color = QColor.fromRgb(255, 255, 255)
                cell.setBackgroundColor(color)
                cell.setToolTip(self.modApp.datumIncMat.iloc[i][3])
                self.setItem(i, j, cell)

        self.show()



    def updateView(self):
        best_ind = self.modApp.best_indv
        if best_ind == []: return
        tableOrder = self.modApp.dataIncMat.columns
        eqs = []
        for place, col in enumerate(tableOrder):
            if col in self.modApp.dataset.varsIn: continue
            eqs.append(self.modApp.dataIncMat.index.tolist().index(col)+int(best_ind[col]))
        l = len(self.modApp.dataIncMat.index.tolist())
        gmodelSize = len(eqs)
        diff = set(range(l)) - set(eqs)
        others = list(sorted(list(diff)))
        self.newOrder = eqs+others
        for i in others:
            eqs.append(i)
        #eqs contiens maintenant normalement le nouvel ordonanamcement.
        nameOrder = []
        for i in eqs:
            nameOrder.append(self.modApp.dataIncMat.index.tolist()[i])
        self.order = nameOrder

        for i,k in enumerate(eqs) : #range(self.modApp.shapeIncMat[0]):
            self.setRowHeight(i, 15)
            for j in range(self.modApp.shapeIncMat[1] + 3):
                if j == 0:
                    self.setColumnWidth(j, 15)
                    cmap = self.modApp.colors.get("complexity",self.modApp.equacolO[eqs[i],0] / self.modApp.cmplxMax)
                    color = QColor.fromRgb(*cmap)
                    cell = QTableWidgetItem(self.modApp.dataIncMat.index.tolist()[i])
                    cell.setBackgroundColor(color)
                    cell.setToolTip(self.modApp.datumIncMat.iloc[i][3])
                    self.setItem(i, j, cell)
                    continue
                if j == 1:
                    self.setColumnWidth(j, 15)
                    value = self.modApp.globErrDet[nameOrder[i]]

                    if i < gmodelSize:
                        cmap = self.modApp.colors.get("global", value)
                    else:
                        cmap=[255,255,255]
                    color = QColor.fromRgb(*cmap)
                    cell = QTableWidgetItem(self.modApp.dataIncMat.index.tolist()[i])
                    cell.setBackgroundColor(color)
                    cell.setToolTip(self.modApp.datumIncMat.iloc[i][3])
                    self.setItem(i, j, cell)
                    continue

                if j == 2:
                    if i < gmodelSize:
                        t = [0, 0, 0]
                    else:
                        t = [125, 125, 125]
                    cell = QTableWidgetItem(nameOrder[i])
                    cell.setBackgroundColor(QColor.fromRgb(255,255,255,255))
                    cell.setTextColor(QColor.fromRgb(*t))
                    self.setItem(i, j, cell)
                    continue
                self.setColumnWidth(j, 15)
                fnt = QFont()
                fnt.setPointSize(5)
                value = self.modApp.dataIncMat.iloc[k, j-3]
                cell = QTableWidgetItem(value)
                cell.setFont(fnt)

                #Si on depasse gmodelSize, nous ne somme plus dans le model global mais dans les restes, on attenu donc la couleurs
                g = [180, 180, 180]
                b = self.colorClasses[nameOrder[i]]#[8, 104, 172]
                b = [int(i * 255) for i in b]
                if i >= gmodelSize:
                    mash = 0.4
                    g = list(map(lambda x : (x + (255-x)*(1-mash)), g))
                    b = list(map(lambda x : (x + (255-x)*(1-mash)), b))

                if value == 1:
                    color = QColor.fromRgb(*g)
                elif value == -1:
                    color = QColor.fromRgb(*b)
                else:
                    color = QColor.fromRgb(255, 255, 255)
                cell.setBackgroundColor(color)
                cell.setToolTip(self.modApp.datumIncMat.iloc[i][3])
                self.setItem(i, j, cell)

        self.show()

    def selected(self,value : str):
        if value == None:
            #resetSelection
            pass
        pass

    def highlight(self, value : int):
        if self.lastSelected :
            for i in range(len(self.modApp.dataIncMat.columns) + 3):
                cell = self.item(self.lastSelected, i)
                color = cell.background().color().getRgb()
                if color == (190, 190, 190, 255):
                    color = [255, 255, 255, 255]
                    cell.setBackgroundColor(QColor.fromRgb(*color))
                else:
                    color = [int((255 / 190) * i) for i in color[:-1]]
                    color.append(255)
                    cell.setBackgroundColor(QColor.fromRgb(*color[:-1]))
        if value == -1:
            self.lastSelected = False
            return
        self.lastSelected = value
        for i in range(len(self.modApp.dataIncMat.columns)+3):
            cell = self.item(value, i)
            color = cell.background().color().getRgb()
            if color == (255,255,255,255):
                color = [190,190,190,125]
                cell.setBackgroundColor(QColor.fromRgb(*color))
            else:
                color = [int((190/255)*i) for i in color[:-1]]
                color.append(255)
                cell.setBackgroundColor(QColor.fromRgb(*color))

    def mutipleHighlight(self, label: str):
        if self.lastSelectedRows:
            for row in self.lastSelectedRows:
                for i in range(len(self.modApp.dataIncMat.columns) + 3):
                    cell = self.item(row, i)
                    color = cell.background().color().getRgb()
                    if color == (190, 190, 190, 255):
                        color = [255, 255, 255, 255]
                        cell.setBackgroundColor(QColor.fromRgb(*color[:-1]))
                    else:
                        color = [int((255 / 190) * i) for i in color]
                        cell.setBackgroundColor(QColor.fromRgb(*color[:-1]))
        if label == -1:
            self.lastSelectedRows = ""
            return
        #temporaryDataFrame = self.modApp.dataIncMat
        #temporaryDataFrame["idx"] = temporaryDataFrame.index
        #rows = temporaryDataFrame.idx == label  # True False Serie ?
        matchingRows = []
        for i, j in enumerate(self.order):
            if j == label:
                matchingRows.append(i)
        self.lastSelectedRows = matchingRows
        for row in matchingRows:
            for i in range(len(self.modApp.dataIncMat.columns) + 3):
                cell = self.item(row, i)
                color = cell.background().color().getRgb()
                if color == (255, 255, 255, 255):
                    color = [190, 190, 190, 125]
                    cell.setBackgroundColor(QColor.fromRgb(*color[:-1]))
                else:
                    color = [int((190 / 255) * i) for i in color]
                    cell.setBackgroundColor(QColor.fromRgb(*color[:-1]))

    def StructureChange(self):
        pass



