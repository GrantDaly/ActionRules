from __future__ import print_function
from readinData import readinFile

import random

class Transactions():
    def __init__(self, fileName, nullValue='?'):
        self.stableDict, self.flexDict, self.classDict, self.attrList, self.numTransactions = readinFile(fileName, nullValue)

    def _getDictionary(self, flexOrStab):
        switchDict = {'flexible' : self.flexDict,
                      'stable' : self.stableDict,
                      'class' : self.classDict}
        return switchDict[flexOrStab]

    def randomAttribute(self, attrDict):
        return random.choice(attrDict.keys())
        
    def randomAttributeValue(self, flexOrStab= 'flexible'):
        attrDict = self._getDictionary(flexOrStab)
        attribute = self.randomAttribute(attrDict)
        value = random.choice(attrDict[attribute].keys())
        if flexOrStab == 'flexible':
            while True:
                tempVal = random.choice(attrDict[attribute].keys())
                if tempVal != value: break
            return attribute, (value, tempVal)
        else: return attribute, value

        
        


