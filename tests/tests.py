from action_rules import (
                         transactions,
                         readinData,
                         )

transactions = transactions.Transactions('test1.data')

print(transactions.numTransactions)
