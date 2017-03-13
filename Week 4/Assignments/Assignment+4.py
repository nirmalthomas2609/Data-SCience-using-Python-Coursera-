
# coding: utf-8

# ---
# 
# _You are currently looking at **version 1.1** of this notebook. To download notebooks and datafiles, as well as get help on Jupyter notebooks in the Coursera platform, visit the [Jupyter Notebook FAQ](https://www.coursera.org/learn/python-data-analysis/resources/0dhYG) course resource._
# 
# ---

# In[1]:

import pandas as pd
import numpy as np
from scipy.stats import ttest_ind


# # Assignment 4 - Hypothesis Testing
# This assignment requires more individual learning than previous assignments - you are encouraged to check out the [pandas documentation](http://pandas.pydata.org/pandas-docs/stable/) to find functions or methods you might not have used yet, or ask questions on [Stack Overflow](http://stackoverflow.com/) and tag them as pandas and python related. And of course, the discussion forums are open for interaction with your peers and the course staff.
# 
# Definitions:
# * A _quarter_ is a specific three month period, Q1 is January through March, Q2 is April through June, Q3 is July through September, Q4 is October through December.
# * A _recession_ is defined as starting with two consecutive quarters of GDP decline, and ending with two consecutive quarters of GDP growth.
# * A _recession bottom_ is the quarter within a recession which had the lowest GDP.
# * A _university town_ is a city which has a high percentage of university students compared to the total population of the city.
# 
# **Hypothesis**: University towns have their mean housing prices less effected by recessions. Run a t-test to compare the ratio of the mean price of houses in university towns the quarter before the recession starts compared to the recession bottom. (`price_ratio=quarter_before_recession/recession_bottom`)
# 
# The following data files are available for this assignment:
# * From the [Zillow research data site](http://www.zillow.com/research/data/) there is housing data for the United States. In particular the datafile for [all homes at a city level](http://files.zillowstatic.com/research/public/City/City_Zhvi_AllHomes.csv), ```City_Zhvi_AllHomes.csv```, has median home sale prices at a fine grained level.
# * From the Wikipedia page on college towns is a list of [university towns in the United States](https://en.wikipedia.org/wiki/List_of_college_towns#College_towns_in_the_United_States) which has been copy and pasted into the file ```university_towns.txt```.
# * From Bureau of Economic Analysis, US Department of Commerce, the [GDP over time](http://www.bea.gov/national/index.htm#gdp) of the United States in current dollars (use the chained value in 2009 dollars), in quarterly intervals, in the file ```gdplev.xls```. For this assignment, only look at GDP data from the first quarter of 2000 onward.
# 
# Each function in this assignment below is worth 10%, with the exception of ```run_ttest()```, which is worth 50%.

# In[2]:

# Use this dictionary to map state names to two letter acronyms
states = {'OH': 'Ohio', 'KY': 'Kentucky', 'AS': 'American Samoa', 'NV': 'Nevada', 'WY': 'Wyoming', 'NA': 'National', 'AL': 'Alabama', 'MD': 'Maryland', 'AK': 'Alaska', 'UT': 'Utah', 'OR': 'Oregon', 'MT': 'Montana', 'IL': 'Illinois', 'TN': 'Tennessee', 'DC': 'District of Columbia', 'VT': 'Vermont', 'ID': 'Idaho', 'AR': 'Arkansas', 'ME': 'Maine', 'WA': 'Washington', 'HI': 'Hawaii', 'WI': 'Wisconsin', 'MI': 'Michigan', 'IN': 'Indiana', 'NJ': 'New Jersey', 'AZ': 'Arizona', 'GU': 'Guam', 'MS': 'Mississippi', 'PR': 'Puerto Rico', 'NC': 'North Carolina', 'TX': 'Texas', 'SD': 'South Dakota', 'MP': 'Northern Mariana Islands', 'IA': 'Iowa', 'MO': 'Missouri', 'CT': 'Connecticut', 'WV': 'West Virginia', 'SC': 'South Carolina', 'LA': 'Louisiana', 'KS': 'Kansas', 'NY': 'New York', 'NE': 'Nebraska', 'OK': 'Oklahoma', 'FL': 'Florida', 'CA': 'California', 'CO': 'Colorado', 'PA': 'Pennsylvania', 'DE': 'Delaware', 'NM': 'New Mexico', 'RI': 'Rhode Island', 'MN': 'Minnesota', 'VI': 'Virgin Islands', 'NH': 'New Hampshire', 'MA': 'Massachusetts', 'GA': 'Georgia', 'ND': 'North Dakota', 'VA': 'Virginia'}


# In[3]:

def get_list_of_university_towns():
    '''Returns a DataFrame of towns and the states they are in from the 
    university_towns.txt list. The format of the DataFrame should be:
    DataFrame( [ ["Michigan", "Ann Arbor"], ["Michigan", "Yipsilanti"] ], 
    columns=["State", "RegionName"]  )
    
    The following cleaning needs to be done:

    1. For "State", removing characters from "[" to the end.
    2. For "RegionName", when applicable, removing every character from " (" to the end.
    3. Depending on how you read the data, you may need to remove newline character '\n'. '''
    with open("university_towns.txt","r") as myfile:
        test=myfile.readlines()
    k=[]
    for a in test:
        if a[-7:]=="[edit]\n":
            state=a[0:len(a)-7]
        elif '(' in a:
            a=a[0:a.index('(')-1]
            k=k+[(state,a)]
        else:
            a=a[0:len(a)-1]
            k=k+[(state,a)]
    k=pd.DataFrame(k,columns=["State","RegionName"])
    return k


# In[4]:

def get_recession_start():
    '''Returns the year and quarter of the recession start time as a 
    string value in a format such as 2005q3'''
    df=pd.read_excel("gdplev.xls",index_col=0,skiprows=7)
    df.rename(columns={"Unnamed: 1":"Annual GDP in current dollars"},inplace=True)
    df.rename(columns={"Unnamed: 2":"Annual GDP in chained 2009 dollars"},inplace=True)
    df.rename(columns={"Unnamed: 4":"Quarterly"},inplace=True)
    df.rename(columns={"Unnamed: 5":"Quarterly GDP in current dollars"},inplace=True)
    df.rename(columns={"Unnamed: 6":"Quarterly GDP in chained 2009 dollars"},inplace=True)
    del df["Unnamed: 3"]
    del df["Unnamed: 7"]
    annual=df[["Annual GDP in current dollars","Annual GDP in chained 2009 dollars"]]
    quarterly=df[["Quarterly","Quarterly GDP in current dollars","Quarterly GDP in chained 2009 dollars"]]
    quarterly=quarterly.reset_index()
    del quarterly["index"]
    p=quarterly[quarterly["Quarterly"]=="2000q1"].index.tolist()[0]
    quarterly=quarterly.drop(quarterly.index[:212])
    o=[i for i in range(66)]
    o=pd.Series(o)
    quarterly.index=o
    t=0
    i=0
    s=[]
    for i in range(len(quarterly)):
        if i==len(quarterly)-2:
            break
        elif t==0:
            if (quarterly.iloc[i]["Quarterly GDP in current dollars"]>quarterly.iloc[i+1]["Quarterly GDP in current dollars"]):
                if(quarterly.iloc[i+1]["Quarterly GDP in current dollars"]>quarterly.iloc[i+2]["Quarterly GDP in current dollars"]):
                    t=1
                    s=s+[quarterly.iloc[i]["Quarterly"]]
        elif t==1:
            if(quarterly.iloc[i]["Quarterly GDP in current dollars"]<quarterly.iloc[i+1]["Quarterly GDP in current dollars"]):
                if (quarterly.iloc[i+1]["Quarterly GDP in current dollars"]<quarterly.iloc[i+2]["Quarterly GDP in current dollars"]):
                    t=0
    return s[0]
get_recession_start()


# In[5]:

def get_recession_end():
    '''Returns the year and quarter of the recession end time as a 
    string value in a format such as 2005q3'''
    df=pd.read_excel("gdplev.xls",index_col=0,skiprows=7)
    df.rename(columns={"Unnamed: 1":"Annual GDP in current dollars"},inplace=True)
    df.rename(columns={"Unnamed: 2":"Annual GDP in chained 2009 dollars"},inplace=True)
    df.rename(columns={"Unnamed: 4":"Quarterly"},inplace=True)
    df.rename(columns={"Unnamed: 5":"Quarterly GDP in current dollars"},inplace=True)
    df.rename(columns={"Unnamed: 6":"Quarterly GDP in chained 2009 dollars"},inplace=True)
    del df["Unnamed: 3"]
    del df["Unnamed: 7"]
    annual=df[["Annual GDP in current dollars","Annual GDP in chained 2009 dollars"]]
    quarterly=df[["Quarterly","Quarterly GDP in current dollars","Quarterly GDP in chained 2009 dollars"]]
    quarterly=quarterly.reset_index()
    del quarterly["index"]
    p=quarterly[quarterly["Quarterly"]=="2000q1"].index.tolist()[0]
    quarterly=quarterly.drop(quarterly.index[:212])
    o=[i for i in range(66)]
    o=pd.Series(o)
    quarterly.index=o
    t=0
    i=0
    s=[]
    for i in range(len(quarterly)):
        if i==len(quarterly)-2:
            break
        elif t==0:
            if (quarterly.iloc[i]["Quarterly GDP in current dollars"]>quarterly.iloc[i+1]["Quarterly GDP in current dollars"]):
                if(quarterly.iloc[i+1]["Quarterly GDP in current dollars"]>quarterly.iloc[i+2]["Quarterly GDP in current dollars"]):
                    t=1
        elif t==1:
            if(quarterly.iloc[i]["Quarterly GDP in current dollars"]<quarterly.iloc[i+1]["Quarterly GDP in current dollars"]):
                if (quarterly.iloc[i+1]["Quarterly GDP in current dollars"]<quarterly.iloc[i+2]["Quarterly GDP in current dollars"]):
                    t=0
                    s=s+[quarterly.iloc[i+2]["Quarterly"]]
    return s[0]
get_recession_end()


# In[6]:

def get_recession_bottom():
    '''Returns the year and quarter of the recession bottom time as a 
    string value in a format such as 2005q3'''
    df=pd.read_excel("gdplev.xls",index_col=0,skiprows=7)
    df.rename(columns={"Unnamed: 1":"Annual GDP in current dollars"},inplace=True)
    df.rename(columns={"Unnamed: 2":"Annual GDP in chained 2009 dollars"},inplace=True)
    df.rename(columns={"Unnamed: 4":"Quarterly"},inplace=True)
    df.rename(columns={"Unnamed: 5":"Quarterly GDP in current dollars"},inplace=True)
    df.rename(columns={"Unnamed: 6":"Quarterly GDP in chained 2009 dollars"},inplace=True)
    del df["Unnamed: 3"]
    del df["Unnamed: 7"]
    annual=df[["Annual GDP in current dollars","Annual GDP in chained 2009 dollars"]]
    quarterly=df[["Quarterly","Quarterly GDP in current dollars","Quarterly GDP in chained 2009 dollars"]]
    quarterly=quarterly.reset_index()
    del quarterly["index"]
    p=quarterly[quarterly["Quarterly"]=="2000q1"].index.tolist()[0]
    quarterly=quarterly.drop(quarterly.index[:212])
    o=[i for i in range(66)]
    o=pd.Series(o)
    quarterly.index=o
    i=quarterly[quarterly["Quarterly"]==get_recession_start()].index.tolist()[0]
    j=quarterly[quarterly["Quarterly"]==get_recession_end()].index.tolist()[0]
    minyear=quarterly.iloc[i]["Quarterly"]
    mingdp=quarterly.iloc[i]["Quarterly GDP in current dollars"]
    j=j-2
    i=i+1
    while i<=j:
        if(quarterly.iloc[i]["Quarterly GDP in current dollars"]<mingdp):
            minyear=quarterly.iloc[i]["Quarterly"]
            mingdp=quarterly.iloc[i]["Quarterly GDP in current dollars"]
        i+=1
    return minyear
get_recession_bottom()


# In[7]:

def convert_housing_data_to_quarters():
    states = {'OH': 'Ohio', 'KY': 'Kentucky', 'AS': 'American Samoa', 'NV': 'Nevada', 'WY': 'Wyoming', 'NA': 'National', 'AL': 'Alabama', 'MD': 'Maryland', 'AK': 'Alaska', 'UT': 'Utah', 'OR': 'Oregon', 'MT': 'Montana', 'IL': 'Illinois', 'TN': 'Tennessee', 'DC': 'District of Columbia', 'VT': 'Vermont', 'ID': 'Idaho', 'AR': 'Arkansas', 'ME': 'Maine', 'WA': 'Washington', 'HI': 'Hawaii', 'WI': 'Wisconsin', 'MI': 'Michigan', 'IN': 'Indiana', 'NJ': 'New Jersey', 'AZ': 'Arizona', 'GU': 'Guam', 'MS': 'Mississippi', 'PR': 'Puerto Rico', 'NC': 'North Carolina', 'TX': 'Texas', 'SD': 'South Dakota', 'MP': 'Northern Mariana Islands', 'IA': 'Iowa', 'MO': 'Missouri', 'CT': 'Connecticut', 'WV': 'West Virginia', 'SC': 'South Carolina', 'LA': 'Louisiana', 'KS': 'Kansas', 'NY': 'New York', 'NE': 'Nebraska', 'OK': 'Oklahoma', 'FL': 'Florida', 'CA': 'California', 'CO': 'Colorado', 'PA': 'Pennsylvania', 'DE': 'Delaware', 'NM': 'New Mexico', 'RI': 'Rhode Island', 'MN': 'Minnesota', 'VI': 'Virgin Islands', 'NH': 'New Hampshire', 'MA': 'Massachusetts', 'GA': 'Georgia', 'ND': 'North Dakota', 'VA': 'Virginia'}
    '''Converts the housing data to quarters and returns it as mean 
    values in a dataframe. This dataframe should be a dataframe with
    columns for 2000q1 through 2016q3, and should have a multi-index
    in the shape of ["State","RegionName"].
    
    Note: Quarters are defined in the assignment description, they are
    not arbitrary three month periods.
    
    The resulting dataframe should have 67 columns, and 10,730 rows.
    '''
    df=pd.read_csv("City_Zhvi_AllHomes.csv")
    for i in range(16):
        if i<10:
            df["200%dq1"%i]=df[["200%d-01"%i,"200%d-02"%i,"200%d-03"%i]].mean(axis=1)
            df["200%dq2"%i]=df[["200%d-04"%i,"200%d-05"%i,"200%d-06"%i]].mean(axis=1)
            df["200%dq3"%i]=df[["200%d-07"%i,"200%d-08"%i,"200%d-09"%i]].mean(axis=1)
            df["200%dq4"%i]=df[["200%d-10"%i,"200%d-11"%i,"200%d-12"%i]].mean(axis=1)
        else:
            df["20%dq1"%i]=df[["20%d-01"%i,"20%d-02"%i,"20%d-03"%i]].mean(axis=1)
            df["20%dq2"%i]=df[["20%d-04"%i,"20%d-05"%i,"20%d-06"%i]].mean(axis=1)
            df["20%dq3"%i]=df[["20%d-07"%i,"20%d-08"%i,"20%d-09"%i]].mean(axis=1)
            df["20%dq4"%i]=df[["20%d-10"%i,"20%d-11"%i,"20%d-12"%i]].mean(axis=1)
    df["2016q1"]=df[["2016-01","2016-02","2016-03"]].mean(axis=1)
    df["2016q2"]=df[["2016-04","2016-05","2016-06"]].mean(axis=1)
    df["2016q3"]=df[["2016-07","2016-08"]].mean(axis=1)
    col=["200%dq%d"%(i,j) for i in range(10) for j in range(1,5)]+["20%dq%d"%(i,j)for i in range(10,16) for j in range(1,5)]+["2016q%d"%i for i in range(1,4)]
    states=pd.Series(states)
    df=df.set_index("State")
    df["States"]=states.loc[df.index]
    df=df.reset_index()
    del df["State"]
    df=df.rename(columns={"States":"State"})
    df.set_index(["State","RegionName"],inplace=True)
    df=df[col]
    return df
convert_housing_data_to_quarters()


# In[37]:

def checkuni(row):
    if(row["RegionName"] in k["RegionName"].tolist()):
        row["uni"]=1
    else:
        row["uni"]=0
    return row
def run_ttest():
    states = {'OH': 'Ohio', 'KY': 'Kentucky', 'AS': 'American Samoa', 'NV': 'Nevada', 'WY': 'Wyoming', 'NA': 'National', 'AL': 'Alabama', 'MD': 'Maryland', 'AK': 'Alaska', 'UT': 'Utah', 'OR': 'Oregon', 'MT': 'Montana', 'IL': 'Illinois', 'TN': 'Tennessee', 'DC': 'District of Columbia', 'VT': 'Vermont', 'ID': 'Idaho', 'AR': 'Arkansas', 'ME': 'Maine', 'WA': 'Washington', 'HI': 'Hawaii', 'WI': 'Wisconsin', 'MI': 'Michigan', 'IN': 'Indiana', 'NJ': 'New Jersey', 'AZ': 'Arizona', 'GU': 'Guam', 'MS': 'Mississippi', 'PR': 'Puerto Rico', 'NC': 'North Carolina', 'TX': 'Texas', 'SD': 'South Dakota', 'MP': 'Northern Mariana Islands', 'IA': 'Iowa', 'MO': 'Missouri', 'CT': 'Connecticut', 'WV': 'West Virginia', 'SC': 'South Carolina', 'LA': 'Louisiana', 'KS': 'Kansas', 'NY': 'New York', 'NE': 'Nebraska', 'OK': 'Oklahoma', 'FL': 'Florida', 'CA': 'California', 'CO': 'Colorado', 'PA': 'Pennsylvania', 'DE': 'Delaware', 'NM': 'New Mexico', 'RI': 'Rhode Island', 'MN': 'Minnesota', 'VI': 'Virgin Islands', 'NH': 'New Hampshire', 'MA': 'Massachusetts', 'GA': 'Georgia', 'ND': 'North Dakota', 'VA': 'Virginia'}
    '''First creates new data showing the decline or growth of housing prices
    between the recession start and the recession bottom. Then runs a ttest
    comparing the university town values to the non-university towns values, 
    return whether the alternative hypothesis (that the two groups are the same)
    is true or not as well as the p-value of the confidence. 
    
    Return the tuple (different, p, better) where different=True if the t-test is
    True at a p<0.01 (we reject the null hypothesis), or different=False if 
    otherwise (we cannot reject the null hypothesis). The variable p should
    be equal to the exact p value returned from scipy.stats.ttest_ind(). The
    value for better should be either "university town" or "non-university town"
    depending on which has a lower mean price ratio (which is equivilent to a
    reduced market loss).'''
    df=pd.read_excel("gdplev.xls",index_col=0,skiprows=7)
    df.rename(columns={"Unnamed: 1":"Annual GDP in current dollars"},inplace=True)
    df.rename(columns={"Unnamed: 2":"Annual GDP in chained 2009 dollars"},inplace=True)
    df.rename(columns={"Unnamed: 4":"Quarterly"},inplace=True)
    df.rename(columns={"Unnamed: 5":"Quarterly GDP in current dollars"},inplace=True)
    df.rename(columns={"Unnamed: 6":"Quarterly GDP in chained 2009 dollars"},inplace=True)
    del df["Unnamed: 3"]
    del df["Unnamed: 7"]
    annual=df[["Annual GDP in current dollars","Annual GDP in chained 2009 dollars"]]
    quarterly=df[["Quarterly","Quarterly GDP in current dollars","Quarterly GDP in chained 2009 dollars"]]
    quarterly=quarterly.reset_index()
    del quarterly["index"]
    p=quarterly[quarterly["Quarterly"]=="2000q1"].index.tolist()[0]
    quarterly=quarterly.drop(quarterly.index[:212])
    o=[i for i in range(66)]
    o=pd.Series(o)
    quarterly.index=o
    a=get_recession_start()
    p=quarterly[quarterly["Quarterly"]==a].index.tolist()[0]-1
    xx=quarterly.iloc[p]["Quarterly"]
    yy=get_recession_bottom()
    df=pd.read_csv("City_Zhvi_AllHomes.csv")
#    df=df.fillna(0)
    for i in range(16):
        if i<10:
            df["200%dq1"%i]=df[["200%d-01"%i,"200%d-02"%i,"200%d-03"%i]].mean(axis=1)
            df["200%dq2"%i]=df[["200%d-04"%i,"200%d-05"%i,"200%d-06"%i]].mean(axis=1)
            df["200%dq3"%i]=df[["200%d-07"%i,"200%d-08"%i,"200%d-09"%i]].mean(axis=1)
            df["200%dq4"%i]=df[["200%d-10"%i,"200%d-11"%i,"200%d-12"%i]].mean(axis=1)
        else:
            df["20%dq1"%i]=df[["20%d-01"%i,"20%d-02"%i,"20%d-03"%i]].mean(axis=1)
            df["20%dq2"%i]=df[["20%d-04"%i,"20%d-05"%i,"20%d-06"%i]].mean(axis=1)
            df["20%dq3"%i]=df[["20%d-07"%i,"20%d-08"%i,"20%d-09"%i]].mean(axis=1)
            df["20%dq4"%i]=df[["20%d-10"%i,"20%d-11"%i,"20%d-12"%i]].mean(axis=1)
    df["2016q1"]=df[["2016-01","2016-02","2016-03"]].mean(axis=1)
    df["2016q2"]=df[["2016-04","2016-05","2016-06"]].mean(axis=1)
    df["2016q3"]=df[["2016-07","2016-08"]].mean(axis=1)
    col=["200%dq%d"%(i,j) for i in range(10) for j in range(1,5)]+["20%dq%d"%(i,j)for i in range(10,16) for j in range(1,5)]+["2016q%d"%i for i in range(1,4)]
    states=pd.Series(states)
    df=df.set_index("State")
    df["States"]=states.loc[df.index]
    df=df.reset_index()
    del df["State"]
    df=df.rename(columns={"States":"State"})
    df.set_index(["State","RegionName"],inplace=True)
    df=df[col]
    housing=df
    housing=housing.reset_index()
    housing["pratio"]=housing[xx]/housing[yy]
    housing=housing.apply(checkuni,axis=1)
#    housing=housing.fillna(0)
    stats,pval=ttest_ind(housing[housing["uni"]==1].dropna()["pratio"],housing[housing["uni"]==0].dropna()["pratio"])
    if(pval<0.01):
        diff=True
    else:
        diff=False
    unimean=np.mean(housing[housing["uni"]==1]["pratio"])
    nonunimean=np.mean(housing[housing["uni"]==0]["pratio"])
    if(unimean<=nonunimean):
        better="university town"
    else:
        better="non-university town"
    return (diff,pval,better)
with open("university_towns.txt","r") as myfile:
    test=myfile.readlines()
k=[]
for a in test:
    if a[-7:]=="[edit]\n":
        state=a[0:len(a)-7]
    elif '(' in a:
        a=a[0:a.index('(')-1]
        k=k+[(state,a)]
    else:
        a=a[0:len(a)-1]
        k=k+[(state,a)]
k=pd.DataFrame(k,columns=["State","RegionName"])
run_ttest()


# In[ ]:




# In[ ]:



