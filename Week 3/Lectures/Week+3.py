
# coding: utf-8

# ---
# 
# _You are currently looking at **version 1.0** of this notebook. To download notebooks and datafiles, as well as get help on Jupyter notebooks in the Coursera platform, visit the [Jupyter Notebook FAQ](https://www.coursera.org/learn/python-data-analysis/resources/0dhYG) course resource._
# 
# ---

# # Merging Dataframes
# 

# In[1]:

import pandas as pd

df = pd.DataFrame([{'Name': 'Chris', 'Item Purchased': 'Sponge', 'Cost': 22.50},
                   {'Name': 'Kevyn', 'Item Purchased': 'Kitty Litter', 'Cost': 2.50},
                   {'Name': 'Filip', 'Item Purchased': 'Spoon', 'Cost': 5.00}],
                  index=['Store 1', 'Store 1', 'Store 2'])
df


# In[2]:

df['Date'] = ['December 1', 'January 1', 'mid-May']
df


# In[3]:

df['Delivered'] = True
df


# In[4]:

df['Feedback'] = ['Positive', None, 'Negative']
df


# In[5]:

adf = df.reset_index()
adf['Date'] = pd.Series({0: 'December 1', 2: 'mid-May'})
adf


# In[7]:

staff_df = pd.DataFrame([{'Name': 'Kelly', 'Role': 'Director of HR'},
                         {'Name': 'Sally', 'Role': 'Course liasion'},
                         {'Name': 'James', 'Role': 'Grader'}])
staff_df = staff_df.set_index('Name')
student_df = pd.DataFrame([{'Name': 'James', 'School': 'Business'},
                           {'Name': 'Mike', 'School': 'Law'},
                           {'Name': 'Sally', 'School': 'Engineering'}])
student_df = student_df.set_index('Name')
print(staff_df.head())
print()
print(student_df.head())


# In[8]:

pd.merge(staff_df, student_df, how='outer', left_index=True, right_index=True)


# In[9]:

pd.merge(staff_df, student_df, how='inner', left_index=True, right_index=True)


# In[10]:

pd.merge(staff_df, student_df, how='left', left_index=True, right_index=True)


# In[14]:

pd.merge(staff_df, student_df, how='right', left_index=True, right_index=True)


# In[15]:

staff_df = staff_df.reset_index()
student_df = student_df.reset_index()
pd.merge(staff_df, student_df, how='left', left_on='Name', right_on='Name')


# In[11]:

staff_df = pd.DataFrame([{'Name': 'Kelly', 'Role': 'Director of HR', 'Location': 'State Street'},
                         {'Name': 'Sally', 'Role': 'Course liasion', 'Location': 'Washington Avenue'},
                         {'Name': 'James', 'Role': 'Grader', 'Location': 'Washington Avenue'}])
student_df = pd.DataFrame([{'Name': 'James', 'School': 'Business', 'Location': '1024 Billiard Avenue'},
                           {'Name': 'Mike', 'School': 'Law', 'Location': 'Fraternity House #22'},
                           {'Name': 'Sally', 'School': 'Engineering', 'Location': '512 Wilson Crescent'}])
pd.merge(staff_df, student_df, how='left', left_on='Name', right_on='Name')


# In[12]:

staff_df = pd.DataFrame([{'First Name': 'Kelly', 'Last Name': 'Desjardins', 'Role': 'Director of HR'},
                         {'First Name': 'Sally', 'Last Name': 'Brooks', 'Role': 'Course liasion'},
                         {'First Name': 'James', 'Last Name': 'Wilde', 'Role': 'Grader'}])
student_df = pd.DataFrame([{'First Name': 'James', 'Last Name': 'Hammond', 'School': 'Business'},
                           {'First Name': 'Mike', 'Last Name': 'Smith', 'School': 'Law'},
                           {'First Name': 'Sally', 'Last Name': 'Brooks', 'School': 'Engineering'}])
staff_df
student_df
pd.merge(staff_df, student_df, how='inner', left_on=['First Name','Last Name'], right_on=['First Name','Last Name'])


# # Idiomatic Pandas: Making Code Pandorable

# In[13]:

import pandas as pd
df = pd.read_csv('census.csv')
df


# In[14]:

(df.where(df['SUMLEV']==50)
    .dropna()
    .set_index(['STNAME','CTYNAME'])
    .rename(columns={'ESTIMATESBASE2010': 'Estimates Base 2010'}))


# In[4]:

df = df[df['SUMLEV']==50]
df.set_index(['STNAME','CTYNAME'], inplace=True)
df.rename(columns={'ESTIMATESBASE2010': 'Estimates Base 2010'})


# In[15]:

import numpy as np
def min_max(row):
    data = row[['POPESTIMATE2010',
                'POPESTIMATE2011',
                'POPESTIMATE2012',
                'POPESTIMATE2013',
                'POPESTIMATE2014',
                'POPESTIMATE2015']]
    return pd.Series({'min': np.min(data)})


# In[16]:

df.apply(min_max,axis=1)


# In[17]:

import numpy as np
def min_max(row):
    data = row[['POPESTIMATE2010',
                'POPESTIMATE2011',
                'POPESTIMATE2012',
                'POPESTIMATE2013',
                'POPESTIMATE2014',
                'POPESTIMATE2015']]
    row['max'] = np.max(data)
    row['min'] = np.min(data)
    return row
df.apply(min_max, axis=1)


# In[18]:

rows = ['POPESTIMATE2010',
        'POPESTIMATE2011',
        'POPESTIMATE2012',
        'POPESTIMATE2013',
        'POPESTIMATE2014',
        'POPESTIMATE2015']
df.apply(lambda x: np.max(x[rows]), axis=1)


# # Group by

# In[19]:

import pandas as pd
import numpy as np
df = pd.read_csv('census.csv')
df = df[df['SUMLEV']==50]
df


# In[6]:

get_ipython().run_cell_magic('timeit', '-n 10', "for state in df['STNAME'].unique():\n    avg = np.average(df.where(df['STNAME']==state).dropna()['CENSUS2010POP'])\n    print('Counties in state ' + state + ' have an average population of ' + str(avg))")


# In[7]:

get_ipython().run_cell_magic('timeit', '-n 10', "for group, frame in df.groupby('STNAME'):\n    avg = np.average(frame['CENSUS2010POP'])\n    print('Counties in state ' + group + ' have an average population of ' + str(avg))")


# In[ ]:

df.head()


# In[20]:

df = df.set_index('STNAME')

def fun(item):
    if item[0]<'M':
        return 0
    if item[0]<'Q':
        return 1
    return 2

for group, frame in df.groupby(fun):
    print('There are ' + str(len(frame)) + ' records in group ' + str(group) + ' for processing.')


# In[28]:

df = pd.read_csv('census.csv')
df = df[df['SUMLEV']==50]


# In[29]:

df.groupby('STNAME').agg({'CENSUS2010POP': np.average})


# In[23]:

print(type(df.groupby(level=0)['POPESTIMATE2010','POPESTIMATE2011']))
df.groupby(level=0)['POPESTIMATE2010']


# In[38]:

print((df.set_index('STNAME').groupby(level=0)['CENSUS2010POP']
    .agg({'avg': np.average, 'sum': np.sum})))
df


# In[31]:

(df.set_index('STNAME').groupby(level=0)['POPESTIMATE2010','POPESTIMATE2011']
    .agg({'avg': np.average, 'sum': np.sum}))


# In[32]:

(df.set_index('STNAME').groupby(level=0)['POPESTIMATE2010','POPESTIMATE2011']
    .agg({'POPESTIMATE2010': np.average, 'POPESTIMATE2011': np.sum}))


# # Scales

# In[33]:

df = pd.DataFrame(['A+', 'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-', 'D+', 'D'],
                  index=['excellent', 'excellent', 'excellent', 'good', 'good', 'good', 'ok', 'ok', 'ok', 'poor', 'poor'])
df.rename(columns={0: 'Grades'}, inplace=True)
df


# In[34]:

df['Grades'].astype('category').head()


# In[36]:

grades = df['Grades'].astype('category',
                             categories=['D', 'D+', 'C-', 'C', 'C+', 'B-', 'B', 'B+', 'A-', 'A', 'A+'],
                             ordered=True)
grades


# In[37]:

grades > 'C'


# In[6]:

df = pd.read_csv('census.csv')
df = df[df['SUMLEV']==50]
df = df.set_index('STNAME').groupby(level=0)['CENSUS2010POP'].agg({'avg': np.average})
print(pd.cut(df['avg'],10))
df


# # Pivot Tables

# In[40]:

#http://open.canada.ca/data/en/dataset/98f1a129-f628-4ce4-b24d-6f16bf24dd64
df = pd.read_csv('cars.csv')


# In[41]:

df.head()


# In[18]:

df.pivot_table(values='(kW)', index='YEAR', columns='Make', aggfunc=np.mean)


# In[21]:

df.pivot_table(values='(kW)', index='YEAR', columns='Make', aggfunc=[np.mean,np.min], margins=True)


# # Date Functionality in Pandas

# In[22]:

import pandas as pd
import numpy as np


# ### Timestamp

# In[27]:

pd.Timestamp('9.1.2016 10:05AM')


# ### Period

# In[4]:

pd.Period('1/2016')


# In[5]:

pd.Period('3/5/2016')


# ### DatetimeIndex

# In[6]:

t1 = pd.Series(list('abc'), [pd.Timestamp('2016-09-01'), pd.Timestamp('2016-09-02'), pd.Timestamp('2016-09-03')])
t1


# In[7]:

type(t1.index)


# ### PeriodIndex

# In[8]:

t2 = pd.Series(list('def'), [pd.Period('2016-09'), pd.Period('2016-10'), pd.Period('2016-11')])
t2


# In[9]:

type(t2.index)


# ### Converting to Datetime

# In[10]:

d1 = ['2 June 2013', 'Aug 29, 2014', '2015-06-26', '7/12/16']
ts3 = pd.DataFrame(np.random.randint(10, 100, (4,2)), index=d1, columns=list('ab'))
ts3


# In[11]:

ts3.index = pd.to_datetime(ts3.index)
ts3


# In[30]:

pd.to_datetime('4.7.12', dayfirst=True)


# ### Timedeltas

# In[13]:

pd.Timestamp('9/3/2016')-pd.Timestamp('9/1/2016')


# In[31]:

pd.Timestamp('9/2/2016 8:10AM') + pd.Timedelta('12Days 3Hours')


# ### Working with Dates in a Dataframe

# In[32]:

dates = pd.date_range('10-01-2016', periods=9, freq='2W-MON')
dates


# In[35]:

df = pd.DataFrame({'Count 1': 100 + np.random.randint(-5, 10, 9).cumsum(),
                  'Count 2': 120 + np.random.randint(-5, 10, 9)}, index=dates)
df


# In[17]:

df.index.weekday_name


# In[18]:

df.diff()


# In[19]:

df.resample('M').mean()


# In[20]:

df['2017']


# In[21]:

df['2016-12']


# In[22]:

df['2016-12':]


# In[36]:

df.asfreq('W', method='ffill')


# In[38]:

import matplotlib.pyplot as plt
get_ipython().magic('matplotlib inline')

df.plot()


# In[ ]:



