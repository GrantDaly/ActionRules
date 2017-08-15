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

    def generateAttribute(self, flexOrStab):
        attrDict = self._getDictionary(flexOrStab)
        for attr in attrDict.keys():
            yield attr

    def generateValue(self, attribute, flexOrStab):
        attrDict = self._getDictionary(flexOrStab)
        for value in attrDict[attribute]:
            yield value

    def generateAttrValue(self, flexOrStab):
        for attr in self.generateAttribute(flexOrStab):
            values = tuple(self.generateValue(attr, flexOrStab))
            yield attr, values

    def undesiredAttributes(self, desired):
        classAttrs = []
        for attr, vals in self.generateAttrValue('class'):
            classAttrs.append((attr, tuple(val for val in vals if val != desired[attr])))
        return classAttrs

    def getTransactions(self, attribute, value, flexOrStab):
        attrDict = self._getDictionary(flexOrStab)
        return attrDict[attribute][value]


