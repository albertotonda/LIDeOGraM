import re

class DesignEquation:
    def __init__(self):
        self.eq = "4.06051503725042e-9+1.04280023474994e-7*UFAdivSFA+5.8569531230778e-8*UFAdivSFA^2-2.3477021990823e-9*UFA"
        self.eqNumbers = re.findall("([0-9]+\.[0-9]+[eE]?[+-]?[\d]*)", self.eq)

        for i in self.eqNumbers:
            newEq= self.eq.replace(i,"{0:.2e}".format(round(float(i), 2)))

        output = newEq
        print(output)


if __name__ == "__main__":
    c = DesignEquation()
