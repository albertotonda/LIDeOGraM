from PyQt4.QtCore import *

class OperatorsView(QtGui.QMainWindow,QtGui.QGraphicsItem):
    def __init__(self, modApp):
        QtGui.QMainWindow.__init__(self)
        QtGui.QGraphicsItem.__init__(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        # self.setWindowTitle(QtGui.QLabel("Test"))
        self.setWindowTitle("LIDeoGraM")
        self.icon = QtGui.QIcon("Icone.png")
        self.setWindowIcon(self.icon)

        self.setWindowState(QtCore.Qt.WindowMaximized)

        self.main_widget = QtGui.QWidget(self)

        self.gridLayout = QtGui.QGridLayout(self.main_widget)
        self.gridLayout.setSpacing(5)
        self.networkGUI = NetworkCanvas(self.modApp, self)
        # self.gridLayout.addWidget(self.networkGUI, 1, 0, 7, 60)
        self.gridLayout.addWidget(self.networkGUI, 1, 0, 2, 2)
        self.incMatGUI = IncMatrixCanvas(self.modApp, self)
        # self.gridLayout.addWidget(self.incMatGUI,1,61,12,60)
        # self.gridLayout.addWidget(self.incMatGUI, 1, 2, 3, 1)
        self.adjThreshold_slider = QtGui.QSlider(QtCore.Qt.Horizontal, self.main_widget)
        self.adjThreshold_slider.setValue(self.modApp.adjThresholdVal * 100)

        self.adjThreshold_lab = QtGui.QLabel('Edges importance : ')
        # self.gridLayout.addWidget(self.adjThreshold_lab, 8, 0, 1, 2)
        self.gridLayout.addWidget(self.adjThreshold_lab, 3, 0, 1, 1)
        # self.gridLayout.addWidget(self.adjThreshold_slider, 8, 2, 1, 57)
        self.gridLayout.addWidget(self.adjThreshold_slider, 3, 1, 1, 1)


        self.comprFitCmplx_lab_fit = QtGui.QLabel('Fitness')
        # self.gridLayout.addWidget(self.comprFitCmplx_lab_fit, 9, 59, 1, 1)
        self.selectContrTxtLab = QtGui.QLabel('')
        self.gridLayout.addWidget(self.selectContrTxtLab, 0, 1, 1, 1)
        selectContrFont = QtGui.QFont("AnyStyle", 14, QtGui.QFont.DemiBold)
        self.selectContrTxtLab.setFont(selectContrFont)

        self.clickedNodeLab = QtGui.QLabel('Selected node:')
        selNodeFont = QtGui.QFont("AnyStyle", 14, QtGui.QFont.DemiBold)
        self.clickedNodeLab.setFont(selNodeFont)
        self.eqTableGUI = EqTableCanvas(self.modApp)
        # self.gridLayout.addWidget(self.eqTableGUI, 1, 130, 6, 60)
        self.gridLayout.addWidget(self.eqTableGUI, 1, 3, 1, 1)

        self.gridLayout.addWidget(self.clickedNodeLab, 0, 3, 1, 1)

        self.uncertaintyModifTxt = QtGui.QLineEdit()
        self.uncertaintyModifButton = QtGui.QPushButton("Change Uncertainty")
        self.fitGUI = FitCanvas(self.modApp)
        # self.gridLayout.addWidget(self.fitGUI, 7, 130, 6, 60)

        self.fit_widget = QtGui.QWidget(self)
        self.fitLayout = QtGui.QGridLayout(self.fit_widget)
        self.fitLayout.addWidget(self.uncertaintyModifTxt, 0, 0, 1, 1)
        self.fitLayout.addWidget(self.uncertaintyModifButton, 0, 1, 1, 1)
        self.fitLayout.addWidget(self.fitGUI, 1, 0, 1, 2)
        self.gridLayout.addWidget(self.fit_widget, 2, 3, 2, 1)

        self.buttonChangerEq = QtGui.QPushButton('Change equation', self)

        self.gridLayout.addWidget(self.buttonChangerEq, 4, 0, 1, 1)



        self.setCentralWidget(self.main_widget)

        self.updateView()