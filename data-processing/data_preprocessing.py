import pandas as pd 
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import quantile_transform
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_score, accuracy_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.neural_network import MLPClassifier

df=pd.read_csv("processed_data.csv")

Y=df["outcome"] # target values 
#X=df.drop(columns=["outcome","sr_no","r1-ts-1","r1-ss-1","r2-ts-1","r2-ss-1","r3-ts-1","r3-ss-1","r4-ts-1","r4-ss-1","r5-ts-1","r5-ss-1","r1-td-1","r2-td-1","r3-td-1","r4-td-1","r5-td-1","r1-kd-1","r2-kd-1","r3-kd-1","r4-kd-1","r5-kd-1","r1-ts-2","r1-ss-2","r2-ts-2","r2-ss-2","r3-ts-2","r3-ss-2","r4-ts-2","r4-ss-2","r5-ts-2","r5-ss-2","r1-td-2","r2-td-2","r3-td-2","r4-td-2","r5-td-2","r1-kd-2","r2-kd-2","r3-kd-2","r4-kd-2","r5-kd-2"])
X=df.drop(columns=["outcome","sr_no"])

#dfna=df.isna().sum() we got to know here the tkd-att-2 had many Nan's values which were unresolved.
#status: resolved
#print(dfna[dfna>0])


pipe=Pipeline(steps=[('scaler',StandardScaler()),('model',LogisticRegression())])
#pipe_=Pipeline(steps=[('scaler',quantile_transform()),('model',LogisticRegression())])
pipe1=Pipeline(steps=[("scaler",StandardScaler()),("model",DecisionTreeClassifier())])
#pipe_1=Pipeline(steps=[("scaler",quantile_transform()),("model",DecisionTreeClassifier())])
pipe3=Pipeline(steps=[("scaler",StandardScaler()),("model",MLPClassifier())])
#pipe_3=Pipeline(steps=[("scaler",quantile_transform()),("model",MLPClassifier())])

X_train,X_test,Y_train,Y_test=train_test_split(X,Y,random_state=42,test_size=0.2)
pipe.fit(X_train,Y_train)
pipe1.fit(X_train,Y_train)
pipe3.fit(X_train,Y_train)
#print(pipe.predict(X_test))

print("Logistic Regression metrics")
print(accuracy_score(Y_test,pipe.predict(X_test)))
print(precision_score(Y_test,pipe.predict(X_test)))
print("DecisionTreeClassifier metrics")
print(accuracy_score(Y_test,pipe1.predict(X_test)))
print(precision_score(Y_test,pipe1.predict(X_test)))
print("MLP metrics")
print(accuracy_score(Y_test,pipe3.predict(X_test)))
print(precision_score(Y_test,pipe3.predict(X_test)))

#Conclusion1: round-wise stats improve accuracy by only a minute percentage with the heavy reliance on overall stats.
#Conclusion2: LogisticRegression>DecisionTreeClassifier,MLP