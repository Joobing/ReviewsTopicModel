

import glob
import pandas as pd
import numpy as np

pd.set_option('display.max_columns', None)  

'''prnc=pd.read_csv("D:\\r\\title.principals.tsv", sep="\t")
bscs=pd.read_csv("D:\\r\\title.basics.tsv", sep="\t")
rtng=pd.read_csv("D:\\r\\title.ratings.tsv", sep="\t")'''
tts=pd.read_csv("e:\\#CULT\\AOM2019.txt", sep="\t").iloc[0:107,0:11]
i=1
df=pd.read_json('M:/'+tts.Const[0]+'.json', orient='records').assign(tconst=tts.Const[0])
for tt in tts.Const[1:10]:#7
    if tt+".json" in [f.replace('M:\\','') for f in glob.glob("M:\*.json")]:
        i+=1
        print(i,"-",tt)
        df=df.append(pd.read_json('M:/'+tt+'.json', orient='records').assign(tconst=tt))
    else:
        print("!",tt,"-", tts[tts.Const==tt].Title)


df=df.set_index('tconst')
df.rating=df.rating.apply(lambda x: int(x.replace('/','')) if x is not None else x)
df['date'] = pd.to_datetime(df['date'])
df['month'], df['day'], df['year'] = df['date'].dt.month, df['date'].dt.day, df['date'].dt.year
df['all']=df.helpful.apply(lambda x: int(x.split(' out of ')[1].replace(',','')) if x is not None else x)
df['helpful']=df.helpful.apply(lambda x: int(x.split(' out of ')[0].replace(',','')) if x is not None else x)
df['length']=df.content.apply(lambda x: x.count(' ') if x is not None else x)

tts= tts.set_index('Const')
tts['release'] = tts['Release Date'].astype('datetime64[ns]')
df=df.join(tts.release.dt.year)
df=df.join(tts.Listed)

df.loc[df.Listed=='BFI'].rating.mean()
df.loc[df.Listed=='Oscars'].groupby(df.loc[df.Listed=='Oscars'].index).rating.mean()
#pd.to_numeric(df.A, errors='coerce').notnull() & (df.A > 0)
df['positive']=df.rating.apply(np.isreal) & (df.rating > 6)
df.head()

#set(tts.tconst.iloc[0:2].astype(str)) in set(df.tconst.astype(str))

lng=df[(df.release>1997) & ( df.year>df.release+1) & (df.year<df.release+10)]
cnt=pd.DataFrame(lng[lng.positive==True].groupby([lng[lng.positive==True].index,'year']).positive.value_counts().diff())
cnt.index.names=['tconst', 'year', 'pos']
trnd= cnt.groupby(['tconst']).mean()
PRMP=trnd.loc[trnd.positive>0]
TEMP=trnd.loc[trnd.positive<0.00000000000000000000000001]
shrt=df[( df.year<df.release+2)]
del shrt, lng
TEMP.join(tts[['Listed','release']])
PRMP.join(tts[['Listed','release']])

#df.groupby(df.index).size().apply(np.arange)
df['id']=[a+"-"+b for a,b in zip(list(df.index),list(df.groupby(df.index).cumcount().apply(str)))]
tmp=pd.DataFrame()           


LGLN=df.loc[(df.Listed=='BFI') & ( df.length>49) & (df.year>df.release+1), ['id', 'content']]
LGLN.set_index('id', inplace=True)

PRLN=df.loc[(df.Listed=='Oscars') & (df.index.isin(PRMP.index)) & ( df.length>49) & (df.year>df.release+1), ['id', 'content']]
PRLN.set_index('id', inplace=True)

TMLN=df.loc[(df.Listed=='Oscars') & (df.index.isin(TEMP.index)) & ( df.length>49) & (df.year>df.release+1), ['id', 'content']]
TMLN.set_index('id', inplace=True)


LGSH=df.loc[(df.Listed=='BFI') & ( df.length>49) & (df.year<df.release+2), ['id', 'content']]
LGSH.set_index('id', inplace=True)

PRSH=df.loc[(df.Listed=='Oscars') & (df.index.isin(PRMP.index)) & ( df.length>49) & (df.year<df.release+2), ['id', 'content']]
PRSH.set_index('id', inplace=True)

TMSH=df.loc[(df.Listed=='Oscars') & (df.index.isin(TEMP.index)) & ( df.length>49) & (df.year<df.release+2), ['id', 'content']]
TMSH.set_index('id', inplace=True)
    
                











# -*- coding: utf-8 -*-
"""
Created on Tue Jan  7 15:25:08 2020

@author: u811717
"""

#dtypes(USER['The Hours'].rating)
#set(USER['The Hours'].rating.apply(type))
