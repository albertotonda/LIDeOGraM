from sympy import srepr
from sympy.parsing.sympy_parser import parse_expr
eq = "a/b"
eqd = {"a":None,"b":None}
expr = parse_expr(eq)
print(srepr(expr))
tree = srepr(expr)

def execute(line: str):
    s = ''
    for n,i in enumerate(((line))):
        if i == '(':
            s+=('\n')

            s+= execute(line[n+1:])
        elif line[n] == ")":
            return s+'\n'
        else:
            s+=(line[n])
    return (s)

#print(execute(tree))

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
                tr.append(ctree((s)))
                s=""
                i+=f2(l2[i+1:],tr[-1].childs)
            elif l2[i] == ")":
                tr.append(ctree(s))
                return i+1
            elif l2[i] == ",":
                tr.append(ctree(s))
                s=""
            else:
                if l2[i] != " ":
                    s+= l2[i]
            i+=1
    f2(line,tr.childs)
    return tr

def display(tree):
    tree.childs = list(filter(lambda x : len(x.childs)> 0 , tree.childs))
    s = ""
    if tree.name == "Symbol":
        print(tree.childs[0].name)
    elif tree.name == 'Mul':
        display(tree.childs[0])
        display(tree.childs[1])
    elif tree.name == "Pow":
        display(tree.childs[0])
        print("^{")
        display(tree.childs[1])
        print('}')
    elif tree.name == "Integer":
        print(tree.childs[0].name)
    elif tree.name == "base":
        display(tree.childs[0])



display(f1(srepr(expr)))