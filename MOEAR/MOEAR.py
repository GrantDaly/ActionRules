from __future__ import division
from __future__ import print_function

import random
import numpy
import matplotlib.pyplot as plt
import sys
import re
import itertools
import timeit
import argparse

from deap import base
from deap import creator
from deap import tools

parser = argparse.ArgumentParser(description = 'Multi-Objective Evolutionary Algorithm for Action Rule Mining')
parser.add_argument('inFile', metavar='i', help="input file")
parser.add_argument('-o', '--outFilePrefix', help="output file", required=False, default=None)
parser.add_argument('-t', '--printTime', help="Prints Generation Time to Screen", action='store_true')
parser.add_argument('-p', '--popSize', help="Population Size (Default 150)", type=int, default=150)
parser.add_argument('-g', '--numGens',  help="Number of Generations (Default 1000)", type=int, default=1000)
parser.add_argument('-e', '--evalFunction', help="Which Evaluation Function to Use. Choose from {aar, gtr}", choices=('aar', 'gtr'), default='aar')
parser.add_argument('-l', '--printLog', help="Print Out the Logbook", action='store_true', required=False)
parser.add_argument('--displayPlot', help="Print graph of Median over generations", action='store_true', required=False)
parser.add_argument('--minConf', type=float, action='store', default=0.0)
parser.add_argument('--minSup', type=int, action='store', default=0)
args = parser.parse_args()
dataFile = args.inFile
outputFileName = args.outFilePrefix
timer = args.printTime
popSize = args.popSize
NGEN = args.numGens
evalFunction = args.evalFunction
geneticProcedureStats = args.printLog
displayPlotBool = args.displayPlot
minConf = args.minConf
minSup = args.minSup
#print(minConf)
debugMode = False
debugGeneticProcedure = False
#timer = True
paretoStats = True
printPop = False
#geneticProcedureStats = True
aarPrintPop = True
transactionIDmode = False
outPutFileMode = True

dataFormatOld = True

#numTransactions = 4000

#dataFile = sys.argv[1]
#outputFile = sys.argv[2]


def readinFile(dataFile):
   readinStart = timeit.default_timer()
   attributeRE = re.compile('^@attribute.*.$', re.MULTILINE)
   decisionRE = re.compile('^@decision.*.$', re.MULTILINE)
   dataRE = re.compile('^((?!@).*.$)', re.MULTILINE)

   nullValue = 'null'

   with open(dataFile, 'r') as data:
      dataList = data.read()
   
      #put attributes into dictionary
      attributes = attributeRE.findall(dataList)
      attributes = [i.split() for i in attributes]
      [i.pop(0) for i in attributes]
      keys = [i.pop(0) for i in attributes]

      for attribute in attributes:
         attribute[0] = attribute[0].strip('{}').split(',')
         #this if for flex or stab. It reads it in as a string
         attribute[1] = int(attribute[1])
      
      #for index, unclnAttr in enumerate(attributes):
      #   tempAttrs = []
      #   tempNames = unclnAttr[0:-1][:]
      #   tempAttrs = tempNames[0].strip('{}').split(',')
         #attributes[index] = unclnAttr.strip('{}').split(',')


      attributeList = []
      transactionDict = {}
      nullSet = set()

      for keyCount in xrange(len(keys)):
         tempList = []
         for values in attributes[keyCount][0]:
            tempList.append((keys[keyCount]+'_'+values))
            transactionDict[(keys[keyCount]+'_'+values)] = set()
         
         #put in Null
         nullName = keys[keyCount]+'_'+nullValue
         tempList.append(nullName)
         transactionDict[nullName] = set()
         nullSet.add(nullName)

         tempList = [tuple(tempList)]
         
         tempList.insert(0, keys[keyCount])
         tempList.append(attributes[keyCount][-1])
         attributeList.append(tempList)
         
      #put decision attributes into decision dictionary
      desiredAttr = []
      undesiredAttr = []
      decisions = decisionRE.findall(dataList)
      decisions = [i.split() for i in decisions]
      [i.pop(0) for i in decisions]

      decisionKeys = [i.pop(0) for i in decisions]
      #[keys.append(i.pop(0)) for i in decisions]
      for decision in decisions:
         decision[0] = decision[0].strip('{}').split(',')
         #decision[1] = int(decision[1])
      #decisionDict = dict(zip(keys, decisions))

      decisionList = []
   
      for decision in decisionKeys:
         for values in decisions:
            tempList = []
            for value in values[0]:
               tempList.append(decision+'_'+value)
               if value == values[-1]:
                  desiredAttr.append(decision+'_'+value)
                  transactionDict[decision+'_'+value] = set()
               elif value != values[-1]:
                  undesiredAttr.append(decision+'_'+value)
                  transactionDict[decision+'_'+value] = set()  

            tempList = [tuple(tempList)]
            #tempList = [tuple(tempList)]
            tempList.append(values[-1])
            tempList.insert(0, decision)
         decisionList.append(tempList)

      #make cost dict, currently deprecated
      #costDict = dict()
      #for attribute in attributeList:
      #   cost = attribute[-1]
      #   for value in attribute[1]:
      #      costDict[value] = cost

      #add data to transaction dict
      allKeys = keys[:]
      dataScrubbed = dataRE.findall(dataList)
      [allKeys.append(i) for i in decisionKeys]
      transactionCounter = 1
      numTransactions = len(dataScrubbed)
      for line in dataScrubbed:
         line = line.split(',')
         if transactionIDmode:
            transactionID = line.pop(0)
         else:
            transactionID = 't'+str(transactionCounter)
            transactionCounter += 1
         candidateIDs = zip(allKeys, line)
         for candidate in candidateIDs:
            tempID = '_'.join(list(candidate))
            if tempID in transactionDict:
               transactionDict[tempID].add(transactionID)
            else:
               #print("Invalid Item: ", tempID)
               pass
   readinEnd = timeit.default_timer()
   if timer:
      #print("File Read In Time (sec): ", round(readinEnd-readinStart, 2)) 
      pass
   return decisionList, attributeList, transactionDict, undesiredAttr, desiredAttr, nullSet, numTransactions

def readNewFormat(dataFile):
   flexibleRE = re.compile('^@flexible.*.$', re.MULTILINE)
   stableRE = re.compile('^@stable.*.$', re.MULTILINE)
   decisionRE = re.compile('^@class.*.$', re.MULTILINE)
   dataRE = re.compile('^((?!@).*.$)', re.MULTILINE)

   nullValue = 'null'

   with open(dataFile, 'r') as data:
      dataList = data.read()
   
      #put stable attributes into dictionary
      stabAttributes = stableRE.findall(dataList)
      stabAttributes = [(i.split()) for i in stabAttributes]
      [i.pop(0) for i in stabAttributes]
      stabAttributes = [(i[0].split(':')) for i in stabAttributes]
      stabKeys = [i.pop(0) for i in stabAttributes]
      #stabAttributes = [i[0].split(',') for i in stabAttributes]

      for stab in stabAttributes:
         stab.append(0)
         stab[0] = tuple(stab[0].split(','))
         #make it clear that this is a stable attribute
         #stab[1] = int(1)

      #put flexible attributes into dictionary
      flexAttributes = flexibleRE.findall(dataList)
      flexAttributes = [(i.split()) for i in flexAttributes]
      [i.pop(0) for i in flexAttributes]
      flexAttributes = [(i[0].split(':')) for i in flexAttributes]
      flexKeys = [i.pop(0) for i in flexAttributes]


      for flex in flexAttributes:
         flex.append(1)
         flex[0] = tuple(flex[0].split(','))
         #make it clear that this is a stable attribute
         #stab[1] = int(1)


      attributeList = []
      attributeList = stabAttributes + flexAttributes
      keys = []
      keys = stabKeys + flexKeys
      transactionDict = {}
      nullSet = set()

      for keyCount in xrange(len(keys)):
         tempList = []
         for values in attributeList[keyCount][0]:
            tempList.append((keys[keyCount]+values))
            transactionDict[(keys[keyCount]+values)] = set()
         
         #put in Null
         nullName = keys[keyCount]+nullValue
         tempList.append(nullName)
         transactionDict[nullName] = set()
         nullSet.add(nullName)

         tempList = [tuple(tempList)]
         
         #print "values: ", values[-1], "attributes: ", attributes[-1]
         tempList.insert(0, keys[keyCount])
         tempList.append(attributeList[keyCount][-1])
         attributeList.append(tempList)
         
      #put decision attributes into decision dictionary
      desiredAttr = []
      undesiredAttr = []
      decisions = decisionRE.findall(dataList)
      decisions = [i.split() for i in decisions]
      [i.pop(0) for i in decisions]
      decisions = [(i[0].split(':')) for i in decisions]


      decisionKeys = [i.pop(0) for i in decisions]
      #[keys.append(i.pop(0)) for i in decisions]
      for decision in decisions:
         decision[0] = decision[0].split(',')
         #decision[1] = int(decision[1])
      #decisionDict = dict(zip(keys, decisions))

      decisionList = []
   
      for decision in decisionKeys:
         for values in decisions:
            tempList = []
            for value in values[0]:
               tempList.append(decision+value)
               if value == values[-1]:
                  desiredAttr.append(decision+value)
                  transactionDict[decision+value] = set()
               elif value != values[-1]:
                  undesiredAttr.append(decision+value)
                  transactionDict[decision+value] = set()  
               #print decision, value
            tempList = [tuple(tempList)]
            #tempList = [tuple(tempList)]
            tempList.append(values[-1])
            tempList.insert(0, decision)
         decisionList.append(tempList)

      #make cost dict, currently deprecated
      commentString = '''
      costDict = dict()
      for attribute in attributeList:
         cost = attribute[-1]
         for value in attribute[1]:
            costDict[value] = cost
      '''
      #add data to transaction dict
      #allKeys = keys[:]
      allKeys = []
      [allKeys.append(i) for i in decisionKeys]
      [allKeys.append(i) for i in keys]
      dataScrubbed = dataRE.findall(dataList)
      #[allKeys.append(i) for i in decisionKeys]
      for line in dataScrubbed:
         line = line.split(',')
         #transactionID = line.pop(0)
         transactionID = 't'+str(dataScrubbed.index(','.join(line))+1)
         candidateIDs = zip(allKeys, line)
         for candidate in candidateIDs:
            tempID = ''.join(list(candidate))
            if tempID in transactionDict:
               transactionDict[tempID].add(transactionID)
            else:
               print("Invalid Item")
   return decisionList, attributeList, transactionDict, undesiredAttr, desiredAttr, nullSet

#from here on we have decisionList, attributeList, and transactionDict, [un]desiredAttr

#ruleList = []
#tempRule = []
def allRules(attributeList, first, nAttr, ruleList, tempRule):
   """generates all possible Conditions. We always assume undesireable to desireable for evaluating."""
   #ruleList = []
   for value in attributeList[first][1]:

      tempRule.append(value)


      if first < nAttr -1 :

         allRules(attributeList, first + 1, nAttr, ruleList, tempRule)
      elif first+1 == nAttr:

         #trim out invalid
         ruleList.append(tempRule[:])  
      if len(tempRule) > 0:
        tempRule.pop()     

def trimAllRules(allRules):
   tempList = []
   for cond, pred  in allRules:

      for i in xrange(len(cond)):

         #logic error
         if  (((cond[i] in nullSet and pred[i] not in nullSet) or ((cond[i] not in nullSet and pred[i]) in nullSet))):

            break    
      else: tempList.append((cond, pred))

   return tempList

def evaluateRule(transactionDict, nullSet, undesiredAttr, desiredAttr, ActionRule):
   """evaluates a population based on support and conf. Will later have cost and coverage added."""
   #support and confidence
   conditionalSetList = [transactionDict[i] for i in ActionRule[0] if i not in nullSet]
   if debugMode:
      #print("ActionRule: "
      #prettyPrintRule(ActionRule, nullSet)
      pass
   try:
      conditionSet = set.intersection(*conditionalSetList)
   #case when all attributes are null
   except TypeError:
      return (0.0,0.0,0.0)
   undesiredSet = undesiredAttr[0]
   conditionalSetList.append(transactionDict[undesiredSet])
   #print("Conditional Set List: ", conditionalSetList)
   #print "condition: ", ActionRule[0]
   #print("Conditional Set: ", conditionalSetList)
   conditionSetDecision = set.intersection(*conditionalSetList)
   #print("ConditionSetDecision: ", conditionSetDecision)
   #print conditionSet

   predictionSetList = [transactionDict[i] for i in ActionRule[1] if i not in nullSet]
   try:
      predictionSet = set.intersection(*predictionSetList)
   except TypeError:
      return (0.0,0.0,0.0)
   desiredSet = desiredAttr[0]
   predictionSetList.append(transactionDict[desiredSet])
   #print("Prediction Set List: ", predictionSetList)
   #print "prediction: ", ActionRule[1]
   #print("prediction Set: ", predictionSetList)
   predictionSetDecision = set.intersection(*predictionSetList)
   #print("Prediction Set Decision: ", predictionSetDecision)
   #this is correct if we do min{C/U, P/D}
   #support = min((len(conditionSetDecision)/ len(transactionDict[undesiredSet])), (len(predictionSetDecision) / len(transactionDict[desiredSet])))
   #numberOfTransactions = len(transactionDict[undesiredSet]) + len(transactionDict[desiredSet])
   #this is correct if we do min{C/TotalTransactions, P/totalTransactions
   numberUndesired = len(transactionDict[undesiredSet])
   numberDesired = len(transactionDict[desiredSet])
   numberOfTransactions = numberUndesired + numberDesired
   if evalFunction == 'aar':
      support = min((len(conditionSetDecision)/ numberOfTransactions), (len(predictionSetDecision) / numberOfTransactions))
   if evalFunction == 'gtr':
      condCov = len(conditionSetDecision) / numberOfTransactions
      predCov = len(predictionSetDecision) / numberOfTransactions
      try:
         purity = len(predictionSetDecision) / len(predictionSet)
      except ZeroDivisionError:
         purity = 0
   if debugMode:
      pass
      #print("Support: ", support)
      #print "support: ", support
   if evalFunction == 'aar':
      try:
         confidence = (len(conditionSetDecision)/len(conditionSet))*(len(predictionSetDecision)/len(predictionSet))
      except ZeroDivisionError:
         confidence = 0.0
   if debugMode:
      pass
      #print("confidence: ", confidence)
   
   #coverage
   if evalFunction == 'aar':
      coverage = len(conditionSetDecision) / numberUndesired
   if debugMode:
      pass
      #print("coverage: ", coverage)
      #print('\n')
   
   #cost: 
   #cost = 0.0
   #combination = zip(ActionRule[0], ActionRule[1])
   #for i in combination:
   #   if (i[0] != i[1]):
   #      cost += costDict[i[0]]
   #if cost > 1.0:
   #   cost = 1.0
   if evalFunction == 'aar':
      return support, confidence, coverage
   if evalFunction == 'gtr':
      return condCov, predCov, purity
def dataGenerator(attributeList, decisionList, startNumber, endNumber):
   """ genterator for more data. put in list comprehension and join the lists"""
   if debugMode == True:
      print(attributeList)
   for i in xrange(startNumber, endNumber):
      transIDstring = 't' + str(i)
      tempList = [random.choice(i[1][:-1]) for i in attributeList]
      tempList.append(random.choice(decisionList[0][1]))
      tempList.insert(0, transIDstring)
      yield tempList
 
def ruleGenerator(attributeList, nullSet):
   """generates valid action rules"""
   #random.seed()
   conditional, prediction = [], []
   for i in attributeList:
      flexOrStab = i[2]
      #print("flexOrStab: ", flexOrStab)
      tempCondition = random.choice(i[1])
      conditional.append(tempCondition)
      #print("attribute: ", attributeList)
      if tempCondition in nullSet:
         #make sure null is the last attribute added
         prediction.append(i[1][-1])
      elif (flexOrStab == 0):
         prediction.append(tempCondition)
      else:
         #print("got here: ")
         prediction.append(random.choice(i[1][:-1]))
   return conditional, prediction

def crossoverAR(rule1, rule2, nullSet, attributeList):
   #changed these from copies of original rules to actually modifying the rules.
   if debugMode:
      print("******************************Crossover***************************")
      print("Old Rules: ")
      print("Rule 1: ")
      prettyPrintRule(rule1, nullSet)
      #print(rule1[0])
      #print(rule1[1])
      print("Rule 2: ")
      prettyPrintRule(rule2, nullSet)
      #print(rule2[0])
      #print(rule2[1])
   #tempRule1, tempRule2 = rule1, rule2
   index = random.randint(0,len(rule1[0])-1)
   flexOrStab = attributeList[index][2]
   #tempRule1[0][index] = rule2[0][index]
   #tempRule2[0][index] = rule1[0][index]
   #if ((tempRule1[0][index] in nullSet) or (flexOrStab == 0)):
   #   tempRule1[1][index] = tempRule1[0][index]

   #if ((tempRule2[0][index] in nullSet) or (flexOrStab == 0)):
    #  tempRule2[1][index] = tempRule2[0][index]

   rule1[0][index], rule1[1][index], rule2[0][index], rule2[1][index] = rule2[0][index], rule2[1][index], rule1[0][index], rule1[1][index]
   if rule1[0][index] in nullSet or flexOrStab == 0:
      rule1[1][index] = rule1[0][index]
   if rule2[0][index] in nullSet or flexOrStab == 0:
      rule2[1][index] = rule1[0][index]
   if debugMode:
      print("New Rules: ")
      prettyPrintRule(rule1, nullSet)
      prettyPrintRule(rule2, nullSet)
      #prettyPrintRule(tempRule1, nullSet)
      #prettyPrintRule(tempRule2, nullSet)
   #return tempRule1, tempRule2
   return rule1, rule2

def mutateAR(rule, nullSet, attributeList):
   #changed this from copies of original rules to actually modifying the rule.
   tempRule = rule
   if debugMode:
      print("***************************Mutation******************************")
      print("Original Rule: ")
      #print(rule[1])
      prettyPrintRule(tempRule, nullSet)
   index = random.randint(0, len(tempRule[0])-1)
   flexOrStab = attributeList[index][2]
   tempRule[0][index] = random.choice(attributeList[index][1])
   tempRule[1][index] = random.choice(attributeList[index][1])
   if tempRule[0][index] in nullSet or flexOrStab == 0:
      tempRule[1][index] = tempRule[0][index]
   #redundant since it can change twice. Should protect against first attribute not null while second ist
   if tempRule[1][index] in nullSet or flexOrStab == 0:
      tempRule[0][index] = tempRule[1][index]
   #if tempRule[1][index]
   if debugMode:
      #print("New Rule: \n", tempRule[0])
      #print(tempRule[1])
      prettyPrintRule(tempRule, nullSet)
      print("******************************************************************")
      
   return tempRule
   
def prettyPrintRule(rule, nullSet):
   print("*************************Rule***************************\n")
   for i in xrange(len(rule[0])):
      if rule[0][i] not in nullSet:
         print(rule[0][i]+'-->'+rule[1][i]) 
   print("Support: %f, Confidence: %f, Coverage: %f\n" % rule.fitness.values)
   print("********************************************************\n")

def aarPrint(rule, nullSet, numTransactions, printFile=sys.stdout):
   tempSup , tempConf = rule.fitness.values[0], rule.fitness.values[1]
   #print("minSup: ", minSup, "tempSup: ", tempSup, "minConf: ", minConf, "tempConf: ", tempConf)
   if int(tempSup*numTransactions) >= minSup and tempConf >= minConf:
      print("@common", end=' ', file=printFile)
      tempString = 'Common'
   elif int(tempSup*numTransactions) < minSup and tempConf >= minConf:
      print("@rare", end=' ', file=printFile)
      tempString = 'Rare'
   else:
      print("got here")
      print("@junk", end=' ', file=printFile)
      tempString = 'Junk'
   lengthCounter = 0
   for i in xrange(len(rule[0])):
      if rule[0][i] not in nullSet:
         lengthCounter += 1
         attributeName = str((str(rule[0][i]).split('_'))[0])
         conditionStr = str((str(rule[0][i]).split('_'))[-1])
         changedStr = str((str(rule[1][i]).split('_'))[-1])
         print('['+attributeName+','+conditionStr, sep = '', end='', file=printFile)
         if conditionStr != changedStr:
            print('->'+changedStr, sep = '', end='', file=printFile)
         print(']', end = '', file=printFile)
   print(end='\t', file=printFile)
   #[print(i, end = ' ', file=printFile) for i in rule.fitness.values]
   if evalFunction == 'aar':
      support , confidence, coverage = rule.fitness.values
      print(int(support*numTransactions),' ',confidence,' ',coverage, lengthCounter, file=printFile)
   if evalFunction == 'gtr':
      conCov , predCov, purity = rule.fitness.values
      print(conCov,' ',predCov,' ',purity, file=printFile)
   return tempString, lengthCounter         
def aarWritePop(population, nullSet, numTransactions, stream=None):
   if stream is None:
      stream = sys.stdout
   rareList, commonList, junkList = [], [], []
   for index, level in enumerate(population):
      #print("Pareto Level: ", index, file=stream)
      #[aarPrint(rule, nullSet ,stream) for rule in level]         
      for rule in level:
         if rule.fitness.values[1] >= minConf:
            tempString , tempLength =  aarPrint(rule, nullSet, numTransactions, stream)
            if tempString == 'Rare':
               rareList.append(tempLength)
            elif tempString == 'Common': 
               commonList.append(tempLength)
            elif tempString == 'Junk':
               junkList.append(tempLength)
               
   numRare = len(rareList)
   numCommon = len(commonList)
   numJunk = len(junkList)
   try:
      avgRare = sum(rareList) / numRare
   except ZeroDivisionError:
      avgRare = 0
   try:
      avgCommon = sum(commonList) / numCommon
   except ZeroDivisionError:
      avgCommon = 0
   try:
      avgJunk = sum(junkList) / numJunk
   except ZeroDivisionError:
      avgJunk = 0
   print("#Rare:", numRare, "AveLength(Rare):", avgRare, "#Common:", numCommon, "Ave Length(Common):", avgCommon, "#Junk:", numJunk, "AveLength(Junk):", avgJunk)
def geneticProcedure(popSize, NGEN, CXPB, MUTPB, decisionList, attributeList, transactionDict, undesiredAttr, desiredAttr, nullSet, numberOfTransactions):

   #numberUndesired = len(transactionDict[undesiredSet])
   #numberDesired = len(transactionDict[desiredSet])
   #numberOfTransactions = numberUndesired + numberDesired   
   #numberOfTransactions = len(transactionDict) 
   #print(numberOfTransactions)
   creator.create("FitnessMulti", base.Fitness, weights=(1.0, 1.0, 1.0))

   #create individual
   creator.create("AtomicSet", tuple, fitness=creator.FitnessMulti)
   toolbox = base.Toolbox()
   
   toolbox.register("evaluate", evaluateRule, transactionDict, nullSet, undesiredAttr, desiredAttr)

   #multiple statistics
   if evalFunction == 'aar':
      objective1Name, objective2Name, objective3Name = 'Support' , 'Confidence', 'Coverage'

   
   if evalFunction == 'gtr':
      objective1Name, objective2Name, objective3Name = 'Conditional Coverage' , 'Prediction Coverage', 'Purity'

   #statsName1, statsName2, statsName3 = 'stats_'+objective1Name, 'stats_'+objective2Name, 'stats_'+objective3Name
   #stats1 = tools.Statistics(key=lambda ind: ind.fitness.values[0])
   #stats2 = tools.Statistics(key=lambda ind: ind.fitness.values[1])
   #stats3 = tools.Statistics(key=lambda ind: ind.fitness.values[2])
   stats = tools.Statistics(key=lambda ind: ind.fitness.values)

   #stats_size = tools.Statistics(key=len)
   #stats = tools.MultiStatistics( objective1 = stats1, objective2 = stats2, objective3 = stats3)

   stats.register("avg", numpy.mean, axis=0)
   stats.register("std", numpy.std, axis=0)
   stats.register("med", numpy.median, axis=0)
   stats.register("min", numpy.min, axis=0)
   stats.register("max", numpy.max, axis=0)

   logbook = tools.Logbook()

   fitnessArchive = []
   paretoArchive, paretoSet = [], set()
   pop = []
   #make pop in one for loop. Then genetic procedure in a second for loop. Currently breaks when NGEN > 1
   random.seed(1)

   if geneticProcedureStats:
      print("Order of Stats:", objective1Name, objective2Name, objective3Name, sep='\t')


   for genNumber in xrange(popSize):
      pop.append(creator.AtomicSet(ruleGenerator(attributeList, nullSet)))
   for i in pop:
      i.fitness.values = toolbox.evaluate(i)

   beforeFirstGen = timeit.default_timer()
   tempPopSize = popSize
   for g in xrange(NGEN):
      beforeGen = timeit.default_timer()
      if debugGeneticProcedure:
         print("***********************Generation: %d*********************\n" %g)
      intermediatePop = tools.sortNondominated(pop, tempPopSize)

      beforeAppend = timeit.default_timer()
      #[paretoArchive.append(toolbox.clone(i)) for i in intermediatePop[0]]
      #append to Pareto Archive while avoiding Repeats
      for rule in intermediatePop[0]:
         ruleString = str(rule)
         if ruleString not in paretoSet:
            paretoArchive.append(toolbox.clone(rule))
            paretoSet.add(ruleString)
      afterAppend = timeit.default_timer()
      if timer:
         #print("Paretor Append Time (sec) ", round(afterAppend-beforeAppend, 4))
         pass
      if debugGeneticProcedure:
        print("**********************Pareto Archive********************\n")
        for rule in paretoArchive:
           prettyPrintRule(rule, nullSet)
        print("********************************************************\n")
      
      #for mutation and crossover
      beforeCloneFlat = timeit.default_timer()
      intermediatePop = [j for i in map(toolbox.clone, intermediatePop) for j in i]
      #remove repeate rules
      noRepeats, noRepeatSet = [], set()
      for rule in intermediatePop:
         ruleString = str(rule)
         if ruleString not in noRepeatSet:
            noRepeats.append(rule)
            noRepeatSet.add(ruleString)


      #Pareto Select
      intermediatePop = noRepeats
      #this is to trim the population. We probably want to replace this with Roullette
      #TODO: this is redundant, as there is a SPEA2 selection at the top of the procedure. Need to try to remove once we are done testing. Should not affect results.
      intermediatePop = tools.selSPEA2(intermediatePop, popSize)
      #intermediatePop = tools.sortNondominated(intermediatePop, popSize)
      afterCloneFlat = timeit.default_timer()
      if timer:
         #print("Intermediate Length: ", len(intermediatePop))
         #print("Flatten Intermediate Pop (sec) ", round(afterCloneFlat-beforeCloneFlat, 4))
         pass
      
      for i in xrange(len(pop)):
         if random.random() < CXPB:
         #print("g ", g, " NGEN/(g +1) ", NGEN/(g+1))
         #if random.random()*NGEN < NGEN/(g+1):
            (intermediatePop.append(i) for i in crossoverAR(toolbox.clone(pop[i]), toolbox.clone(random.choice(pop)), nullSet, attributeList))
         if random.random() < MUTPB:
         #if random.random() < NGEN/(g+1):
            intermediatePop.append(mutateAR(toolbox.clone(pop[i]), nullSet, attributeList))
            #intermediatePop.append(creator.AtomicSet(ruleGenerator(attributeList, nullSet)))

      for i in intermediatePop:
         i.fitness.values = toolbox.evaluate(i)

      

      #pop = tools.selRoulette(intermediatePop, popSize)
      pop = intermediatePop
      record = stats.compile(pop)

      afterGen = timeit.default_timer()
      elapsedGen = afterGen - beforeGen
      if timer:
         print("Time for Gen ", g+1, " (sec): ", round(elapsedGen, 2)) 
         #pass
      if debugMode:
         print("record: ", record)
      logbook.record(Generation=g+1, Time=elapsedGen, **record)
      if geneticProcedureStats:
        print(logbook.stream)              

   comment = '''
   levelCounter = 0
   ruleCounter = 0
   for level in intermediatePop:
      levelCounter += 1
      for rule in level:
         ruleCounter += 1
      if ruleCounter >= popSize:
         tempPopSize = levelCounter
         break'''

   afterAllGens = timeit.default_timer()
   elapsedAfterGens = afterAllGens  - beforeFirstGen
   sortedPareto = tools.sortNondominated(paretoArchive, len(paretoArchive))

   allRules = pop

   [allRules.append(i) for i in paretoArchive]
   rmdupSet = set()
   #allRulesRmDup = [allRules[i] for i in xrange(len(allRules)) if str(allRules[i]) != str(allRules[i-1])]
   allRulesRmDup = []
   for rule in allRules:
      tempString = str(rule)
      if tempString not in rmdupSet:
         allRulesRmDup.append(rule)
         rmdupSet.add(tempString)


   allRulesRmDup = tools.sortNondominated(allRulesRmDup, len(allRulesRmDup))   

   #if timer:
   print("Pop Size:", popSize, "Num Gens:", NGEN, end=' ')
   print("Overall Execution Time (sec):", round(elapsedAfterGens, 2), end=' ')
   if printPop:
      #print("***********************Population*************************")
      #[prettyPrintRule(i, nullSet) for i in pop]
      #pass
      print("******************Top Level Pareto Archive****************")
      for index, level in enumerate(allRulesRmDup):
         print("Pareto Level: ", index)
         [prettyPrintRule(rule, nullSet) for rule in level]
   if aarPrintPop:
      '''
      #with open(outputFile+'PrintPop.out', 'w') as outFile:
      #   for index, level in enumerate(allRulesRmDup[:-1]):
      #      print("Pareto Level: ", index, file=outFile)
      #      [aarPrint(rule, nullSet ,outFile) for rule in level]
      '''
      if outputFileName != None:
         with open(outputFileName+'.out', 'w') as outFile:
            aarWritePop(allRulesRmDup[:-1], nullSet, numberOfTransactions, stream=outFile)
      else:
         aarWritePop(allRulesRmDup[:-1], nullSet, numberOfTransactions, stream=sys.stdout)
   logbook.header = "Generation", "Time", 'avg', 'med', 'std', 'min', 'max'
   #logbook.chapters['objective1'].header =  'avg', 'med', 'std', 'min', 'max'
   #logbook.chapters['objective2'].header =  'avg', 'med', 'std', 'min', 'max'
   #logbook.chapters['objective3'].header =  'avg', 'med', 'std', 'min', 'max'
   #logbook.chapters["size"].header = "min", "avg", "max"

   #print("support_ave: ", support_ave)
   #if geneticProcedureStats:
   #  print("Order of Stats:", objective1Name, objective2Name, objective3Name, sep='\t')
    #  print(logbook)

   gen = logbook.select("Generation")
   #objective1med = logbook.chapters['objective1'].select("med")
   #objective2med = logbook.chapters['objective2'].select("med")
   #objective3med = logbook.chapters['objective3'].select("med")

   #support_max = logbook.chapters["support"].select("max")
   #conf_mins = logbook.chapters["confidence"].select("min")
   #coverage_mins = logbook.chapters["coverage"].select("min")   

   objective1med = [i[0] for i in logbook.select("med")]
   objective2med = [i[1] for i in logbook.select("med")]
   objective3med = [i[2] for i in logbook.select("med")]

   #plot
   
   fig, ax1 = plt.subplots()
   fig.suptitle("Ojective Measures by Generation")
   
   label1 , label2, label3 = "Median "+objective1Name, "Median "+objective2Name, "Median "+objective3Name

   line1 = ax1.plot(gen, objective1med, linestyle="--", color = 'b', label= label1)
   line2 = ax1.plot(gen, objective2med, linestyle=":", color = 'k', label= label2)
   line3 = ax1.plot(gen, objective3med,linestyle="-", color = 'r', label= label3)
   paramString = "Population Size: "+str(popSize)+'\n'+"Number of Generations: "+str(NGEN)
   fig.text(0,0, paramString, fontsize=11)
   ax1.set_xlabel("Generation")
   ax1.set_ylabel("Magnitude", color="b")
   for tl in ax1.get_yticklabels():
       tl.set_color("b")

   #ax2 = ax1.twinx()
  
   #ax2.set_ylabel("Size", color="r")
   #for tl in ax2.get_yticklabels():
   #   tl.set_color("r")
   
   lns = line1 + line2 + line3
   #lns = line1
   labs = [l.get_label() for l in lns]
   ax1.legend(lns, labs, loc="lower right")
   plt.savefig(outputFileName)
   if displayPlotBool:
      plt.show()

   paretoCounter = 1

def main(popSize, NGEN):
   if dataFormatOld:
      decisionList, attributeList, transactionDict, undesiredAttr, desiredAttr, nullSet, numTransactions = readinFile(dataFile)
   else:
      decisionList, attributeList, transactionDict, undesiredAttr, desiredAttr, nullSet = readNewFormat(dataFile)

   #population size and number of generations
   #popSize = 150
   #NGEN = 1000

   #crossover and mutation probability
   CXPB = .5
   MUTPB = .5

   return geneticProcedure(popSize, NGEN, CXPB, MUTPB, decisionList, attributeList, transactionDict, undesiredAttr, desiredAttr, nullSet, numTransactions)
main(popSize, NGEN)

