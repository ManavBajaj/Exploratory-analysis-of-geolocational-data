# GeoScope: Exploratory Analysis of Geolocational Data  

GeoScope is an interactive web application designed to analyze and visualize geolocational data with a focus on food preferences and apartment locality. Built using Streamlit, this tool leverages clustering algorithms to reveal spatial patterns in food-related amenities—assisting students, urban planners, and businesses in making data-driven decisions.

##  Key Features
-  **Clustering Algorithms**  
  Implements K-Means, Hierarchical Clustering, and Affinity Propagation to analyze apartment clusters based on food venue proximity.

-  **Interactive Mapping with Folium**  
  Visualizes spatial data clusters directly on a map for intuitive insight.

-  **Geocoding with Geopy**  
  Converts location names into coordinates dynamically using the Nominatim API.

-  **Streamlit Interface**  
  Fully interactive and easy-to-use interface with sections for About, Coordinate Entry, Clustering, and EDA.

-  **Exploratory Data Analysis (EDA)**  
  Box plots and summary statistics reveal relationships within the dataset using Pandas, Matplotlib, and Seaborn.

-  **Dynamic Execution**  
  Runs clustering algorithms in real-time through Python’s `subprocess` module for modular code integration.

##  Tech Stack
- Python 3.7+
- [Streamlit](https://streamlit.io/)
- [Geopy](https://geopy.readthedocs.io/)
- [Folium](https://python-visualization.github.io/folium/)
- [Pandas](https://pandas.pydata.org/)
- [Scikit-learn](https://scikit-learn.org/)
- [Matplotlib](https://matplotlib.org/)
- [Seaborn](https://seaborn.pydata.org/)

##  How It Works
1. Enter a location or geographic coordinates in the sidebar.
2. Choose a clustering algorithm (K-Means, Hierarchical, Affinity Propagation).
3. View output maps, box plots, and silhouette scores.
4. Navigate to the EDA tab for deeper insights into spatial relationships and food choices.
