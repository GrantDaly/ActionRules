from action_rules import (
                         transactions,
                         readinData,
                         aar
                         )

transactObject = transactions.Transactions('test1.data')

aar = aar.AAR(transactObject, 1, 1, {'LIFE':'2'})
aar.aarGenerator()
