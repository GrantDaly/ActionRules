from __future__ import print_function


class ActionRule():
    def __init__(self, stableAttrs, flexibleAttrs, classAttrs, transactions):
        self.stableAttrs = stableAttrs
        self.flexibleAttrs = flexibleAttrs
        self.classAttrs = classAttrs
        self.transactions = transactions
        
    def support(self, transactions):
        #stableSet = transactions.getTransactions(stable
        pass

    def prettyPrint(self):
        #print("got here")
        #print(type(self.stableAttrs))
        #stableList = (sorted(*[(i.attribute, i.value) for i in self.stableAttrs], key = lambda x : x[0], reverse=True))

        #flexList = (sorted(*[(i.attribute, i.conditionValue, i.predictionValue) for i in self.flexibleAttrs], key = lambda x : x[0], reverse = True))
        #print(*(i.attribute for i in self.flexibleAttrs))

        stableList, flexList, classList = [],[],[]
        for candidate in self.transactions.attrList:
            #print(candidate.name)
            
            if candidate.isStable():
                #print("got here")
                for stab in self.stableAttrs:
                    if stab.attribute == candidate.name:
                        print("[",stab.attribute,",", stab.value,"]", sep="", end="")
        for candidate in self.transactions.attrList:
            if candidate.isFlex():
                for flex in self.flexibleAttrs:
                    if flex.attribute == candidate.name:
                        print("[",flex.attribute,",", flex.conditionValue,"->",flex.predictionValue,"]", sep="", end="")
        for candidate in self.transactions.attrList:
            if candidate.isClass():
                for classAttr in self.classAttrs:
                    if classAttr.classAttribute == candidate.name:
                        print("[",classAttr.classAttribute,",", classAttr.undesiredValue,"->",classAttr.desiredValue,"]", sep="", end="")
        print()
        #print(*stableList)
        #print(*flexList)

