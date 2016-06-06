import re

class DesignEquation:
    def __init__(self):
        self.eq = "0.890420685427687+(12.075341069316*UFAdivSFA+73.2315556415024*UFAdivSFA**3-0.943665542824327-51.5061941345233*UFAdivSFA**2)/(CFAdivUFA-3.83166666666667)"
        self.eqNumber = re.findall("([0-9]\.[0-9]*)", self.eq)

        for i in self.eqNumber:
            newEq= self.eq.replace(i,"{0:.2e}".format(round(float(i), 2)))

        output = newEq
        print(output)