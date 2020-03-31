import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import time
import pandas as pd
import streamlit as st

st.title('CoViD-19')

dataset_array = ["new_cases", "new_deaths", "total_cases", "total_deaths"]

mode = st.sidebar.radio("Select view", ["One country curve", "Countries comparison", "Summary"])

# @st.cache(persist=True)
def read_csv(array):
	dataframes_dict = {}
	for dataset in dataset_array:
		dataframes_dict[dataset] = pd.read_csv(dataset+".csv")
	return dataframes_dict

dataframes_dict = read_csv(dataset_array)

# i = st.sidebar.slider("filter >=", 0, 10000, 100, step=100)
i = st.sidebar.number_input('Insert a number to filter >=', min_value=0, max_value=10000, value=100, step=100)
top10 = st.sidebar.checkbox("Top-10")

df_filtered_dict = {}
top10_countries = {}

for dataset_key in dataframes_dict:
	countries = []
	
	# select top 10
	last_pos = len(dataframes_dict[dataset_key]) -1
	for country in dataframes_dict[dataset_key].columns[1:]:
		try:  
			if int(dataframes_dict[dataset_key].loc[last_pos,country]) >= i:
				countries.append((country, int(dataframes_dict[dataset_key].loc[last_pos,country])))
		except Exception as e:
			pass
	if top10:
		countries = sorted(countries, key=lambda tup: - tup[1])[:11]
	else:
		countries = sorted(countries, key=lambda tup: - tup[1])
	
	df_filtered = pd.DataFrame(columns=[a for a,b in countries])
	df_filtered.loc[dataset_key] = [b for a,b in countries]

	# st.write(df_filtered)
	df_filtered_dict[dataset_key] = df_filtered

	for a,b in countries:
		top10_countries[a] = a

if mode == "One country curve":
	all_dataset = st.sidebar.checkbox("All in One")
	country = st.sidebar.selectbox("Country", list(top10_countries))
	# country = st.sidebar.selectbox("Country", sorted(list(top10_countries)))
	if all_dataset:
		grid_size = (7,7)
		pos = [(0, 0),(0, 4),(4, 0),(4, 4)]
		for i in range(4):
			plt.subplot2grid(grid_size, pos[i], rowspan=3, colspan=3)
			plt.bar(range(last_pos+1), dataframes_dict[dataset_array[i]][country])
			plt.title(dataset_array[i])

		st.pyplot()
		st.subheader(country)
		st.write(	"new_cases", 	dataframes_dict["new_cases"		].loc[last_pos,country],
					"new_deaths", 	dataframes_dict["new_deaths"	].loc[last_pos,country],
					"total_cases", 	dataframes_dict["total_cases"	].loc[last_pos,country],
					"total_deaths", dataframes_dict["total_deaths"	].loc[last_pos,country])

	else:
		selected_dataset = st.sidebar.radio("Dataset",options=dataset_array)
		plt.bar(range(last_pos+1), dataframes_dict[selected_dataset][country])
		st.pyplot()
		st.subheader(country)
		st.write(selected_dataset, dataframes_dict[selected_dataset].loc[last_pos,country])

if mode == "Countries comparison":
	countries = countries[1:]
	selected_dataset = st.sidebar.radio("Dataset", options=dataset_array)
	df_filtered_dict[selected_dataset].drop(['World'], axis='columns', inplace=True)
	plt.bar(range(len(df_filtered_dict[selected_dataset].columns)), df_filtered_dict[selected_dataset].loc[selected_dataset])
	plt.xticks(range(len(df_filtered_dict[selected_dataset].columns)), df_filtered_dict[selected_dataset].columns)
	labels = plt.axes().get_xticklabels()
	plt.setp(labels, rotation = 30.)
	st.pyplot()
	st.write(df_filtered_dict[selected_dataset])

if mode == "Summary":
	for dataset_key in dataframes_dict:
		st.write(df_filtered_dict[dataset_key])
		# st.write(dataframes_dict[dataset_key].describe())
