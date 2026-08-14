import pandas as pd  #type: ignore
from sklearn.pipeline import Pipeline #type: ignore
from sklearn.preprocessing import StandardScaler #type: ignore
from sklearn.preprocessing import QuantileTransformer #type: ignore
from sklearn.linear_model import LogisticRegression #type: ignore
from sklearn.model_selection import train_test_split #type: ignore
from sklearn.metrics import precision_score, accuracy_score, confusion_matrix,recall_score #type: ignore
from sklearn.tree import DecisionTreeClassifier #type: ignore
from sklearn.ensemble import RandomForestClassifier #type: ignore
import matplotlib.pyplot as plt #type: ignore
from sklearn.metrics import roc_curve #type: ignore
from sklearn.metrics import RocCurveDisplay #type: ignore
from xgboost import XGBClassifier 
import time 
from sklearn.calibration import CalibrationDisplay #type: ignore
from sklearn.metrics import log_loss #type: ignore
import joblib #type: ignore

#Input CSV File
df=pd.read_csv("processed_data.csv")

#Initialise Parameters
Y=df["outcome"] # target values 
X=df.drop(columns=["outcome","sr_no","r1-ts-1","r1-ss-1","r2-ts-1","r2-ss-1","r3-ts-1","r3-ss-1","r4-ts-1","r4-ss-1","r5-ts-1","r5-ss-1","r1-td-1","r2-td-1","r3-td-1","r4-td-1","r5-td-1","r1-kd-1","r2-kd-1","r3-kd-1","r4-kd-1","r5-kd-1","r1-ts-2","r1-ss-2","r2-ts-2","r2-ss-2","r3-ts-2","r3-ss-2","r4-ts-2","r4-ss-2","r5-ts-2","r5-ss-2","r1-td-2","r2-td-2","r3-td-2","r4-td-2","r5-td-2","r1-kd-2","r2-kd-2","r3-kd-2","r4-kd-2","r5-kd-2"])
#X=df.drop(columns=["outcome","sr_no"])
#We Choose to drop round-wise stats as they have very little impact on accuracy.
#+ To predict a fight we won't have the round -wise stats available.

#dfna=df.isna().sum() we got to know here the tkd-att-2 had many Nan's values which were unresolved.
#status: resolved
#print(dfna[dfna>0])

#Train-Test-Split
X_train,X_test,Y_train,Y_test=train_test_split(X,Y,random_state=42,test_size=0.2)

#Model-Selection

a=time.time()
#Model 1: Logistic Regression
pipe=Pipeline(steps=[('scaler',StandardScaler()),('model',LogisticRegression(max_iter=1000))])
pipe.fit(X_train,Y_train)
print("Logistic Regression metrics")
print("Accuracy Score:-",end="---")
print(accuracy_score(Y_test,pipe.predict(X_test))*100,end="%\n")
print("Precision Score:-",end="---")
print(precision_score(Y_test,pipe.predict(X_test))*100,end="%\n")
print(confusion_matrix(Y_test,pipe.predict(X_test)))
print("Recall Score:-",end="---")
print(recall_score(Y_test,pipe.predict(X_test))*100)
RocCurveDisplay.from_estimator(pipe,X_test,Y_test)
CalibrationDisplay.from_estimator(pipe,X_test,Y_test)
print(f'logloss: {log_loss(y_true=Y_test,y_pred=pipe.predict(X_test))}')
print(f'Model 1 exec time: {time.time()-a}')

a=time.time()
#Model 2: Logistic Regression + Quantile Transformer 
pipe_=Pipeline(steps=[("transformer",QuantileTransformer(output_distribution="normal")),("model",LogisticRegression())])
pipe_.fit(X_train,Y_train)
print("----quantileTransformer----")
print("Accuracy Score:-",end="---")
print(accuracy_score(Y_test,pipe_.predict(X_test))*100,end="%\n")
print("Precision Score:-",end="---")
print(precision_score(Y_test,pipe_.predict(X_test))*100,end="%\n")
print(confusion_matrix(Y_test,pipe_.predict(X_test)))
print("Recall Score:-",end="---")
print(recall_score(Y_test,pipe_.predict(X_test))*100)
RocCurveDisplay.from_estimator(pipe_,X_test,Y_test)
CalibrationDisplay.from_estimator(pipe_,X_test,Y_test)
print(f'logloss: {log_loss(y_true=Y_test,y_pred=pipe_.predict(X_test))}')
print(f'Model 2 exec time: {time.time()-a}')

a=time.time()
#Model 3: Decision Tree Classifier + Standard Scaler
pipe1=Pipeline(steps=[("scaler",StandardScaler()),("model",DecisionTreeClassifier())])
pipe1.fit(X_train,Y_train)
print("DecisionTreeClassifier metrics")
print("Accuracy Score:-",end="---")
print(accuracy_score(Y_test,pipe1.predict(X_test))*100,end="%\n")
print("Precision Score:-",end="---")
print(precision_score(Y_test,pipe1.predict(X_test))*100,end="%\n")
print(confusion_matrix(Y_test,pipe1.predict(X_test)))
print("Recall Score:-",end="---")
print(recall_score(Y_test,pipe1.predict(X_test))*100)
RocCurveDisplay.from_estimator(pipe1,X_test,Y_test)
CalibrationDisplay.from_estimator(pipe1,X_test,Y_test)
print(f'logloss: {log_loss(y_true=Y_test,y_pred=pipe1.predict(X_test))}')
print(f'Model 3 exec time: {time.time()-a}')

a=time.time()
#Model 4: RandomForestClassifier + Standard Scaler
#pipe3=Pipeline(steps=[("scaler",QuantileTransformer(output_distribution="normal")),("clf",RandomForestClassifier(n_estimators=500,max_depth=None,random_state=42))])
pipe3=Pipeline(steps=[("scaler",StandardScaler()),("clf",RandomForestClassifier(n_estimators=500,max_depth=None,random_state=42))])
pipe3.fit(X_train,Y_train)
print("RandomForestClassifier metrics")
print("Accuracy Score:-",end="---")
print(accuracy_score(Y_test,pipe3.predict(X_test))*100,end="%\n")
print("Precision Score:-",end="---")
print(precision_score(Y_test,pipe3.predict(X_test))*100,end="%\n")
print(confusion_matrix(Y_test,pipe3.predict(X_test)))
print("Recall Score:-",end="---")
print(recall_score(Y_test,pipe3.predict(X_test))*100)
RocCurveDisplay.from_estimator(pipe3,X_test,Y_test)
CalibrationDisplay.from_estimator(pipe3,X_test,Y_test)
print(f'logloss: {log_loss(y_true=Y_test,y_pred=pipe3.predict(X_test))}')
print(f'Model 4 exec time: {time.time()-a}')

a=time.time()
#Model 5: XGBClassifier + Standard Scaler
#pipe4=Pipeline(steps=[("transformer",QuantileTransformer(output_distribution="normal")),("model",XGBClassifier(n_estimators=500,max_depth=None,learning_rate=1,objective="binary:logistic"))])
pipe4=Pipeline(steps=[("scaler",StandardScaler()),("model",XGBClassifier(n_estimators=500,max_depth=None,learning_rate=1,objective="binary:logistic"))])
pipe4.fit(X_train,Y_train)
print("XGBClassifier metrics")
print("Accuracy Score:-",end="---")
print(accuracy_score(Y_test,pipe4.predict(X_test))*100,end="%\n")
print("Precision Score:-",end="---")
print(precision_score(Y_test,pipe4.predict(X_test))*100,end="%\n")
print(confusion_matrix(Y_test,pipe4.predict(X_test)))
print("Recall Score:-",end="---")
print(recall_score(Y_test,pipe4.predict(X_test))*100)
RocCurveDisplay.from_estimator(pipe4,X_test,Y_test)
CalibrationDisplay.from_estimator(pipe4,X_test,Y_test)
print(f'logloss: {log_loss(y_true=Y_test,y_pred=pipe4.predict(X_test))}')
print(f'Model 5 exec time: {time.time()-a}')

plt.show()

joblib.dump(pipe_,"lrqt.joblib")
joblib.dump(pipe3,"rfc.joblib")

#print("MLP metrics")
#print(accuracy_score(Y_test,pipe3.predict(X_test)))
#print(precision_score(Y_test,pipe3.predict(X_test)))
#Conclusion1: round-wise stats improve accuracy by only a minute percentage with the heavy reliance on overall stats.
#Conclusion2: LogisticRegression>DecisionTreeClassifier,MLP
#Conclusion 3 : better results with Logistics regression + quantile Transformer
#Conclusion 4: better results from RandomForestClasssifier based on ROC-AUC + quantile transformer 
#Conclusion 5: XGB's AUC ~= LR+QT's 
#Conclusion 6: LR+QT's execution time < RFC's exec time with <1% accuracy change so we choose model 2
#Conclusion 7 : Model 2 > Model 4 in terms of Calibration and log loss