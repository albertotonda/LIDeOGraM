#-*- coding: utf-8
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import *
from PyQt4.QtCore import Qt
import matplotlib as mpl
from matplotlib.backends.backend_agg import FigureCanvasAgg as fca
from sympy import *
from sympy.parsing.sympy_parser import parse_expr
import numpy as np
import ColorMaps

# TODO Crée la table contenant les équations du noeud sélectionné
class EqTableCanvas(QTableWidget):
    def __init__(self, modApp, *args):
        self.modApp = modApp
        self.colors = ColorMaps.colorm()
        QTableWidget.__init__(self)


    def paintSection(self, painter, rect, logicalIndex):

        if not rect.isValid():
            return

        # ------------------------------ paint section (without the label) ----

        opt = QStyleOptionHeader()
        self.initStyleOption(opt)

        opt.rect = rect
        opt.section = logicalIndex
        opt.text = ""

        # ---- mouse over highlight ----

        mouse_pos = self.mapFromGlobal(QtGui.QCursor.pos())
        if rect.contains(mouse_pos):
            opt.state |= QtGui.QStyle.State_MouseOver

        # ---- paint ----

        painter.save()
        self.style().drawControl(QtGui.QStyle.CE_Header, opt, painter, self)
        painter.restore()

        # ------------------------------------------- paint mathText label ----

        qpixmap = self.qpixmaps[logicalIndex]

        # ---- centering ----

        xpix = (rect.width() - qpixmap.size().width()) / 2. + rect.x()
        ypix = (rect.height() - qpixmap.size().height()) / 2.

        # ---- paint ----

        rect = QtCore.QRect(xpix, ypix, qpixmap.size().width(),
                            qpixmap.size().height())
        painter.drawPixmap(rect, qpixmap)

    #def sizeHint(self):

        #baseSize = QHeaderView.sizeHint(self)

        #baseHeight = baseSize.height()
        #if len(self.qpixmaps):
        #    for pixmap in self.qpixmaps:
        #        baseHeight = max(pixmap.height() + 8, baseHeight)
        #baseSize.setHeight(baseHeight)

        #self.parentWidget().repaint()

        #return baseSize

    def tex_to_QPixmap(self,tex, fs):
        fig = mpl.figure.Figure()
        fig.patch.set_facecolor('none')
        fig.set_canvas(fca(fig))
        renderer = fig.canvas.get_renderer()

        ax = fig.add_axes([0,0,1,1])
        ax.axis('off')
        ax.patch.set_facecolor("none")
        t = ax.text(0,0,tex,ha='left', va = 'bottom', fontsize=fs)

        fwidth, fheight = fig.get_size_inches()
        fig_bbox = fig.get_window_extent(renderer)

        text_bbox = t.get_window_extent(renderer)

        tight_fwidth = text_bbox.width * fwidth / fig_bbox.width
        tight_fheight = text_bbox.height * fheight / fig_bbox.height

        fig.set_size_inches(tight_fwidth, tight_fheight)

        #---- convert mpl figure to QPixmap ----

        buf, size = fig.canvas.print_to_buffer()
        qimage = QImage.rgbSwapped(QImage(buf, size[0], size[1],QImage.Format_ARGB32))
        qpixmap = QPixmap(qimage)

        return qpixmap

    def generateLatex(self):
        def getlatex(n):
            expr = parse_expr((self.modApp.data[n][2]).replace('^','**'))
            tex = latex(expr)
            return self.tex_to_QPixmap("$" + tex + "$", 12)
        eqLat = list(map(lambda x : self.tex_to_QPixmap("$"+latex(parse_expr((self.modApp.data[x][2]).replace('^','**')))+"$",20),range(len(self.modApp.data))))
        return eqLat



    def updateView(self):
        self.clear()
        self.setRowCount(len(self.modApp.data))
        self.setColumnCount(3)
        self.wordWrap()
        self.setTextElideMode(Qt.ElideNone)
        self.setHorizontalHeaderLabels(['Complexity', 'Fitness', 'Equation'])

        #self.horizontalHeader().setMaximumWidth(1000)
        self.resizeColumnsToContents()
        #self.resizeRowsToContents()
        #self.resizeColumnsToContents()
        #eqList = self.generateLatex()
        for n  in range(len(self.modApp.data)):
            newitem = QTableWidgetItem(str(self.modApp.data[n][0]))
            cmap = self.colors.get("complexity",(self.modApp.data[n][0]/self.modApp.cmplxMax))
            newitem.setBackground(QColor(*cmap))
            if(sum(cmap)<128*3):
                newitem.setTextColor(Qt.white)
            self.setItem(n, 0, newitem)

            newitem = QTableWidgetItem(str(self.modApp.data[n][1]))

            cmap = self.colors.get("local",(self.modApp.data[n][1]/self.modApp.dataMaxFitness))
            newitem.setBackground(QColor(*cmap))
            self.setItem(n, 1, newitem)

            newitem = QTableWidgetItem(self.reformatNumberEquation(str(self.modApp.data[n][2])))
            #newitem = QTableWidgetItem(str(self.modApp.data[n][2]))
            if(self.modApp.clicked_line==n):
                newitem.setBackground(QColor(130, 130, 110))
            else:
                newitem.setBackground(QColor(255, 255, 255))
            #newitem.setSizeHint(QtCore.QSize(300,5))
            self.setItem(n, 2, newitem)

            #newitem = QTableWidgetItem(self.modApp.data[n][m])
            #self.setItem(n,m,newitem)
            #if m == 2:
            #    t = QTableWidgetItem()
            #    t.setData(Qt.DecorationRole, eqList[n])
            #    newitem = QTableWidgetItem(t)
            #    self.setItem(n, m, newitem)
            #else:
            #    self.setItem(n, m, QTableWidgetItem(self.modApp.data[n][m]))
        self.wordWrap()
        #self.setHorizontalHeaderLabels(['Complexity','Fitness','Equation'])
        #self.resizeColumnsToContents()
        self.resizeRowsToContents()
        self.horizontalHeader().setResizeMode(2,QtGui.QHeaderView.Stretch)
        #self.resizeColumnsToContents()
        self.resizeRowsToContents()

        if(self.modApp.globalModelView and not self.modApp.lastNodeClicked in self.modApp.varsIn and self.modApp.lastNodeClicked != ''):
            self.item(self.modApp.selectedEq[self.modApp.lastNodeClicked], 2).setBackground(QColor(100, 100, 150))


    def reformatNumberEquation(self,eq):
        eqlist=eq.split()
        eqRet=""
        for t in eqlist:
            try:
                eqRet=eqRet+"{:.2E}".format(float(t))
            except:
                if(t=="(" or t==")" or t=="log"):
                    eqRet = eqRet + t
                else:
                    eqRet=eqRet+" "+t+" "
        return eqRet

