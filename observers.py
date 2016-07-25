class Observer:
    def update(self, values: dict):
        pass

class Subject:
    def __init__(self):
        self.obs = []

    def registerObs(self,o : Observer):
        self.obs.append(o)

    def removeObs(self,o : Observer):
        self.obs.remove(o)

    def notifyObs(self, values : dict):
        for o in self.obs:
            o.update(values)