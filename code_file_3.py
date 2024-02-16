import pandas as pd
from pandas import json_normalize
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import silhouette_score
from sklearn.cluster import AffinityPropagation
import folium as f
import json
import requests

# Load the dataset
full_dataset = pd.read_csv("food_coded.csv")

# Select relevant columns
relevent = full_dataset[['cook', 'eating_out', 'employment', 'ethnic_food', 'exercise', 'fruit_day', 'income', 'on_off_campus', 'pay_meal_out', 'sports', 'veggies_day']]

print(full_dataset.head())
print(full_dataset.info())
#print(full_dataset.describe())

missing_values_count = relevent.isnull().sum()
print(missing_values_count)

# how many total missing values do we have?
total_cells = np.product(relevent.shape)
total_missing = missing_values_count.sum()

# percent of data that is missing
percent_missing = (total_missing/total_cells) * 100
print(percent_missing)

#As percent missing is less than 5%,we are dropping rows containing missing values.
relevent_with_no_na=relevent.dropna(axis=0)
print(relevent_with_no_na.shape[0])

# Boxplot
fig = plt.figure(figsize=(10, 5))
ax = sns.boxplot(data=relevent_with_no_na, linewidth=2)
plt.show()

# Foursquare API Credentials
CLIENT_ID = 'YVXU3P2WSRWZAFQPVSSO3HHUVWZ5TIMEW1NNKENYURXHMMKD'
CLIENT_SECRET = 'Q3ABL5LX1B2AXBEOTM3AIL3NM2DYAJ2JEYJNFMPHYWZJRXHR'
VERSION = '20200604'
LIMIT = 200

# Example location
latitude = 17.4732138
longitude = 78.5115017

# Foursquare API request
search_query = 'Apartment'
radius = 100000
url = 'https://api.foursquare.com/v2/venues/search?client_id={}&client_secret={}&ll={},{}&v={}&query={}&radius={}&limit={}'.format(
    CLIENT_ID, CLIENT_SECRET, latitude, longitude, VERSION, search_query, radius, LIMIT)

results = requests.get(url).json()

# Extract venue information
venues = results['response']['venues']
dataframe = pd.json_normalize(venues)
filtered_columns = ['name', 'categories'] + [col for col in dataframe.columns if col.startswith('location.')] + ['id']
dataframe_filtered = dataframe.loc[:, filtered_columns]

# Function to extract category of the venue
def get_category_type(row):
    try:
        categories_list = row['categories']
    except:
        categories_list = row['venue.categories']

    if len(categories_list) == 0:
        return None
    else:
        return categories_list[0]['name']

# Apply the function to filter the category for each row
dataframe_filtered['categories'] = dataframe_filtered.apply(get_category_type, axis=1)
dataframe_filtered.columns = [column.split('.')[-1] for column in dataframe_filtered.columns]
dataframe_filtered.reset_index(drop=True, inplace=True)
dataframe_filtered.drop(['cc', 'country', 'state', 'city'], axis=1, inplace=True)

# Map visualization
map_bang = f.Map(location=[latitude,longitude], zoom_start=12)
locations = f.map.FeatureGroup()

latitudes = list(dataframe_filtered.lat)
longitudes = list(dataframe_filtered.lng)
labels = list(dataframe_filtered.name)

for lat, lng, label in zip(latitudes, longitudes, labels):
    f.Marker([lat, lng], popup=label).add_to(map_bang)

# add incidents to map
map_bang.add_child(locations)

map_bang
df_evaluate=dataframe_filtered[['lat','lng']]
RestList=[]
latitudes = list(dataframe_filtered.lat)
longitudes = list( dataframe_filtered.lng)
for lat, lng in zip(latitudes, longitudes):
    radius = 100000
    latitude=lat#Query for the apartment location in question
    longitude=lng
    url = 'https://api.foursquare.com/v2/venues/search?client_id={}&client_secret={}&ll={},{}&v={}&query={}&radius={}&limit={}'.format(CLIENT_ID, CLIENT_SECRET, latitude, longitude, VERSION, search_query, radius, LIMIT)
    search_query = 'Restaurant' #Search for any food related locations
    results = requests.get(url).json()
    # assign relevant part of JSON to venues
    venues = results['response']['venues']
    # tranform venues into a dataframe
    dataframe2 = json_normalize(venues)
    filtered_columns = ['name', 'categories'] + [col for col in dataframe2.columns if col.startswith('location.')] + ['id']
    dataframe_filtered2 = dataframe2.loc[:, filtered_columns]
    # filter the category for each row
    dataframe_filtered2['categories'] = dataframe_filtered2.apply(get_category_type, axis=1)
    # clean column names by keeping only last term
    dataframe_filtered2.columns = [column.split('.')[-1] for column in dataframe_filtered2.columns]
    RestList.append(dataframe_filtered2['categories'].count())
df_evaluate['Restaurants']=RestList
FruitList=[]
latitudes = list(dataframe_filtered.lat)
longitudes = list( dataframe_filtered.lng)
for lat, lng in zip(latitudes, longitudes):
    radius = 100000
    latitude=lat#Query for the apartment location in question
    longitude=lng
    url = 'https://api.foursquare.com/v2/venues/search?client_id={}&client_secret={}&ll={},{}&v={}&query={}&radius={}&limit={}'.format(CLIENT_ID, CLIENT_SECRET, latitude, longitude, VERSION, search_query, radius, LIMIT)
    search_query = 'Fruit' #Search for any food related locations
    results = requests.get(url).json()
    
    # assign relevant part of JSON to venues
    venues = results['response']['venues']
    
    # tranform venues into a dataframe
    dataframe2 = json_normalize(venues)
    filtered_columns = ['name', 'categories'] + [col for col in dataframe2.columns if col.startswith('location.')] + ['id']
    dataframe_filtered2 = dataframe2.loc[:, filtered_columns]
    
    # filter the category for each row
    dataframe_filtered2['categories'] = dataframe_filtered2.apply(get_category_type, axis=1)
    
    # clean column names by keeping only last term
    dataframe_filtered2.columns = [column.split('.')[-1] for column in dataframe_filtered2.columns]
    FruitList.append(dataframe_filtered2['categories'].count())

df_evaluate['Fruits,Vegetables,Groceries']=FruitList

# Choose the number of clusters
n_clusters = 3  # You can adjust this parameter

# Run Affinity Propagation
affinity_propagation = AffinityPropagation()
df_evaluate['Cluster'] = affinity_propagation.fit_predict(df_evaluate[['lat', 'lng']])
df_evaluate['Cluster'] = df_evaluate['Cluster'].apply(str)

# calculate silhouette score
sil_score = silhouette_score(df_evaluate[['lat', 'lng']], df_evaluate['Cluster'])
print(f"Silhouette Score: {sil_score}")

#define coordinates of the college
map_bang=f.Map(location=[latitude,longitude],zoom_start=12)

# instantiate a feature group for the incidents in the dataframe
locations = f.map.FeatureGroup()

# set color scheme for the clusters
def color_producer(cluster):
    if cluster=='0':
        return 'green'
    elif cluster=='1':
        return 'orange'
    else:
        return 'red'
latitudes = list(df_evaluate.lat)
longitudes = list(df_evaluate.lng)
labels = list(df_evaluate.Cluster)
names=list(dataframe_filtered.name)
for lat, lng, label,names in zip(latitudes, longitudes, labels,names):
    f.CircleMarker(
            [lat,lng],
            fill=True,
            fill_opacity=1,
            popup=f.Popup(names, max_width = 300),
            radius=5,
            color=color_producer(label)
        ).add_to(map_bang)

# add locations to map
map_bang.add_child(locations)

# Save the map as an HTML file
map_bang.save("map_for_affinitypropogation.html")  



