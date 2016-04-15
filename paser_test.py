from sympy import srepr
from sympy.parsing.sympy_parser import parse_expr
eq = "0.890420685427687+(12.075341069316*UFAdivSFA+73.2315556415024*UFAdivSFA**3-0.943665542824327-51.5061941345233*UFAdivSFA**2)/(CFAdivUFA-3.83166666666667)"
expr = parse_expr(eq)
print(srepr(expr))
tree = srepr(expr)


class ctree:
    def __init__(self, n):
        self.name = n
        self.childs = []

def f1(line):

    tr = ctree("base")

    def f2(l2, tr):
        i = 0
        s= ""
        while( i < len(l2)):
            if l2[i] == "(":
                if s is not "":
                    tr.append(ctree((s)))
                s=""
                i+=f2(l2[i+1:],tr[-1].childs)
            elif l2[i] == ")":
                if s is not "":
                    tr.append(ctree(s))
                return i+1
            elif l2[i] == ",":
                if s is not "":
                    tr.append(ctree(s))
                s=""
            else:
                if l2[i] != " ":
                    s+= l2[i]
            i+=1
    f2(line,tr.childs)
    return tr

def display(tree):
    s = ""
    if tree.name == "Symbol":
        s+=(tree.childs[0].name)
    elif tree.name == 'Mul':
        for i in tree.childs:
            s +=display(i)
        #s +=display(tree.childs[1])
    elif tree.name == "Pow":
        s += ("(")
        s +=display(tree.childs[0])
        s +=("^{")
        s +=display(tree.childs[1])
        s +=('}')
        s +=(")")
    elif tree.name == "Integer":
        s +=(tree.childs[0].name)
    elif tree.name == "base":
        s +=display(tree.childs[0])
    elif tree.name == "Add":
        s +=("(")
        for i in tree.childs[:-1]:
            s += display(i)
            s +=("+")
        s+= display(tree.childs[-1])
        s +=(")")
    elif tree.name == "Float":
        #print("{03}".format(float(tree.childs[0].name.replace("'",""))))
        t = tree.childs[0].name
        u = t[1:-1]
        v = float(u)
        s+="{0:.2f}".format(v)
        #s +=(tree.childs[0].name)
    return s




t = display(f1(srepr(expr)))
k = t.replace("'","")

import numpy as np
import matplotlib.pyplot as plt
t = np.arange(0.0, 2.0, 0.01)
s = np.sin(2*np.pi*t)

plt.plot(t,s)
plt.title(r'$\alpha_i > \beta_i$', fontsize=20)
plt.text(1, -0.6, r'$\sum_{i=0}^\infty x_i$', fontsize=20)
plt.text(0.6, 0.6, "$"+k+"$",fontsize=20)
plt.xlabel('time (s)')
plt.ylabel('volts (mV)')
plt.show()
