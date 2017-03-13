
# coding: utf-8

# ---
# 
# _You are currently looking at **version 1.0** of this notebook. To download notebooks and datafiles, as well as get help on Jupyter notebooks in the Coursera platform, visit the [Jupyter Notebook FAQ](https://www.coursera.org/learn/python-data-analysis/resources/0dhYG) course resource._
# 
# ---

# # The Series Data Structure

# In[5]:

import pandas as pd


# In[4]:

animals = ['Tiger', 'Bear', 'Moose']
pd.Series(animals)


# In[5]:

numbers = [1, 2, 3]
pd.Series(numbers)


# In[6]:

animals = ['Tiger', 'Bear', None]
pd.Series(animals)


# In[7]:

numbers = [1, 2, None]
pd.Series(numbers)


# In[8]:

import numpy as np
np.nan == None


# In[9]:

np.nan == np.nan


# In[10]:

np.isnan(np.nan)


# In[11]:

sports = {'Archery': 'Bhutan',
          'Golf': 'Scotland',
          'Sumo': 'Japan',
          'Taekwondo': 'South Korea'}
s = pd.Series(sports)
s


# In[12]:

s.index


# In[13]:

s = pd.Series(['Tiger', 'Bear', 'Moose'], index=['India', 'America', 'Canada'])
s


# In[14]:

sports = {'Archery': 'Bhutan',
          'Golf': 'Scotland',
          'Sumo': 'Japan',
          'Taekwondo': 'South Korea'}
s = pd.Series(sports, index=['Golf', 'Sumo', 'Hockey'])
s


# # Querying a Series

# In[15]:

sports = {'Archery': 'Bhutan',
          'Golf': 'Scotland',
          'Sumo': 'Japan',
          'Taekwondo': 'South Korea'}
s = pd.Series(sports)
s


# In[16]:

s.iloc[3]


# In[17]:

s.loc['Golf']


# In[18]:

s[3]


# In[19]:

s['Golf']


# In[ ]:

sports = {99: 'Bhutan',
          100: 'Scotland',
          101: 'Japan',
          102: 'South Korea'}
s = pd.Series(sports)
s


# In[ ]:

s[0] #This won't call s.iloc[0] as one might expect, it generates an error instead


# In[ ]:

s = pd.Series([100.00, 120.00, 101.00, 3.00])
s


# In[ ]:

total = 0
for item in s:
    total+=item
print(total)


# In[ ]:

import numpy as np

total = np.sum(s)
print(total)


# In[ ]:

#this creates a big series of random numbers
s = pd.Series(np.random.randint(0,1000,10000))
s.head()
#print (len(s))


# In[ ]:

len(s)


# In[31]:

get_ipython().run_cell_magic('timeit', '-n 100', 'summary = 0\nfor item in s:\n    summary+=item')


# In[32]:

get_ipython().run_cell_magic('timeit', '-n 100', 'summary = np.sum(s)')


# In[39]:

s+=2 #adds two to each item in s using broadcasting
s.head()


# In[40]:

for label, value in s.iteritems():
    s.set_value(label, value+2)
s.head()


# In[1]:

get_ipython().run_cell_magic('timeit', '-n 10', 's = pd.Series(np.random.randint(0,1000,10000))\nfor label, value in s.iteritems():\n    s.loc[label]= value+2')


# In[ ]:

get_ipython().run_cell_magic('timeit', '-n 10', 's = pd.Series(np.random.randint(0,1000,10000))\ns+=2')


# In[2]:

s = pd.Series([1, 2, 3])
s.loc['Animal'] = 'Bears'
s


# In[3]:

original_sports = pd.Series({'Archery': 'Bhutan',
                             'Golf': 'Scotland',
                             'Sumo': 'Japan',
                             'Taekwondo': 'South Korea'})
cricket_loving_countries = pd.Series(['Australia',
                                      'Barbados',
                                      'Pakistan',
                                      'England'], 
                                   index=['Cricket',
                                          'Cricket',
                                          'Cricket',
                                          'Cricket'])
all_countries = original_sports.append(cricket_loving_countries)


# In[4]:

original_sports


# In[ ]:

cricket_loving_countries


# In[ ]:

all_countries


# In[ ]:

all_countries.loc['Cricket']


# # The DataFrame Data Structure

# In[7]:

import pandas as pd
purchase_1 = pd.Series({'Name': 'Chris',
                        'Item Purchased': 'Dog Food',
                        'Cost': 22.50})
purchase_2 = pd.Series({'Name': 'Kevyn',
                        'Item Purchased': 'Kitty Litter',
                        'Cost': 2.50})
purchase_3 = pd.Series({'Name': 'Vinod',
                        'Item Purchased': 'Bird Seed',
                        'Cost': 5.00})
df = pd.DataFrame([purchase_1, purchase_2, purchase_3], index=['Store 1', 'Store 1', 'Store 2'])
df.head()


# In[9]:

df.loc['Store 2']


# In[10]:

type(df.loc['Store 2'])


# In[11]:

df.loc['Store 1']


# In[12]:

df.loc['Store 1', 'Cost']


# In[18]:

df.T
df


# In[14]:

df.T.loc['Cost']


# In[15]:

df['Cost']


# In[19]:

df.loc['Store 1']['Cost']


# In[17]:

df.loc[:,['Name', 'Cost']]


# In[20]:

df.drop('Store 1')


# In[21]:

df


# In[22]:

copy_df = df.copy()
copy_df = copy_df.drop('Store 1')
copy_df


# In[ ]:




# In[24]:

del copy_df['Name']
copy_df


# In[25]:

df['Location'] = None
df


# # Dataframe Indexing and Loading

# In[26]:

costs = df['Cost']
costs


# In[27]:

costs+=2
costs


# In[28]:

df


# In[29]:

get_ipython().system('cat olympics.csv')


# In[30]:

df = pd.read_csv('olympics.csv')
df.head()


# In[31]:

df = pd.read_csv('olympics.csv', index_col = 0, skiprows=1)
df.head()


# In[32]:

df.columns


# In[32]:

for col in df.columns:
    if col[:2]=='01':
        df.rename(columns={col:'Gold' + col[4:]}, inplace=True)
    if col[:2]=='02':
        df.rename(columns={col:'Silver' + col[4:]}, inplace=True)
    if col[:2]=='03':
        df.rename(columns={col:'Bronze' + col[4:]}, inplace=True)
    if col[:1]=='№':
        df.rename(columns={col:'#' + col[1:]}, inplace=True) 
df.head()


# # Querying a DataFrame

# In[33]:

df['Gold'] > 0


# In[37]:

only_gold = df.where(df['Gold'] > 0)
only_gold.index


# In[37]:

only_gold['Gold'].count()


# In[38]:

df['Gold'].count()


# In[39]:

only_gold = only_gold.dropna()
only_gold.head()


# In[40]:

only_gold = df[df['Gold'] > 0]
only_gold.head()


# In[41]:

len(df[(df['Gold'] > 0) | (df['Gold.1'] > 0)])


# In[42]:

df[(df['Gold.1'] > 0) & (df['Gold'] == 0)]


# # Indexing Dataframes

# In[43]:

df.head()


# In[44]:

df['country'] = df.index
df = df.set_index('Gold')
df.head()


# In[45]:

df = df.reset_index()
df.head()


# In[14]:

df = pd.read_csv('census.csv')
df.head()


# In[15]:

df['SUMLEV'].unique()


# In[16]:

df=df[df['SUMLEV'] == 50]
df.head()


# In[17]:

columns_to_keep = ['STNAME',
                   'CTYNAME',
                   'BIRTHS2010',
                   'BIRTHS2011',
                   'BIRTHS2012',
                   'BIRTHS2013',
                   'BIRTHS2014',
                   'BIRTHS2015',
                   'POPESTIMATE2010',
                   'POPESTIMATE2011',
                   'POPESTIMATE2012',
                   'POPESTIMATE2013',
                   'POPESTIMATE2014',
                   'POPESTIMATE2015']
df = df[columns_to_keep]
df.head()


# In[21]:

df = df.set_index(['STNAME', 'CTYNAME'])
df


# In[11]:

df.loc['Michigan', 'Washtenaw County']


# In[ ]:

df.loc[ [('Michigan', 'Washtenaw County'),
         ('Michigan', 'Wayne County')] ]


# # Missing values

# In[2]:

import pandas as pd
df = pd.read_csv('log.csv')
df


# In[3]:

get_ipython().magic('pinfo df.fillna')


# In[22]:

df = df.set_index('time')
df = df.sort_index()
df


# In[9]:

df = df.reset_index()
df = df.set_index(['time', 'user'])
df


# In[8]:

df = df.fillna(method='ffill')
df.head()


# In[ ]:



