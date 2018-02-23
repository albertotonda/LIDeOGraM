import matplotlib.pyplot as plt
import numpy as np
from matplotlib.pyplot import cm
import csv
class Gene_Controller:
    def __init__(self,modGene,vwGene):
        self.modGene=modGene
        self.vwGene=vwGene

    def onClickTest(self,event):

        bp=self.modGene.p0
        nodes=[]

        toexp=[bp]

        while(not toexp==[]):
            bp=toexp
            toexp=[]
            for p2 in bp:
                w = self.modGene.getallchildfrom([p2])
                score = np.mean(np.std(self.modGene.Xf[w], 0))
                if score >0.32 or (score > 0.25 and len(w) > 8):
                    newp = [sp for sp in self.modGene.tree[self.modGene.tree.parent == p2].child if sp in self.modGene.parents]
                    toexp.extend(newp)
                else:
                    nodes.append(p2)

        #leafs = [x for x in self.modGene.G.nodes() if self.modGene.G.out_degree(x) == 0]
        todata = []
        for l in nodes:

            w = self.modGene.getallchildfrom([l])

            score = np.mean(np.std(self.modGene.Xf[w], 0))
            #if score < 0.2:
            fig, ax = plt.subplots()
            # [j for j in range(len(self.modGene.f)) if self.modGene.loc[self.modGene.f[j]][1]=='galK']
            ax.set_position([0.1, 0.1, 0.7, 0.8])
            color = iter(cm.rainbow(np.linspace(0, 1, len(w))))
            for j in w:
                ax.plot(self.modGene.Xf[j], 'o-', c=next(color),
                        label=self.modGene.loc[self.modGene.f[j]][1] + ' ' + self.modGene.loc[self.modGene.f[j]][0][5:])
            ax.set_ylim((np.minimum(-3, ax.get_ylim()[0]), np.maximum(3, ax.get_ylim()[1])))
            # score = np.std(self.modGene.Xf[w])

            ax.set_title('nbGene:' + str(len(w)) + ' score:' + str(score))

            ax.legend(fontsize='small', bbox_to_anchor=(1.25, 1))
            fig.savefig('fig5/' + "class  " + str(l) + ' nbGene ' + str(len(w)) + '.png', dpi=400)

            #fig.show()



            for j in w:
                todataclass = [0] * 12
                for j in w:  # Parcours les indices dans f de la classe courante
                    todataclass += self.modGene.X2[self.modGene.f[j]]  # Les 12 points de données correspondant à un gène de cette classe
            todataline=[]
            todataline.append('Class '+str(l))
            todataline.append('Genes')
            todataline.append('0')
            todataline.extend(todataclass)
            todata.append(todataline)

        todata = np.transpose(todata)
        todata=todata[[0,1,2,3,5,6,8,9,10,13,14,4,7,11,12],:]
        #todata=todata[[0,1,2,3,4,5,6,7,8,9,10,11,12],:]
        with open("testdatagenes3.csv", 'w',newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(todata)




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

            #leu_iso_val : w=[952,953,954,955,958,957,956,887]
            # leu_iso_valV2 : w=[952,953,954,958,957,956]
            #pompe a proton w=[24,25,26,27,28,29,30,31,32]
            #Transport galactose w=[196,197,198,199,200,201,202,203]
            # Transport galactoseV2 w=[197,198,199,200,201,202]
            #Acetyl to Acetate w = [1500, 167, 168]
            #Transport Lactose Cellulose w=[644,645]
            #Transport Lactose Cellulose V2 w=[644,645,646,1145]
            #Parois w=[914,915,916,1147,1150,1161,1162,1163,1209,917,1148,1146]
            #ParoisV2 w=[914,915,916,1147,1150,917,1148,1146]
            #Paroisv2_TagGHL w = [1161, 1162, 1163, 1209]
            #acety_krebs w=[565,566,567]
            #glycolyse w=[840,1913,2101,159]
            #Metabolisme du glycerol w=[1910,1909,1908,1907,929]
            # Metabolisme du glycerol V2 w=[1910,1909,1908,1907]


            fig, ax = plt.subplots()
            #[j for j in range(len(self.modGene.f)) if self.modGene.loc[self.modGene.f[j]][1]=='galK']
            ax.set_position([0.1, 0.1, 0.7, 0.8])
            color = iter(cm.rainbow(np.linspace(0, 1, len(w))))
            for j in w:
                ax.plot(self.modGene.Xf[j], 'o-',c=next(color),label=self.modGene.loc[self.modGene.f[j]][1] + ' ' + self.modGene.loc[self.modGene.f[j]][0][5:] )
            ax.set_ylim((np.minimum(-3, ax.get_ylim()[0]), np.maximum(3, ax.get_ylim()[1])))
            #score = np.std(self.modGene.Xf[w])
            score = np.mean(np.std(self.modGene.Xf[w], 0))
            #score= np.mean(np.std(self.modGene.Xf[w],0))
            ax.set_title("prof : " + str(prof) + 'nbGene:' + str(len(w)) + ' score:' + str(score))
            print('click ', nodeclicked, ' prof: ', prof)
            ax.legend(fontsize='small', bbox_to_anchor=(1.25, 1))
            fig.show()

            # import csv
            # todata = []
            # wL=[[952,953,954,958,957,956],[1910,1909,1908,1907],[914,915,916,1147,1150,917,1148,1146],[24,25,26,27,28,29,30,31,32],[197,198,199,200,201,202]]
            # for w in wL:
            #     for j in w:
            #         todataclass = [0] * 12
            #         for j in w:  # Parcours les indices dans f de la classe courante
            #             todataclass += self.modGene.X2[self.modGene.f[j]]  # Les 12 points de données correspondant à un gène de cette classe
            #     todataline=[]
            #     todataline.append('Class')
            #     todataline.append('Genes')
            #     todataline.append('0')
            #     todataline.extend(todataclass)
            #     todata.append(todataline)
            #
            # todata = np.transpose(todata)
            # todata=todata[[0,1,2,3,5,6,8,9,10,13,14,4,7,11,12],:]
            # #todata=todata[[0,1,2,3,4,5,6,7,8,9,10,11,12],:]
            # with open("testdatagenes3.csv", 'w',newline='') as csvfile:
            #     writer = csv.writer(csvfile)
            #     writer.writerows(todata)
            #
            # np.savetxt("genesExp.csv", todata, delimiter=",")

    def clickSearchGene(self):
        print("clickSearchGene")
        txt=self.vwGene.searchTxt.text()
        numgene=[j for j in range(len(self.modGene.f)) if self.modGene.loc[self.modGene.f[j]][1] == txt or self.modGene.loc[self.modGene.f[j]][0] == txt  ]
        if numgene == []:
            self.modGene.highlightNode=-1
        else:
            numgene=numgene[0]
            numparent=self.modGene.tree[self.modGene.tree.child==numgene].parent.values[0]
            self.modGene.highlightNode=numparent
        self.vwGene.updateView()
