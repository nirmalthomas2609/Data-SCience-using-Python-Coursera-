
# coding: utf-8

# ---
# 
# _You are currently looking at **version 1.2** of this notebook. To download notebooks and datafiles, as well as get help on Jupyter notebooks in the Coursera platform, visit the [Jupyter Notebook FAQ](https://www.coursera.org/learn/python-data-analysis/resources/0dhYG) course resource._
# 
# ---

# # Assignment 2 - Pandas Introduction
# All questions are weighted the same in this assignment.
# ## Part 1
# The following code loads the olympics dataset (olympics.csv), which was derrived from the Wikipedia entry on [All Time Olympic Games Medals](https://en.wikipedia.org/wiki/All-time_Olympic_Games_medal_table), and does some basic data cleaning. 
# 
# The columns are organized as # of Summer games, Summer medals, # of Winter games, Winter medals, total # number of games, total # of medals. Use this dataset to answer the questions below.

# In[2]:

import pandas as pd

df = pd.read_csv('olympics.csv', index_col=0, skiprows=1)

for col in df.columns:
    if col[:2]=='01':
        df.rename(columns={col:'Gold'+col[4:]}, inplace=True)
    if col[:2]=='02':
        df.rename(columns={col:'Silver'+col[4:]}, inplace=True)
    if col[:2]=='03':
        df.rename(columns={col:'Bronze'+col[4:]}, inplace=True)
    if col[:1]=='№':
        df.rename(columns={col:'#'+col[1:]}, inplace=True)

names_ids = df.index.str.split('\s\(') # split the index by '('

df.index = names_ids.str[0] # the [0] element is the country name (new index) 
df['ID'] = names_ids.str[1].str[:3] # the [1] element is the abbreviation or ID (take first 3 characters from that)
df = df.drop('Totals')
df[100:146]


# ### Question 0 (Example)
# 
# What is the first country in df?
# 
# *This function should return a Series.*

# In[3]:

# You should write your whole answer within the function provided. The autograder will call
# this function and compare the return value against the correct solution value
def answer_zero():
    # This function returns the row for Afghanistan, which is a Series object. The assignment
    # question description will tell you the general format the autograder is expecting
    
    return df.iloc[0]

# You can examine what your function returns by calling it in the cell. If you have questions
# about the assignment formats, check out the discussion forums for any FAQs
answer_zero() 


# ### Question 1
# Which country has won the most gold medals in summer games?
# 
# *This function should return a single string value.*

# In[4]:

import numpy as np
def answer_one():
    for m in (df[df['Gold']==np.max(df['Gold'])]).index:
        return m
answer_one()


# ### Question 2
# Which country had the biggest difference between their summer and winter gold medal counts?
# 
# *This function should return a single string value.*

# In[5]:

def answer_two():
    copy_df=df.copy()
    copy_df['Gold.3']=copy_df['Gold']-copy_df['Gold.1']
    k=np.max(copy_df['Gold.3'])
    s=copy_df[copy_df['Gold.3']==k]
    del copy_df['Gold.3']
    for m in s.index:
       return m

#    return "YOUR ANSWER HERE"
#answer_two()


# ### Question 3
# Which country has the biggest difference between their summer gold medal counts and winter gold medal counts relative to their total gold medal count? 
# 
# $$\frac{Summer~Gold - Winter~Gold}{Total~Gold}$$
# 
# Only include countries that have won at least 1 gold in both summer and winter.
# 
# *This function should return a single string value.*

# In[60]:

def answer_three():
    copy_df=df.copy()
    copy_df=copy_df[(copy_df['Gold']>=1) & (copy_df['Gold.1']>=1)]
    copy_df['rel']=(copy_df['Gold']-copy_df['Gold.1'])/copy_df['Gold.2']
    k=np.max(copy_df['rel'])
    s=copy_df[(copy_df['rel']==k)]
    del copy_df['rel']
    for m in s.index:
        return m
#    return "YOUR ANSWER HERE"


# ### Question 4
# Write a function that creates a Series called "Points" which is a weighted value where each gold medal (`Gold.2`) counts for 3 points, silver medals (`Silver.2`) for 2 points, and bronze medals (`Bronze.2`) for 1 point. The function should return only the column (a Series object) which you created.
# 
# *This function should return a Series named `Points` of length 146*

# In[3]:

def answer_four():
    Points=(df["Gold.2"]*3)+(df["Silver.2"]*2)+df["Bronze.2"]
    return Points


# ## Part 2
# For the next set of questions, we will be using census data from the [United States Census Bureau](http://www.census.gov/popest/data/counties/totals/2015/CO-EST2015-alldata.html). Counties are political and geographic subdivisions of states in the United States. This dataset contains population data for counties and states in the US from 2010 to 2015. [See this document](http://www.census.gov/popest/data/counties/totals/2015/files/CO-EST2015-alldata.pdf) for a description of the variable names.
# 
# The census dataset (census.csv) should be loaded as census_df. Answer questions using this as appropriate.
# 
# ### Question 5
# Which state has the most counties in it? (hint: consider the sumlevel key carefully! You'll need this for future questions too...)
# 
# *This function should return a single string value.*

# In[10]:

census_df = pd.read_csv('census.csv')
census_df


# In[7]:

def answer_five():
    cdf=census_df.copy()
    a=cdf['STNAME'].unique()
    t={cdf[cdf["STNAME"]==j]["CTYNAME"].size:j for j in a}
    t=pd.Series(t)
    l=t.keys()
    l=pd.Series(l)
    f=np.max(l)
    return t.loc[f]
answer_five()


# ### Question 6
# Only looking at the three most populous counties for each state, what are the three most populous states (in order of highest population to lowest population)? Use `CENSUS2010POP`.
# 
# *This function should return a list of string values.*

# In[20]:

import numpy as np
def answer_six():
    cdf=census_df.copy()
    cdf=cdf[cdf["SUMLEV"]==50]
    a=cdf["STNAME"].unique()
    l={}    
    for j in a:
        t=cdf[cdf["STNAME"]==j]
        col=["CENSUS2010POP"]
        t=t.sort(['CENSUS2010POP'],ascending=False) #sort function does not sort the data frame in place.
        k=t[col]
        p=0
        m=0
        z=k['CENSUS2010POP']
        for g in z:
            p=p+k.iloc[m]
            m+=1
            if(m>=3):
                break
        l[j]=p
    l=pd.DataFrame(l)
    l=l.T
    l=l.sort(['CENSUS2010POP'],ascending=False)
    oo=l.index
    l['states']=oo
    f=[l.iloc[0]['states'],l.iloc[1]['states'],l.iloc[2]['states']]
    return f


# ### Question 7
# Which county has had the largest absolute change in population within the period 2010-2015? (Hint: population values are stored in columns POPESTIMATE2010 through POPESTIMATE2015, you need to consider all six columns.)
# 
# e.g. If County Population in the 5 year period is 100, 120, 80, 105, 100, 130, then its largest change in the period would be |130-80| = 50.
# 
# *This function should return a single string value.*

# In[73]:

import numpy as np
def answer_seven():
    cdf=census_df.copy()
    cdf=cdf[cdf["SUMLEV"]==50]
    col=["POPESTIMATE201%d"% i for i in range (6)]
    cdf=cdf.set_index(["CTYNAME"])
    cdf=cdf[col]
    cdf["test"]=np.max(cdf[col],axis=1)-np.min(cdf[col],axis=1)
    k=cdf.index
    cdf["counties"]=k
    j=np.max(cdf["test"])
    cdf=cdf.set_index(["test"])
    t=cdf.loc[j,"counties"]
    return t
answer_seven()


# In[ ]:




# #### Question 8
# In this datafile, the United States is broken up into four regions using the "REGION" column. 
# 
# Create a query that finds the counties that belong to regions 1 or 2, whose name starts with 'Washington', and whose POPESTIMATE2015 was greater than their POPESTIMATE 2014.
# 
# *This function should return a 5x2 DataFrame with the columns = ['STNAME', 'CTYNAME'] and the same index ID as the census_df (sorted ascending by index).*

# In[13]:

def answer_eight():
    cdf=census_df.copy()
    cdf=cdf[cdf["SUMLEV"]==50]
    cdf=cdf[(cdf["REGION"]==1) | (cdf["REGION"]==2)]
    cdf=cdf[cdf["POPESTIMATE2015"]>cdf["POPESTIMATE2014"]]
    col=["STNAME","CTYNAME"]
    cdf["test"]=pd.Series([cdf.loc[i]["CTYNAME"][0:10] for i in (cdf.index)],index=cdf.index)
    cdf=cdf[cdf["test"]=="Washington"]
#    col=col+["test"]
#    cdf=cdf[col]
    return cdf[col]
answer_eight()


# In[ ]:



