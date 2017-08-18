from __future__ import print_function

import pdb
#from attribute import Attribute
#from attributeValue import AttributeValue

from decimal import Decimal
from collections import defaultdict, OrderedDict
import csv
import re

def readinFile(fileName, nullValue='?'):

    with open(fileName, 'r') as inFile:
        attrList = []

        for line in inFile:
            if not (line.startswith("%")):
                line = line.strip('\n')
                if line.startswith("@data"):
                    break

                line = line.strip('@').split(' ')
                attrType = line.pop(0)

                line = line[0].split(':')
                attrName = line.pop(0)
                
                attrValList = line[0].split(',')
                #attrValList = [AttributeValue(i) for i in attrValList]

                #tempAttr = Attribute(attrName, attrType, attrValList)
                tempAttr = tuple((attrName, attrType, attrValList))
                attrList.append(tempAttr)

        transactionDict = OrderedDict()
        for attrName, attrTyp, attrValList in attrList:

            transactionDict[attrName] = dict()
            transactionDict[attrName]['type'] = attrTyp
            transactionDict[attrName]['values'] = OrderedDict.fromkeys(attrValList, set())



        for i, line in enumerate(inFile):
            line = line.strip('\n').split(',')
            
            for attribute , value in zip(transactionDict.keys() , line):
                #pdb.set_trace()
                #print("Attribute: ", attribute.name,
                     #"Value: ", value)
                if value == nullValue: continue
                
                
                else:
                    #print("Invalid Entry")
                    tempVal = cleanData(value, transactionDict[attribute]['values'].keys())
                    transactionDict[attribute]['values'][tempVal].add(i)
                    
    numTransactions = i + 1
    return transactionDict, numTransactions

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

     
