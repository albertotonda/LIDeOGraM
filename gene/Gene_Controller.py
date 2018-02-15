import matplotlib.pyplot as plt
import numpy as np
class Gene_Controller:
    def __init__(self,modGene,vwGene):
        self.modGene=modGene
        self.vwGene=vwGene

    def onClick(self,event):

        (x, y) = (event.xdata, event.ydata)
        if x == None or y == None:
            return

        dst = [(pow(x - self.modGene.pos[node][0], 2) + pow(y - self.modGene.pos[node][1], 2), node) for node in
               self.modGene.pos]# compute the distance to each node

        if (len(list(filter(lambda x: x[0] < self.modGene.radius,
                            dst))) == 0 and event.button == 1):  # If no node is close enougth, select no node update view and exit

            self.modGene.lastNodeClicked = None
            print('click None')

        else:
            nodeclicked = min(dst, key=(lambda x: x[0]))[1]  # Closest node
            self.modGene.lastNodeClicked = nodeclicked

            prof = self.modGene.profondeur(nodeclicked)
            w = self.modGene.getallchildfrom([nodeclicked])
            fig, ax = plt.subplots()
            ax.set_position([0.1, 0.1, 0.7, 0.8])
            for j in w:
             ax.plot(self.modGene.Xf[j], 'o-',c=np.random.rand(3,1),label=self.modGene.loc[self.modGene.f[j]][1] + ' ' + self.modGene.loc[self.modGene.f[j]][0][5:] )
            ax.set_ylim((np.minimum(-3, ax.get_ylim()[0]), np.maximum(3, ax.get_ylim()[1])))
            score = np.std(self.modGene.Xf[w])
            ax.set_title("prof : " + str(prof) + 'nbGene:' + str(len(w)) + ' score:' + str(score))
            print('click ', nodeclicked, ' prof: ', prof)
            ax.legend(fontsize='xx-small', bbox_to_anchor=(1.25, 1))
            fig.show()