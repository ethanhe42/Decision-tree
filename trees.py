from math import log
import operator
import numpy as np

leavesCnt=0
def entropy(dataSet):
    numEntries = len(dataSet)
    labelCounts = {}
    for featVec in dataSet: #the the number of unique elements and their occurance
        currentLabel = featVec[-1]
        if currentLabel not in labelCounts.keys(): labelCounts[currentLabel] = 0
        labelCounts[currentLabel] += 1
    ent = 0.0
    for key in labelCounts:
        prob = float(labelCounts[key])/numEntries
        imp=-prob*log(prob,2)
        ent += imp #log base 2
    return ent

def splitDataSet(dataSet, axis, value):
    retDataSet = []
    for featVec in dataSet:
        if featVec[axis] == value:
            reducedFeatVec = featVec[:axis]     #chop out axis used for splitting
            reducedFeatVec.extend(featVec[axis+1:])
            retDataSet.append(reducedFeatVec)
    return retDataSet

def chooseBestFeatureToSplit(dataSet,labels):
    numFeatures = len(dataSet[0]) - 1      #the last column is used for the labels
    baseEntropy = entropy(dataSet)
    bestInfoGain = 0.0; bestFeature = 0
    for i in range(numFeatures):        #iterate over all the features
        featList = [example[i] for example in dataSet]#create a list of all the examples of this feature
        uniqueVals = set(featList)       #get a set of unique values
        newEntropy = 0.0
        print labels[i],'impurity'
        for value in uniqueVals:
            subDataSet = splitDataSet(dataSet, i, value)
            prob = len(subDataSet)/float(len(dataSet))

            sub_ent=entropy(subDataSet)
            print value,sub_ent
            newEntropy +=prob*sub_ent
        infoGain = baseEntropy - newEntropy     #calculate the info gain; ie reduction in entropy
        print 'information Gain',infoGain
        print 'Total impurity', newEntropy,'\n'
        if (infoGain > bestInfoGain):       #compare this to the best gain so far
            bestInfoGain = infoGain         #if better than current best, set to best
            bestFeature = i
    return bestFeature,bestInfoGain
    #returns an integer

def findClass(classList,rank):
    global leavesCnt
    classCount={}
    for i in ['Yes','No']:
        classCount[i]=0
    for vote in classList:
        if vote not in classCount.keys(): 
            classCount[vote] = 0
        classCount[vote] += 1
    clas='Yes'
    for vote in classList:
        if classCount[vote]>classCount[clas]:
            clas=vote
    infos=[classCount['Yes'],classCount['No'],(classCount['Yes']+1.0)/(classCount['Yes']+classCount['No']+2),leavesCnt]
    leavesCnt+=1
    rank.append(infos)
    return clas,infos

def sortRankingTree(rankingTree,rank):
    sorted_rank=np.array(rank).T[-2:]
    idx=(-sorted_rank[0]).argsort()
    sorted_idx=sorted_rank[1][idx]
    #print sorted_idx
    sorted_prob=sorted_rank[0][idx]
    #print sorted_prob
    new_ranks=[1]
    for i in range(len(sorted_prob[1:])):
        if sorted_prob[i+1]==sorted_prob[i]:
            new_ranks.append(new_ranks[-1])
        else:
            new_ranks.append(new_ranks[-1]+1)
    #print new_ranks
    ret_idx=sorted_idx.argsort().astype(int)
    ret_ranks=np.array(new_ranks)[ret_idx]
    return ret_ranks

def traverseLeaves(rankingTree,func):
    pass



def rankingTree2string(rankTree):
    firstStr = rankTree.keys()[0]
    secondDict = rankTree[firstStr]
    for valueOfFeat  in secondDict:
        item=secondDict[valueOfFeat]
        if isinstance(item, dict):
            rankingTree2string(item)
        else: 
            string=str(item[:2])+'\n'
            string+="{:2.1f}".format(item[-2]*100.0)+'%\n'
            string+='rank'+str(item[-1])
            secondDict[valueOfFeat]=string


def Rank(rankTree,rank):
    firstStr = rankTree.keys()[0]
    secondDict = rankTree[firstStr]
    for valueOfFeat  in secondDict:
        item=secondDict[valueOfFeat]
        if isinstance(item, dict):
            Rank(item,rank)
        else: 
            secondDict[valueOfFeat][-1]=rank[item[-1]]

def getUniqueVals(dataSet,labels):
    uniqueVals=dict()
    i=0
    for feature in dataSet.T[:-1]:
        uniqueVals[labels[i]]=set(feature)
        i+=1
    return uniqueVals

def createTree(dataSet,labels,ValsSet,node='root',rank=None):
    #check impurity and if we've run out of features
    classList = [example[-1] for example in dataSet]
    if classList.count(classList[0]) == len(classList) or len(dataSet[0])==1:
        return findClass(classList,rank)
    print '================================================================'
    print node
    print '----------------------------------------------------------------'
    bestFeat,bestInfoGain = chooseBestFeatureToSplit(dataSet,labels)
    #if bestInfoGain==0:
    #    return findClass(classList,rank)
    bestFeatLabel = labels[bestFeat]
    print 'I choose',bestFeatLabel
    node+='->'+bestFeatLabel+'='
    myTree = {bestFeatLabel:{}}
    rankTree={bestFeatLabel:{}}
    del(labels[bestFeat])
    #print bestFeat
    featValues = [example[bestFeat] for example in dataSet]
    #print featValues
    uniqueVals = set(featValues)
    if len(uniqueVals)!=len(ValsSet[bestFeatLabel]):
       # some value have no example
       for val in ValsSet[bestFeatLabel]:
           if val not in uniqueVals:
               l,votes=findClass(classList,rank)
               myTree[bestFeatLabel][val]=l
               rankTree[bestFeatLabel][val]=[0,0,.5,votes[-1]]
            
    for value in uniqueVals:
        #print value
        subLabels = labels[:]       #copy all of labels, so trees don't mess up existing labels
        myTree[bestFeatLabel][value],rankTree[bestFeatLabel][value]\
                = createTree(splitDataSet(dataSet, bestFeat, value),subLabels,ValsSet,node=node+value,rank=rank)
    return myTree,rankTree #also return a ranking tree

def classify(inputTree,featLabels,testVec):
    firstStr = inputTree.keys()[0]
    secondDict = inputTree[firstStr]
    featIndex = featLabels.index(firstStr)
    key = testVec[featIndex]
    valueOfFeat = secondDict[key]
    if isinstance(valueOfFeat, dict):
        classLabel = classify(valueOfFeat, featLabels, testVec)
    else: classLabel = valueOfFeat
    return classLabel


#def storeTree(inputTree,filename):
#    import pickle
#    fw = open(filename,'w')
#    pickle.dump(inputTree,fw)
#    fw.close()
#
#def grabTree(filename):
#    import pickle
#    fr = open(filename)
#    return pickle.load(fr)

