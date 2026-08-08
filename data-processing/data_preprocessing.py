import pandas as pd 
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

df=pd.read_csv("processed_data.csv")

Y=df["outcome"] # target values 
X=df.drop(columns=["outcome","sr_no","r1-ts-1","r1-ss-1","r2-ts-1","r2-ss-1","r3-ts-1","r3-ss-1","r4-ts-1","r4-ss-1","r5-ts-1","r5-ss-1","r1-td-1","r2-td-1","r3-td-1","r4-td-1","r5-td-1","r1-kd-1","r2-kd-1","r3-kd-1","r4-kd-1","r5-kd-1","r1-ts-2","r1-ss-2","r2-ts-2","r2-ss-2","r3-ts-2","r3-ss-2","r4-ts-2","r4-ss-2","r5-ts-2","r5-ss-2","r1-td-2","r2-td-2","r3-td-2","r4-td-2","r5-td-2","r1-kd-2","r2-kd-2","r3-kd-2","r4-kd-2","r5-kd-2"])

dfna=df.isna().sum()
#print(dfna[dfna>0])
#print(X.describe())
#print(Y.describe())

pipe=Pipeline(steps=[('scaler',StandardScaler()),('model',LinearRegression())])

X_train,X_test,Y_train,Y_test=train_test_split(X,Y,random_state=42,test_size=0.2)
pipe.fit(X_train,Y_train)
pipe.predict(X_test)