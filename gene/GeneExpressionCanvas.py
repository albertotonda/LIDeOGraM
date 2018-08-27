from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import numpy as np
from PyQt4 import QtGui
from matplotlib.pyplot import cm


class GeneExpressionCanvas(FigureCanvas):

    def __init__(self,modGene,vwGene):
        self.modGene = modGene
        self.vwGene = vwGene
        self.fig = plt.figure()
        self.axes = self.fig.add_subplot(111)
        self.axes.hold(True)
        self.fig.patch.set_visible(False)
        self.axes.axis('off')


        FigureCanvas.__init__(self, self.fig)
        FigureCanvas.setSizePolicy(self, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)


    def updateView(self):
        self.fig.clear()
        self.axes = self.fig.add_subplot(111)
        w = self.modGene.currGeneExpPlt
        if len(w)<75:
            xpos=np.arange(0.5, len(self.modGene.activCondShow) + 0.5, 1)
            if w!=[]:
                ax = self.axes
                # [j for j in range(len(self.modGene.f)) if self.modGene.loc[self.modGene.f[j]][1]=='galK']
                #ax.set_position([0.1, 0.1, 0.7, 0.8])
                color = iter(cm.rainbow(np.linspace(0, 1, len(w))))
                print('w:',w)

                if self.modGene.isZoomExp:
                    minExp = np.array([np.min(v) for v in np.transpose(self.modGene.Xf[np.ix_(w, self.modGene.activCondShow)])])
                    maxExp = np.array([np.max(v) for v in np.transpose(self.modGene.Xf[np.ix_(w, self.modGene.activCondShow)])])
                    subtractVect=(minExp+maxExp)/2
                    divVect=(maxExp-minExp)/2

                for j in w:
                    cn=next(color)
                    geneExps=self.modGene.Xf[j,self.modGene.activCondShow]

                    if self.modGene.isZoomExp:
                        geneExps=(geneExps-subtractVect)/divVect

                    if j != self.modGene.selectedGene:
                        ax.plot(xpos,geneExps, 'o-', c=cn,
                            label=self.modGene.loc[self.modGene.f[j]][1] + ' ' + self.modGene.loc[self.modGene.f[j]][0][5:])
                    else:
                        ax.plot(xpos, geneExps, 'o-', c=cn,
                                label=self.modGene.loc[self.modGene.f[j]][1] + ' ' +
                                      self.modGene.loc[self.modGene.f[j]][0][5:], linewidth=5)

                if self.modGene.isZoomExp:
                    ax.set_ylim((-1,1))
                else:
                    ax.set_ylim((np.minimum(-3, ax.get_ylim()[0]), np.maximum(3, ax.get_ylim()[1])))
                ax.set_xticks(xpos-0.4)

                tlab=[]
                if(0 in self.modGene.activCondShow):
                    tlab.extend(['22C 0h']*3)
                if(3 in self.modGene.activCondShow):
                    tlab.extend(['22C 6h']*3)
                if(6 in self.modGene.activCondShow):
                    tlab.extend(['30C 0h']*3)
                if(9 in self.modGene.activCondShow):
                    tlab.extend(['30C 6h']*3)
                ax.set_xticklabels(tlab,rotation=45 )

                # score = np.std(self.modGene.Xf[w])
                score = np.mean(np.std(self.modGene.Xf[w], 0))
                # score= np.mean(np.std(self.modGene.Xf[w],0))
                ax.set_title("prof: " + str(self.modGene.currprof) + ' nbGene: ' + str(len(w)) + ' score: ' + str(score))
                print('click ', self.modGene.lastNodeClicked, ' prof: ', self.modGene.currprof)
                #ax.legend(fontsize='small', bbox_to_anchor=(1.25, 1))
        else:
            self.axes.text(0.5,0.5,"Too much genes to plot",horizontalalignment='center')
        self.fig.canvas.draw()
