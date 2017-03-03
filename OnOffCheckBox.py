from PyQt4 import QtGui, QtCore
import sys
#===============================================================================
# MyCheckBox
#===============================================================================
#className
class OnOffCheckBox(QtGui.QCheckBox):
#|-----------------------------------------------------------------------------|
# class Variables
#|-----------------------------------------------------------------------------|
    #no classVariables

#|-----------------------------------------------------------------------------|
# Constructor
#|-----------------------------------------------------------------------------|
    def __init__(self, cntrApp, id,   *args, **kwargs):
            QtGui.QCheckBox.__init__(self, *args, **kwargs)
            self.setStyleSheet("background-color: rgb(0, 0, 0);\n" +
                      "color: rgb(255, 255, 255);\n")
            #set default check as True
            self.setChecked(True)
            #set default enable as True
            #    if it set to false will always remain on/off
            #    here it is on as setChecked is True
            self.setEnabled(True)
            self._enable = True
            self.id=id
            self.cntrApp=cntrApp
#|--------------------------End of Constructor---------------------------------|
#|-----------------------------------------------------------------------------|
#   mousePressEvent
#|-----------------------------------------------------------------------------|
    #overrite
    def mousePressEvent(self, *args, **kwargs):
            #tick on and off set here
            if self.isChecked():
                self.setChecked(False)
            else:
                self.setChecked(True)
            self.cntrApp.onOffClicked(self)
            return QtGui.QCheckBox.mousePressEvent(self, *args, **kwargs)
#|--------------------------End of mousePressEvent-----------------------------|

#|-----------------------------------------------------------------------------|
# paintEvent
#|-----------------------------------------------------------------------------|
    def paintEvent(self,event):

            #just setting some size aspects
            self.setMinimumHeight(1)
            self.setMinimumWidth(1)
            self.setMaximumHeight(20)
            self.setMaximumWidth(40)

            self.resize(self.parent().width(),self.parent().height())
            painter = QtGui.QPainter()
            painter.begin(self)

            #for the black background
            #brush = QtGui.QBrush(QtGui.QColor(0,0,0),style=QtCore.Qt.SolidPattern)
            #painter.fillRect(self.rect(),brush)


            #smooth curves
            painter.setRenderHint(QtGui.QPainter.Antialiasing)

            #for the on off font
            font  = QtGui.QFont()
            font.setFamily("Courier New")
            font.setPixelSize(10)
            painter.setFont(font)

            #change the look for on/off
            if self.isChecked():
                #blue fill
                brush = QtGui.QBrush(QtGui.QColor(120,120,120),style=QtCore.Qt.SolidPattern)
                painter.setBrush(brush)

                #rounded rectangle as a whole
                painter.drawRoundedRect(0,0,self.width()-2,self.height()-2, \
                                   self.height()/2,self.height()/2)

                #white circle/button instead of the tick mark
                brush = QtGui.QBrush(QtGui.QColor(200,200,200),style=QtCore.Qt.SolidPattern)
                painter.setBrush(brush)
                painter.drawEllipse(self.width()-self.height(),0,self.height(),self.height())

                #on text
                brush = QtGui.QBrush(QtGui.QColor(0, 0, 0), style=QtCore.Qt.SolidPattern)
                painter.setBrush(brush)
                painter.drawText(self.width()/6,self.height()/1.5, "On")

            else:
                #gray fill
                brush = QtGui.QBrush(QtGui.QColor(50,50,50),style=QtCore.Qt.SolidPattern)
                painter.setBrush(brush)

                #rounded rectangle as a whole
                painter.drawRoundedRect(0,0,self.width()-2,self.height()-2, \
                                   self.height()/2,self.height()/2)

                #white circle/button instead of the tick but in different location
                brush = QtGui.QBrush(QtGui.QColor(200,200,200),style=QtCore.Qt.SolidPattern)
                painter.setBrush(brush)
                painter.drawEllipse(0,0,self.height(),self.height())

                #off text
                brush = QtGui.QBrush(QtGui.QColor(0, 0, 0), style=QtCore.Qt.SolidPattern)
                painter.setBrush(brush)
                painter.drawText(self.width()/2,self.height()/1.5, "Off")


#|-----------------------End of paintEvent-------------------------------------|
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    wgt = QtGui.QWidget()
    wgt.setStyleSheet("background-color: rgb(0, 0, 0);\n")
    cb = OnOffCheckBox(-1)
    cb.setParent(wgt)
    layout = QtGui.QHBoxLayout()
    layout.addWidget(cb)
    wgt.resize(30,15)
    wgt.show()
    sys.exit(app.exec_())