#!/usr/bin/env python
# coding: utf-8

# 911 Calls Capstone Project , using data from Morganstown county in 2015-2106 in Pennsylvania
#This was done in Jupyter notebook , so there are not many prints
#Import libraries

import numpy as np
import pandas as pd
import matplotlib as plt
import seaborn as sns
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('whitegrid')
get_ipython().run_line_magic('matplotlib', 'inline')


#Read in the csv file as a dataframe called df
df=pd.read_csv('911.csv')

df.head()
#Top 5 zipcode

top5_zip=df['zip'].value_counts().head(5)
print(top5_zip)

#Top 5 town 
top5_twp=df['twp'].value_counts().head(5)
print(top5_twp)


#Unique title codes

title_unique=df['title'].nunique()
print(title_unique)

#Create new column to store the three basic "Reason" To call the 911,
def get_reason(reason):
    code=reason.split(':')
    return code[0] 


df['Reason']=df['title'].apply(lambda x:get_reason(x))
print(df['Reason'])


#Reason count

reason_rank=df['Reason'].value_counts()
print(reason_rank)

#Count Plot for reasons (image=Reason CountPlot.png)
sns.countplot(x='Reason',data=df)

#Converting Timestamp 

df['timeStamp']

df['timeStamp']=pd.to_datetime(df['timeStamp'])



#Creating and adding new column for further analysis

#Add column with the Hour for further analysis
def get_hour(date):
    hour=date.hour
    return hour

df['Hour']=df['timeStamp'].apply(lambda x:get_hour(x))

#Add Column with the Month for further analysis
def get_month(date):
    month=date.month
    return month

df['Month']=df['timeStamp'].apply(lambda x:get_month(x))

#Add Column with the DOW for further analysis
dmap = {0:'Mon',1:'Tue',2:'Wed',3:'Thu',4:'Fri',5:'Sat',6:'Sun'}

def get_day(date):
    num_day=date.weekday()
    day=dmap[num_day]
    return day

df['Day of Week']=df['timeStamp'].apply(lambda x:get_day(x))

df.tail()


#Count Plot for all the calls during the day of the week(Day Of Week CountPlot.png)
g = sns.countplot(x='Day of Week',data=df,hue='Reason',palette='viridis')
g.legend(loc='center left', bbox_to_anchor=(1, 0.9), ncol=1)

#Count Plot for all the calls during the months(Month Countplot.png)
g = sns.countplot(x='Month',data=df,hue='Reason',palette='viridis')
g.legend(loc='center left', bbox_to_anchor=(1, 0.9), ncol=1)

#Groupping by Month for more analysis

byMonth=df.groupby('Month').count()
byMonth.head()

#Plott of how the call are ditributed over the 12 months,(Call by month.png)

byMonth['twp'].plot(marker='o')

#Linear fit and Regression model(Regression Curve.ong),reset index is needed to make it work

byMonth.reset_index(inplace=True)
sns.lmplot(x='Month',y='twp',data=byMonth,markers='o',size=7)


#Create new column for the Date

def get_date(date):
    return date.date()

df['Date']=df['timeStamp'].apply(lambda x:get_date(x))
df.head()

#Create a plot count of all the call over time (Group by call.png)

df.groupby('Date').count()['twp'].plot(figsize=(12,3))

#Create a plot count of all the call over time on the EMS section(Group by EMS.png)

df[df['Reason']=='EMS'].groupby('Date').count()['twp'].plot(figsize=(12,3))
plt.title('EMS')

#Create a plot count of all the call over time on the EMS section(Group by Fire.png)

df[df['Reason']=='Fire'].groupby('Date').count()['twp'].plot(figsize=(12,3))
plt.title('Fire')

#Create a plot count of all the call over time on the EMS section(Group by Traffic.png)

df[df['Reason']=='Traffic'].groupby('Date').count()['twp'].plot(figsize=(12,3))
plt.title('Traffic')

#Call per hour per day of the week table

day_hour = df.groupby(by=['Day of Week','Hour']).count()['Reason'].unstack()
day_hour.head()

#Heat map for the dayHour table(Day of Week-Month heatmap.png)

plt.figure(figsize=(12,5))
sns.heatmap(day_hour,cmap='viridis')

#Cluster map for the dayHour table(Day of the Week-Hour Cluster Map.png)

plt.figure(figsize=(12,5))
sns.clustermap(day_hour,cmap='viridis')

#Call per month per day of the week(HeatMap per week and month.png)

day_Month = df.groupby(by=['Day of Week','Month']).count()['Reason'].unstack()
day_Month.head()

#Heat map for the dayHour table(Day of Week-Month heatmap.png)

plt.figure(figsize=(12,5))
sns.heatmap(day_Month,cmap='viridis')

#Cluster map for the dayHour table(Day of Week-Month Cluster Map.png)

plt.figure(figsize=(12,5))
sns.clustermap(day_Month,cmap='viridis')

#Create a map for where the call came from(Heat map per year per town.png)
def get_year(date):
    year=date.year
    return year
df['Year']=df['timeStamp'].apply(lambda x:get_year(x))
twp_year = df.groupby(by=['twp','Year']).count()['Reason'].unstack()
plt.figure(figsize=(20,20))
sns.heatmap(twp_year,cmap='coolwarm',annot=True)

#print the top 5(stored before)

print(top5_twp)

#Create a graph that show the number for the top 5 town(Total per town.png)

twp_year['TOTAL']=twp_year[2015]+twp_year[2016]
twp_year.sort_values(by='TOTAL',axis=0,ascending=False, inplace=True)
twp_top5sort=twp_year.head(5)
twp_top5sort.reset_index(inplace=True)
plt.figure(figsize=(15,5))
sns.barplot(x='twp',y='TOTAL',data=twp_top5sort)


#More analysis possible to come




