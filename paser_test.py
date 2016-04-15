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
        print(tree.childs[0].name)
    elif tree.name == 'Mul':
        display(tree.childs[0])
        display(tree.childs[1])
    elif tree.name == "Pow":
        print("(")
        display(tree.childs[0])
        print("^{")
        display(tree.childs[1])
        print('}')
        print(")")
    elif tree.name == "Integer":
        print(tree.childs[0].name)
    elif tree.name == "base":
        display(tree.childs[0])
    elif tree.name == "Add":
        print("(")
        display(tree.childs[0])
        print("+")
        display(tree.childs[1])
        print(")")
    elif tree.name == "Float":
        #print("{03}".format(float(tree.childs[0].name.replace("'",""))))
        print(tree.childs[0].name)




display(f1(srepr(expr)))