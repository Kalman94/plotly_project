# -*- coding: utf-8 -*-
"""
Created on Sun Apr  1 00:49:21 2018

@author: teo
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Mar  8 10:32:18 2018

@author: teo
"""

import pandas as pd


from plotly import tools
import numpy as np
import matplotlib.pyplot as plt

import plotly.plotly as py
import plotly.graph_objs as go
import cufflinks as cf
cf.go_offline()

from plotly.graph_objs import *
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
#init_notebook_mode(connected=True) 

data=pd.read_csv("C:\\Users\\teo\Downloads\\HR_comma_sep.csv",header=0)

# ------------------------------ Pre-Processing---------------------------------------------


data_viz=pd.DataFrame(data)
# Check for null columns
data_list=[data]
for dataset in data_list:
 print("+++++++++++++++++++++++++++")
 print(pd.isnull(dataset).sum() >0)
 print("+++++++++++++++++++++++++++")

#We dont have missing values 


xx=["other","sales","accounting","hr","technical","support","product_mng","marketing"]
for dataset in data_list[:]:

#Mapping departments
 dep_mapping={"sales":1,"accounting":2,"hr":3,"technical":4,"support":5,"product_mng":6,"marketing":7}
 dataset['sales']=dataset['sales'].map(dep_mapping)
 dataset['sales']=dataset['sales'].fillna(0)# for other deparments RandD,IT
#Mapping salary
 salary_mapping={'low':1,'medium':2,'high':3}
 dataset['salary']=dataset['salary'].map(salary_mapping)
 
#Mapping monthly average hours
 dataset.loc[dataset['average_montly_hours']<=100,'average_montly_hours']                              =0
 dataset.loc[(dataset['average_montly_hours']>100) & (dataset['average_montly_hours'] <=150),'average_montly_hours']=1
 dataset.loc[(dataset['average_montly_hours']>150) & (dataset['average_montly_hours'] <=250),'average_montly_hours']=2
 dataset.loc[(dataset['average_montly_hours']>250) & (dataset['average_montly_hours']<=300),'average_montly_hours']   =3
 dataset.loc[dataset['average_montly_hours']>300,'average_montly_hours']                                 =4

#Mapping time spend company
 dataset.loc[dataset['time_spend_company']<=3,'time_spend_company']                         =3
 dataset.loc[(dataset['time_spend_company']>3) & (dataset['time_spend_company'] <=6),'time_spend_company']=6
 dataset.loc[dataset['time_spend_company']>6 ,'time_spend_company']                        =9

#Mapping last evaluation
 dataset.loc[dataset['last_evaluation']<=0.25,'last_evaluation']                         =0
 dataset.loc[(dataset['last_evaluation']>0.25) & (dataset['last_evaluation']<=0.5),'last_evaluation'] =1
 dataset.loc[(dataset['last_evaluation']>0.5) & (dataset['last_evaluation'] <=0.75),'last_evaluation']=2
 dataset.loc[dataset['last_evaluation']>0.75  ,'last_evaluation']                        =3

#Mapping satisfaction level
 dataset.loc[dataset['satisfaction_level']<=0.25,'satisfaction_level']                         =0
 dataset.loc[(dataset['satisfaction_level']>0.25) & (dataset['satisfaction_level'] <=0.5),'satisfaction_level']=1
 dataset.loc[(dataset['satisfaction_level']>0.5) & (dataset['satisfaction_level']<=0.75),'satisfaction_level'] =2
 dataset.loc[dataset['satisfaction_level']>0.75  ,'satisfaction_level']                        =3


#convert list to dataframe

features = dataset.dtypes.index


dataDF = pd.DataFrame() #creates a new dataframe that's empty
dataDF = dataDF.append(data_list, ignore_index = False)
features = list(dataDF.columns[:10])
features.pop(6)
from sklearn import preprocessing
y = dataDF["left"]
X = dataDF[features]
X=preprocessing.scale(X)
X=pd.DataFrame(X)


init_notebook_mode(connected=True)
#cf.set_config_file(offline=False, world_readable=True, theme='ggplot')
df_plot_helper_salary=data_viz.groupby("salary")["left"].sum()
df_plot_helper_department=data_viz.groupby("sales")["left"].sum()
df_plot_helper_left=data_viz.groupby("left")["left"].sum()



salary_size=data_viz.groupby("salary").size()
sales_size=data_viz.groupby("sales").size()
df_plot_helper_department2=sales_size-df_plot_helper_department
df_plot_helper_salary2=salary_size-df_plot_helper_salary
#rename the sales column
data['sales']=data.rename(columns={'sales':'department'},inplace=True)
data=data.drop(['sales'],1)
        
#visualziation of the dependent variable left


a=data_viz.query('left == "0"')
#df_plot_helper_department2=a.groupby("sales")["sales"].sum().apply(lambda x: '%.3f' % x)

import plotly
plotly.offline.init_notebook_mode()


###############Department Barchart##############


x1=[0,1,2,3,4,5,6,7,]

y1=pd.DataFrame({'email':df_plot_helper_salary.index, 'list':df_plot_helper_salary.values})
y2=pd.DataFrame({'email':df_plot_helper_salary2.index, 'list':df_plot_helper_salary2.values})
y11=pd.DataFrame({'email':df_plot_helper_department.index, 'list':df_plot_helper_department.values})
y22=pd.DataFrame({'email':df_plot_helper_department2.index, 'list':df_plot_helper_department2.values})
trace1 = go.Bar(
    x=xx,
    y=y11['list'],
    name='Left'
)

trace2 = go.Bar(
    x=xx,
    y=y22['list'],
    name='Stay'
)

data = [trace1, trace2]
layout = go.Layout(
    barmode='group', width=500,
    height=500
)

fig = go.Figure(data=data, layout=layout)
aplot=plotly.offline.plot(fig, config={"displayModeBar": False}, 
                            show_link=False, 
                            include_plotlyjs=False, 
                            output_type='div')
# Salary Barchart
x1=[1,2,3]
x11=["low","medium","high"]

trace1 = go.Bar(
    x=x11,
    y=y1['list'],
    name='Left'
)

trace2 = go.Bar(
    x=x11,
    y=y2['list'],
    name='Stay'
)
#
data = [trace1, trace2]
layout = go.Layout(
    barmode='group'
)

fig = go.Figure(data=data, layout=layout)
bplot=plotly.offline.plot(fig, config={"displayModeBar": False}, 
                            show_link=False, 
                            include_plotlyjs=False, 
                            output_type='div')
#============================Pie chart ==============================
accidents=data_viz.groupby("Work_accident")["Work_accident"].count()



labels = ['Had Accident','Didnt have accident']
values = [accidents[0],accidents[1]]

trace = go.Pie(labels=labels, values=values)

cplot=plotly.offline.plot([trace], config={"displayModeBar": False}, 
                            show_link=False, 
                            include_plotlyjs=False, 
                            output_type='div')


#============================    BOX PLOTS=====================================

#split df
data_0 = data_viz[data_viz['left'] == 0]
satisfaction_0=data_0['satisfaction_level'].values.tolist()
time_0=data_0['time_spend_company'].values.tolist()
nproject_0=data_0['number_project'].values.tolist()
hours_0=data_0['average_montly_hours'].values.tolist()
lasteval_0=data_0['last_evaluation'].values.tolist()
accident_0=data_0['Work_accident'].values.tolist()
promotion_0=data_0['promotion_last_5years'].values.tolist()
sales_0=data_0['sales'].values.tolist()
salary_0=data_0['salary'].values.tolist()
data_1 = data_viz[data_viz['left'] == 1]
satisfaction_1=data_1['satisfaction_level'].values.tolist()
time_1=data_1['time_spend_company'].values.tolist()
nproject_1=data_1['number_project'].values.tolist()
hours_1=data_1['average_montly_hours'].values.tolist()
lasteval_1=data_1['last_evaluation'].values.tolist()
accident_1=data_1['Work_accident'].values.tolist()
promotion_1=data_1['promotion_last_5years'].values.tolist()
sales_1=data_1['sales'].values.tolist()
salary_1=data_1['salary'].values.tolist()

#df1, df2 = [x for _, x in dataDF.groupby(dataDF['Left'] < 1)]
x00=[]
x11=[]
x22=[]
x33=[]
x44=[]
x55=[]
x66=[]
x77=[]
x88=[]

for i in range(1,len(satisfaction_0)):
     x00.append('NO LEFT')
for i in range(1,len(satisfaction_1)):
     x00.append('LEFT')
for i in range(1,len(lasteval_0)):
     x11.append('NO LEFT')
for i in range(1,len(lasteval_1)):
     x11.append('LEFT')
for i in range(1,len(nproject_0)):
     x22.append('NO LEFT')
for i in range(1,len(nproject_1)):
     x22.append('LEFT')
for i in range(1,len(hours_0)):
     x33.append('NO LEFT')
for i in range(1,len(hours_1)):
     x33.append('LEFT')
for i in range(1,len(time_0)):
     x44.append('NO LEFT')
for i in range(1,len(time_1)):
     x44.append('LEFT')
for i in range(1,len(accident_0)):
     x55.append('NO LEFT')
for i in range(1,len(accident_1)):
     x55.append('LEFT')
for i in range(1,len(promotion_0)):
     x66.append('NO LEFT')
for i in range(1,len(promotion_1)):
     x66.append('LEFT')
for i in range(1,len(sales_0)):
     x77.append('NO LEFT')
for i in range(1,len(sales_1)):
     x77.append('LEFT')
for i in range(1,len(salary_0)):
     x88.append('NO LEFT')
for i in range(1,len(salary_1)):
     x88.append('LEFT')

trace00 = go.Box(
    y=satisfaction_0+satisfaction_1,
    x=x00,
    name='satisfaction',
    marker=dict(
        color='#3D9970'
    )
)
trace11 = go.Box(
    y=lasteval_0+lasteval_1,
    x=x11,
    name='last evaluation',
    marker=dict(
        color='#FF4136'
    )
)
trace22 = go.Box(
    y=nproject_0+nproject_1,
    x=x22,
    name='number_projects',
    marker=dict(
        color='#FF951B'
    )
)
trace33 = go.Box(
    y=hours_0+hours_1,
    x=x33,
    name='average_monthlyhours',
    marker=dict(
          color='#FE2EF7'
    )
)
trace44 = go.Box(
    y=time_0+time_1,
    x=x44,
    name='time_spendcompany',
    marker=dict(
      color='#8A4B08'
    )
    )
trace55 = go.Box(
    y=accident_0+accident_1,
    x=x55,
    name='work_accident',
    marker=dict(
      color='#9598fb'
    )
    )
trace66= go.Box(
    y=promotion_0+promotion_1,
    x=x66,
    name='promotion',
    marker=dict(
      color='#d0d636'
    ))
trace77 = go.Box(
    y=sales_0+sales_1,
    x=x77,
    name='sales',
    marker=dict(
      color='#e3c455'
    ))
trace88 = go.Box(
    y=salary_0+salary_1,
    x=x88,
    name='salary',
    marker=dict(
      color='#7f4555'
    )
)
data = [trace00, trace11, trace22,trace33,trace44,trace55,trace66,trace77,trace88]
layout = go.Layout(
    yaxis=dict(
        title='Distributions of parameters',
        zeroline=False
    ),
    boxmode='group'
)
fig = go.Figure(data=data, layout=layout)
dplot=plotly.offline.plot(fig ,config={"displayModeBar": False}, 
                            show_link=False, 
                            include_plotlyjs=False, 
                            output_type='div')


html_string = '''
<html>
    <head>
      <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
      <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.1/css/bootstrap.min.css">
      <style>body{ margin:0 100; background:whitesmoke; }</style>
    </head>
    <body>
      <h1>Departments barplot</h1>
      ''' + aplot + '''
          <h1>Salaries barplot</h1>
      ''' +bplot + '''
          <h1>Piechart of people who had accident</h1>
      ''' + cplot + '''
               <h1>Boxplots of all variables</h1>
      ''' + dplot + '''
    </body>
</html>'''

with open("pythonplots.html", 'w') as f:
    f.write(html_string)
