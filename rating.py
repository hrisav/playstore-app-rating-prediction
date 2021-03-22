import pandas as pd
import numpy as np
import pickle
import re
from datetime import datetime, date
from sklearn.preprocessing import LabelEncoder 
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor

df = pd.read_csv('googleplaystore.csv')
df.loc[10472]=['Life Made WI-Fi Touchscreen Photo Frame','LIFESTYLE',1.9,'19','3.0M','1,000+','Free','0','Everyone','Lifestyle','February 11, 2018','1.0.19','4.0 and up']
df = df[df['Rating'].notna()]

df['Current_Ver_Upd'] = df['Current Ver']
df['Current_Ver_Upd'] = df['Current_Ver_Upd'].replace(np.nan,'Varies with device')
df['Current_Ver_Upd'] = df['Current_Ver_Upd'].apply(lambda x: 'Varies with device' if x=='Varies with device'  else  re.findall('^[0-9]\.[0-9]|[\d]|\W*',str(x))[0]) 
df['Current_Ver_Upd'] = df['Current_Ver_Upd'].replace('','Varies with device')
df['Current_Ver_Upd'] = df['Current_Ver_Upd'].replace('Varies with device','1.0')
df['Current_Ver_Upd'] = pd.to_numeric(df['Current_Ver_Upd'])

df['Android_Ver_Upd'] = df['Android Ver']
df['Android_Ver_Upd'] = df['Android_Ver_Upd'].replace(np.nan,'Varies with device')
df['Android_Ver_Upd'] = df['Android_Ver_Upd'].apply(lambda x: 'Varies with device' if x=='Varies with device'  else  re.findall('^[0-9]',str(x))[0]) 
df['Android_Ver_Upd'] = df['Android_Ver_Upd'].replace('Varies with device','4')
df['Android_Ver_Upd'] = pd.to_numeric(df['Android_Ver_Upd'])

df['Installs'] = df['Installs'].apply(lambda x: x.replace(',',''))
df['Installs'] = df['Installs'].apply(lambda x: x.strip('+'))
df['Installs'] = pd.to_numeric(df['Installs'])

df['Price'] = df['Price'].apply(lambda x: x.strip('$'))
df['Price'] = pd.to_numeric(df['Price'])

df['Size_Upd'] = df['Size'].apply(lambda a: str(a).replace('M', ''))
df['Size_Upd'] = df['Size_Upd'].apply(lambda a: float(str(a).replace('k', ''))/1000 if 'k' in str(a) else a)
df['Size_Upd'] = df['Size_Upd'].apply(lambda a: str(a).replace('Varies with device', '14'))
df['Size_Upd'] = pd.to_numeric(df['Size_Upd'])

temp = pd.to_datetime(df['Last Updated'])
df['Last_Updated_Days'] = temp.apply(lambda x:date.today()-datetime.date(x))
df['Last_Updated_Days'] = df['Last_Updated_Days'].dt.days
df['Last_Updated_Days'] = pd.to_numeric(df['Last_Updated_Days'])

df['Content_Rating'] = df['Content Rating']
df.loc[df['Content_Rating']=='Unrated', 'Content_Rating'] = 'Everyone'
df.loc[df['Content_Rating']=='Adults only 18+', 'Content_Rating'] = 'Mature 17+'

df['Reviews'] = pd.to_numeric(df['Reviews'])
df = df.drop(['Size', 'Last Updated', 'Current Ver', 'Android Ver', 'Content Rating'], axis = 1)
df = df.drop(['App', 'Genres'], axis = 1)

content_rating_dict = {'Everyone':1, 'Everyone 10+':2, 'Teen':3, 'Mature 17+':4}
df['Content_Rating'] = df['Content_Rating'].map(content_rating_dict)

le = LabelEncoder()
df['Category']= le.fit_transform(df['Category'])

dummies = pd.get_dummies(df['Type'],drop_first=True)
df = pd.concat([df,dummies],axis=1)
df = df.drop(['Type'],axis=1)

#Model Building

X = df.drop(['Rating'], axis=1)
y = df['Rating']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=20)

reg_rf = RandomForestRegressor()

reg_rf.fit(X_train, y_train)

file = open('playstore_rating.pkl', 'wb')
pickle.dump(reg_rf, file)