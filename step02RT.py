#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 14 21:18:32 2025

@author: pburgos
"""

from glob import glob
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pingouin as pg

files = glob("./reports/output2*.xlsx", recursive = True)

new_rc_params = {'text.usetex': False,
"svg.fonttype": 'none','font.size': 18
}
plt.rcParams.update(new_rc_params)   



dfs = []
for fi in files:
    df = pd.read_excel(fi)
    dfs.append(df)
    
df2 = pd.concat(dfs)
df2.to_excel('review_data.xlsx')


var = ['total yes number', 'error extra yes', 'error missing yes', 'mean RT',
'std RT']
df3 = df2.groupby(["Sub_ID","condition"],as_index=False)[var].mean()
df3.condition[df3.condition==0]='ST'
df3.condition[df3.condition==1]='DT_Walk'
df3.condition[df3.condition==2]='DT_Turn'
df3['error'] = df3[['error extra yes', 'error missing yes']].sum(axis=1).astype('int64')
df3["group"] = np.nan
df3.group[df3.Sub_ID.str.contains('AUT_2')]='HC'
df3.group[df3.Sub_ID.str.contains('AUT_0')]='PD'


df3PD = df3[df3.group=='PD']
df3HC = df3[df3.group=='HC']


# var = ["a","b","c"]
# inter5d = df.groupby(["file","subject","stage"],as_index=False)[var].mean() 

plt.figure()
sns.boxplot(data=df3,x="condition",y="mean RT")
sns.stripplot(data=df3,x="condition",y="mean RT")
plt.title("PD+HC")

plt.figure()
sns.boxplot(data=df3,x="condition",y="std RT")
sns.stripplot(data=df3,x="condition",y="std RT")
plt.title("PD+HC")

plt.figure()
sns.boxplot(data=df3,x="condition",y="error")
sns.stripplot(data=df3,x="condition",y="error")
plt.title("PD+HC")


plt.figure()
sns.boxplot(data=df3PD,x="condition",y="mean RT")
sns.stripplot(data=df3PD,x="condition",y="mean RT")
plt.ylim([None,0.85])
phoc1=pg.pairwise_tests(data=df3PD,dv="mean RT",within="condition",subject="Sub_ID",padjust='holm') #within_first=False

plt.figure()
sns.boxplot(data=df3PD,x="condition",y="std RT")
sns.stripplot(data=df3PD,x="condition",y="std RT")
plt.ylim([None,0.24])
plt.show()
phoc2=pg.pairwise_tests(data=df3PD,dv="std RT",within="condition",subject="Sub_ID",padjust='holm') #within_first=False


# plt.title("PD")

plt.figure()
sns.boxplot(data=df3PD,x="condition",y="error")
sns.stripplot(data=df3PD,x="condition",y="error")
# plt.title("PD")




plt.figure()
sns.barplot(data=df3,x="condition",y="mean RT", hue='group')
plt.ylim([0.4,0.8])
phoc3=pg.pairwise_tests(data=df3,between='group',dv="mean RT",within="condition",subject="Sub_ID",padjust='holm') #within_first=False



plt.figure()
sns.barplot(data=df3,x="condition",y="std RT", hue='group')
plt.ylim([0.02,0.16])
# sns.stripplot(data=df3,x="condition",y="std RT")
phoc4=pg.pairwise_tests(data=df3,between='group',dv="std RT",within="condition",subject="Sub_ID",padjust='holm') #within_first=False



plt.figure()
sns.boxplot(data=df3HC,x="condition",y="mean RT")
sns.stripplot(data=df3HC,x="condition",y="mean RT")
plt.ylim([None,0.85])
phoc5=pg.pairwise_tests(data=df3HC,dv="mean RT",within="condition",subject="Sub_ID",padjust='holm') #within_first=False

plt.figure()
sns.boxplot(data=df3HC,x="condition",y="std RT")
sns.stripplot(data=df3HC,x="condition",y="std RT")
plt.ylim([None,0.24])
plt.show()
phoc6=pg.pairwise_tests(data=df3HC,dv="std RT",within="condition",subject="Sub_ID",padjust='holm') #within_first=False





plt.show()

print(len(df3PD.Sub_ID.unique()))
print(len(df3HC.Sub_ID.unique()))
