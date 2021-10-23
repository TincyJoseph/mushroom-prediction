# -*- coding: utf-8 -*-
"""
Created on Fri Jan  8 02:57:29 2021

@author: User
"""

import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
data=pd.read_csv("mushrooms.csv")
y = data['class']
x = data.drop(['class','stalk-root'],axis=1)
from sklearn import preprocessing
label=preprocessing.LabelEncoder()
#x=pd.get_dummies(x)
for i in  x.columns:
    x[i]=label.fit_transform(x[i])
    print(x[i].unique())
x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.3,random_state=42)
from sklearn.linear_model import LogisticRegression
regressor=LogisticRegression()
regressor.fit(x_train,y_train)
pickle.dump(regressor,open('model.pkl','wb'))