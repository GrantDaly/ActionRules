from __future__ import print_function

from action_rules import transactions


transactions = transactions.Transactions('tests/test1.data')


print(*transactions.randomAttributeValue('class'))
