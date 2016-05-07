from trees import *
from treePlotter import *
import numpy as np
import pandas as pd

rank=[]

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
print rank
rankingTree2string(rankTree)
createPlot(rankTree)
exit()
 #createPlot(myTree)

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


