from __future__ import print_function

from attribute import Attribute

from decimal import Decimal
from collections import defaultdict
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

                tempAttr = Attribute(attrName, attrType, attrValList)
                attrList.append(tempAttr)
        #[attr.displayAttr() for attr in attrList]

        stableDict = defaultdict(dict)
        flexDict = defaultdict(dict)
        classDict = defaultdict(dict)

        attrSwitch = {'class' : classDict,
                      'flexible' : flexDict,
                      'stable' : stableDict}

        for attribute in attrList:
            attrDict = attrSwitch[attribute.attrType][attribute.name]
            for val in attribute.attrValList:
                attrDict[val] = set()
        #print(flexDict)

        for i, line in enumerate(inFile):
            line = line.strip('\n').split(',')
            
            for attribute , value in zip(attrList , line):
                #print("Attribute: ", attribute.name,
                     #"Value: ", value)
                if value == nullValue: continue

                else:
                    #print("Invalid Entry")
                    tempVal = cleanData(value, attribute.attrValList)
                    #print("Temp Val: ", tempVal, "***", attribute.attrValList)
                    try:
                        attrSwitch[attribute.attrType][attribute.name][tempVal].add(i)
                    except KeyError:
                        attrSwitch[attribute.attrType][attribute.name][tempVal] = set()
    #print("Stab Dict: ",stableDict)
    #print("******************************************")
    #print("Flex Hist: ", flexDict['HISTOLOGY'])
    numTransactions = i + 1
    return stableDict, flexDict, classDict, attrList, numTransactions

def cleanData(value, valueList):

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

     
