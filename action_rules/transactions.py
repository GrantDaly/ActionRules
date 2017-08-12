from __future__ import print_function
from readinData import readinFile

import random

class Transactions():
    def __init__(self, fileName, nullValue='?'):
        self.stableDict, self.flexDict, self.classDict, self.attrList, self.numTransactions = readinFile(fileName, nullValue)

    def randomAttribute(self, flexOrStab = 'flexible'):
        switchDict = {'flexible' : self.flexDict,
                      'stable' : self.stableDict}
        return random.choice(self.switchDict[flexOrStab].keys())
        


