from __future__ import print_function
from __future__ import division

import pdb

class ActionRule():
    def __init__(self, stableAttrs, flexibleAttrs, classAttrs, transactions):
        self.stableAttrs = stableAttrs
        self.flexibleAttrs = flexibleAttrs
        self.classAttrs = classAttrs
        self.transactions = transactions
        
    def suppConf(self):
        stableSet = set.intersection(*[self.transactions.getTransactions(i.attribute, i.value, 'stable') for i in self.stableAttrs])
        #pdb.set_trace()
        flexCondSet = set.intersection(*[self.transactions.getTransactions(i.attribute, i.conditionValue, 'flexible') for i in self.flexibleAttrs])
        flexPredSet = set.intersection(*[self.transactions.getTransactions(i.attribute, i.predictionValue, 'flexible') for i in self.flexibleAttrs])

        

        classUndesSet = set.intersection(*[self.transactions.getTransactions(i.classAttribute, i.undesiredValue, 'class') for i in self.classAttrs])
        classDesSet = set.intersection(*[self.transactions.getTransactions(i.classAttribute, i.desiredValue, 'class') for i in self.classAttrs])

        condCard = len(set.intersection(stableSet, flexCondSet, classUndesSet))
        predCard = len(set.intersection(stableSet, flexPredSet, classDesSet))
        support = min(condCard, predCard)
 
        confCardPt1Num = condCard
        confCardPt1Denom = len(set.intersection(stableSet, flexCondSet))

        confCardPt2Num = predCard
        confCardPt2Denom = len(set.intersection(stableSet, flexPredSet))

        try:
            confidence = (confCardPt1Num / confCardPt1Denom) * (confCardPt2Num / confCardPt2Denom)
        except ZeroDivisionError:
            confidence = float('inf')

        return support, confidence
        #for stabAttr in self.stableAttrs:


    def prettyPrint(self):

        stableList, flexList, classList = [],[],[]
        for candidate in self.transactions.attrList:
            
            if candidate.isStable():

                for stab in self.stableAttrs:
                    if stab.attribute == candidate.name:
                        print("[",stab.attribute,",", stab.value,"]", sep="", end="")
        for candidate in self.transactions.attrList:
            if candidate.isFlex():
                for flex in self.flexibleAttrs:
                    if flex.attribute == candidate.name:
                        print("[",flex.attribute,",", flex.conditionValue,"->",flex.predictionValue,"]", sep="", end="")
        print(" -> ",end="")
        for candidate in self.transactions.attrList:
            if candidate.isClass():
                for classAttr in self.classAttrs:
                    if classAttr.classAttribute == candidate.name:
                        print("[",classAttr.classAttribute,",", classAttr.undesiredValue,"->",classAttr.desiredValue,"]", sep="", end="")
        print(end=" ")
        print(*self.suppConf(), end="")
        print()
        #print(*stableList)
        #print(*flexList)

