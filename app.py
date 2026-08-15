import streamlit as st 
from Logic_engine.engine import fighter_prob
import json 

with open("pri-fighter-link.json",'r') as f:
    pfl=json.load(f)
names=list(pfl.keys())

st.title("UFC Fighter Predictor")
name1=st.selectbox("fighter1",names)
name2=st.selectbox("fighter2",names)

if(st.button("Predict!")):
    result=fighter_prob(name1,name2)
    st.write(result)
