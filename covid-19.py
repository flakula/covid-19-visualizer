import matplotlib.pyplot as plt
import numpy as np
import time
import pandas as pd
import streamlit as st

st.title('CoViD-19')

ds = st.sidebar.radio("Dataset",options=["new_cases", "new_deaths", "total_cases", "total_deaths"])
df = pd.read_csv(ds+".csv")

if st.sidebar.checkbox("Print full data set"):
	df
	
countries = []
l = len(df) - 1
st.write("Date: ",df.loc[l, "date"], "World: ", df.loc[l, "World"])

for country in df:
	try:
		if int(df.loc[l, country]) > 0:
	 		countries.append((country, df.loc[l, country]))
	except Exception as e:
 		pass

if st.sidebar.checkbox("Top 10", True):
	sorted_by_value = sorted(countries, key=lambda tup: 20947 - tup[1])
	# for x, y in sorted_by_value[:10]:
	# 	st.write(x,y)
	countries = sorted_by_value[1:10]
else:
	countries = countries[1:]

# i = st.sidebar.slider("filter >=", 0, 10000, 100, step=100)
i = 0
d = pd.DataFrame(columns=[a for a,b in countries if b >= i])
d.loc[0] = [b for a,b in countries if b > i]
# st.write(df.loc[l][2:])
st.write(d)

mode = st.sidebar.radio("Select view", ["One country curve", "Countries comparison"])

if mode == "One country curve":
	country = st.sidebar.selectbox("Country",d.columns)
	plt.bar(range(l+1), df[country])
	st.pyplot()
if mode == "Countries comparison":
	# countries = countries[1:]
	plt.bar(range(len(d.columns)), d.loc[0])
	plt.xticks(range(len(d.columns)), d.columns)
	labels = plt.axes().get_xticklabels()
	plt.setp(labels, rotation = 30.)
	st.pyplot()
