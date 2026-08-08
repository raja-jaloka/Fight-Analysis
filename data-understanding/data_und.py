import matplotlib.pyplot as plt 
import sklearn as sk
import pandas as pd 

df=pd.read_csv("processed_data.csv")

Y=df["outcome"] #labels of outcome i.e win or loss
X=df.drop(columns=["outcome","sr_no"]) #all data except labels 
#print(X)
#print(Y)

plt.hist(X["b-tar-1"])
plt.xlabel("number of fighters")
plt.ylabel("body targets")
plt.show()