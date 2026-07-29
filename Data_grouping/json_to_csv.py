import pandas as pd  # type: ignore[import]
#df=pd.read_json('stats_per_fight.json',encoding='utf-8-sig')
#df.to_csv("stats_per_fight.csv", index=False, encoding='utf-8-sig')

df=pd.read_json('usable_data.json',encoding='utf-8-sig')
df.to_csv("usable_data.csv",index=True,encoding='utf-8-sig')