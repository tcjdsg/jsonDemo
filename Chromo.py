class Chromosome(object):
    def __init__(self):
        self.codes = []
        self.WorkTime = 99999999
        self.variance = 0
        self.movetime = 0
        self.t=0


    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def setcodes(self,codes):
            self.codes=codes

    def setf(self):

        self.f=[self.WorkTime,self.variance,self.movetime]
        return self.f