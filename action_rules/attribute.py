from __future__ import print_function

from collections import OrderedDict

class Attribute:
    
    def __init__(self, name, attrType, valList):
        self.name = name
        self.attrType = attrType
        self.valDict = OrderedDict.fromkeys(valList, set())


    def isFlex(self):
        return self.attrType == 'flexible'

    def isStable(self):
        return self.attrType == 'stable'

    def isClass(self):
        return self.attrType == 'class'

    def displayAttr(self):
        print("Attribute Name: ",self.name, 
            "Attribute Type: ", self.attrType)

    def getTransactions(self, attribute

