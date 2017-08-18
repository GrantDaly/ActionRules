from __future__ import print_function

class AttributeValue:

    def __init__(attribute, value):
        self.attribute = attribute
        self.value = self.cleanData(value, self.attribute.attrValList)

    def __eq__(self, another):
        return hasattr(another, attribute) 
            and hasattr(another value) 
            and self.attribute.name == another.attribute.name
            and self.attribute.value == another.attribute.value

    def __hash__(self):
        return hash(self.attribute.name+self.value)

    def cleanData(value, valueList):

        if value in valueList: return value

        try:
            tempValue = int(value)
            tempValueList = map(int, valueList)
        except ValueError:
            tempValue = Decimal(value)
            tempValueList = map(Decimal, valueList)

        for val in tempValueList:
            #print(val,tempValue)
            if tempValue <= val:
                #print(str(val))
                return str(val)
        else: return str(val)
