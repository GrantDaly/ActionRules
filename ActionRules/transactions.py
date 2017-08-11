from __future__ import print_function
from readinData import readinFile

class Transactions():
    def __init__(self, fileName, nullValue='?'):
        self.stableDict, self.flexDict, self.classDict, self.attrList, self.numTransactions = readinFile(fileName, nullValue)


