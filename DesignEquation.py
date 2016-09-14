import re

# A intégrer au code de Marc.
class DesignEquation:
    def __init__(self,eq):
        print(eq)
        self.eq =eq
        self.eqNumbers = re.findall("((?:\d+)(?:\.\d*)?(?:[eE][+\-]?\d+)?)", self.eq)
        self.eqNumbers = list(filter(lambda x : x , self.eqNumbers))
        print(self.eqNumbers)

        for i in self.eqNumbers:
            self.eq= self.eq.replace(i,"{0:.2e}".format(round(float(i), 2)))

        self.output = self.eq

    def __str__(self):
        return self.output
    def __repr__(self):
        return self.output



if __name__ == "__main__":
    c = DesignEquation()
