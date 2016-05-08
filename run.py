from trees import *
from treePlotter import *
import numpy as np
import pandas as pd
import sys
sys.stdout = open("decision.txt", "w")
rank=[]
decision=True
def getData(filename):
    raw_train=pd.read_excel(filename,index_col=0)

    dataset=np.array(raw_train,dtype=str).tolist()

    label=np.array(raw_train.T.index,dtype=str)[:-1].tolist()

    obj=np.array(raw_train.T.index,dtype=str)[-1]
    
    return dataset,label,obj
dataset,label,obj=getData('train.xlsx')
u=getUniqueVals(np.array(dataset),label)
myTree,rankTree=createTree(dataset,label,u,rank=rank)
rank=sortRankingTree(rankTree,rank)
Rank(rankTree,rank)
#print rank

def DTmetric(myTree=myTree):
    sys.stdout = open("classify.txt", "w")
    for i in range(3):
        name='HW3 - Test data set '+str(i)+'.xlsx'
        if i==0:
            name='train.xlsx'
        dataset,label,obj=getData(name)
        print name
        res=[]
        idx=[]
        for j,cnt in zip(dataset,range(1,len(dataset)+1)):
            clas=classify(myTree,label,j)
            #print clas
            if clas != j[-1]:
                idx.append(cnt)
                res.append(j)
    
        res=pd.DataFrame(res)
        res.columns=label+[obj]
        res.index=idx
        print res
        print 'error rate',float(len(idx))/len(dataset)
    
    
def RTmetric(rankTree=rankTree):
    sys.stdout = open("ranking.txt", "w")
    for i in range(3):
        name='HW3 - Test data set '+str(i)+'.xlsx'
        if i==0:
            name='train.xlsx'
        dataset,label,obj=getData(name)
        print name
        ranks=[[],[]]
        for j,cnt in zip(dataset,range(1,len(dataset)+1)):
            clas=classify(rankTree,label,j,True)
            if j[-1]=='Yes':
                ranks[0].append(clas)
            else:
                ranks[1].append(clas)
        ranks=pd.DataFrame(ranks).T
        ranks=ranks.apply(pd.value_counts).fillna(0).astype(int)
        ranks.columns=['Yes','No']
        err=0
        err_each_level=[]
        idx=ranks.index
        for level in range(len(ranks)):
            neg=ranks.ix[idx[level]]['No']
            err_in_this_level=0
            for sublevel in range(level,len(ranks)):
                pos=ranks.ix[idx[sublevel]]['Yes']
                if idx[sublevel]==idx[level]:
                    pos*=.5
                err_in_this_level+=neg*pos
                err+=neg*pos
            err_each_level.append(err_in_this_level)
        print 'error each level',err_each_level,'total',err
        err_rate=float(err)/ranks.sum().prod()
        print ranks.append(pd.Series(ranks.sum(),name='Total'))
        print 'error rate',err_rate
        print 'accuracy',1-err_rate,'\n'

print '\n'
if decision==False:
    RTmetric(rankTree)
    rankingTree2string(rankTree)
    createPlot(rankTree)
else:
    DTmetric(myTree)
    createPlot(myTree)
