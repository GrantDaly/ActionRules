from __future__ import print_function

class Attribute:
    
    def __init__(self, name, attrType, attrValList):
        self.name = name
        self.attrType = attrType
        self.attrValList = attrValList

    def isFlex(self):
        return self.attrType == 'flexible'

    def isStable(self):
        return self.attrType == 'stable'

    def isClass(self):
        return self.attrType == 'class'

    def displayAttr(self):
        print("Attribute Name: ",self.name, 
            "Attribute Type: ", self.attrType)
