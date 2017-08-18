from __future__ import print_function

import pdb

import itertools
from action_rules import classSet, stableSet, flexibleSet, actionRule, atomicSet

class AAR:
    def __init__(self, transactions, minSup, minConf, desired):
        self.transactions = transactions
        if isinstance(minSup, int):
            self.minSup = minSup
        elif isinstance(minSup, float):
            self.minSup = minSup * self.transaction.numTransactions
        self.minConf = float(minConf)
        self.desired = desired

    
    def aarGenerator(self):
      
        stableAttrs = list(self.transactions.generateAttrValue('stable'))
        flexibleAttrs = list(self.transactions.generateAttrValue('flexible'))
        #print(self.desired)
        classAttrs = self.transactions.undesiredAttributes(self.desired)

        initialActionSet = self.generateSingletRules(stableAttrs, flexibleAttrs, classAttrs)
        [i.prettyPrint() for i in initialActionSet]
        #while True:

           
            #self.generateSingletRules(stableAttrs, flexibleAttrs, classAttrs)
            
            #print(flexibleAttrs)
            #break



    def generateAtomicSets(self):
        switchDict = {'class' : self.classAtomicSet, 'stable': self.stableAtomicSet, 'flexible' : self.flexibleAtomicSet}
        for attr in self.transactions.generateAttribute():
            valList = [val for val in self.transactions.generateValue(attr)]
            attrType = self.transactions.getType(attr)
            tempAtomicSetGen = switchDict[attrType]
            atomicSetVals = [(attr, val) for val in tempAtomicSetGen(*valList)]
            print("Got Here")
            print(atomicSetVals)
                


    def classAtomicSet(self, *values):
        desired = self.desired
        undesiredList = filter(lambda x: x != desired, values)

        for undes in undesiredList:
            yield undes, desired

    def stableAtomicSet(self, *values):
        for stab in values:
            yield stab, stab

    def flexibleAtomicSet(self, *values):
        for cond, pred in itertools.permutations(values, 2):
            yield cond, pred
