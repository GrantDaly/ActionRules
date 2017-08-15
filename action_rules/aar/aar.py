from __future__ import print_function

import itertools
from action_rules import classSet, stableSet, flexibleSet, actionRule

class AAR:
    def __init__(self, transactions, minSup, minConf, desired):
        self.transactions = transactions
        if isinstance(minSup, int):
            self.minSup = minSup
        elif isinstance(minSup, float):
            self.minSup = minSup * self.transaction.numTransactions
        self.desired = desired

    
    def aarGenerator(self):
      
        stableAttrs = list(self.transactions.generateAttrValue('stable'))
        flexibleAttrs = list(self.transactions.generateAttrValue('flexible'))
        #print(self.desired)
        classAttrs = self.transactions.undesiredAttributes(self.desired)

        while True:

            #print(*(i for i in itertools.product(stableAttrs, flexibleAttrs)))
            self.generateSingletRules(stableAttrs, flexibleAttrs, classAttrs)
            
            #print(flexibleAttrs)
            break

    def generateSingletRules(self, stableAttrs, flexibleAttrs, classAttrs):
        for stabAttr, stabValues in stableAttrs:
            for stabVal in stabValues:
                #print(stabAttr, stabVal)
                for flexAttr, flexValues in flexibleAttrs:
                    #print(*itertools.permutations(flexValues, 2))
                    for flexVal in itertools.permutations(flexValues, 2):
                        for classAttr, classValues in classAttrs:
                            for classVal in classValues:
                                #print(stabAttr, stabVal, flexAttr, flexVal, classAttr, (classVal, self.desired[classAttr]))
                                tempStabSet = [stableSet.StableSet(stabAttr, stabVal)]
                                tempFlexSet = [flexibleSet.FlexibleSet(flexAttr, *flexVal)]
                                tempClassSet = [classSet.ClassSet(classAttr, classVal, self.desired[classAttr])]
                                tempActionRule = actionRule.ActionRule(tempStabSet, tempFlexSet, tempClassSet, self.transactions)
                                tempActionRule.prettyPrint()
