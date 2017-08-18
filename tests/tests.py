from action_rules import (
                         transactions,
                         readinData,
                         aar
                         )

#transactObject = transactions.Transactions('test1.data')
transactObject = transactions.Transactions('../Data/hepatitis.data')

aar = aar.AAR(transactObject, 4, 0.75, '2')
atomicSets = tuple(j for i in aar.generateAtomicSets() for j in i)
print(atomicSets)
