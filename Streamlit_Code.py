import streamlit as st
from geopy.geocoders import Nominatim
import subprocess
import pandas as pd

# Function to update coordinates in code files
def update_coordinates_in_code(code_file, new_latitude, new_longitude):
    try:
        with open(code_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        for i in range(len(lines)):
            if "latitude =" in lines[i]:
                lines[i] = f"latitude = {new_latitude}\n"
            elif "longitude =" in lines[i]:
                lines[i] = f"longitude = {new_longitude}\n"

        with open(code_file, 'w', encoding='utf-8') as f:
            f.writelines(lines)

        st.success(f"Coordinates updated in {code_file}")
    except Exception as e:
        st.error(f"An error occurred: {e}")

# Function to run code
def run_code(code_file):
    try:
        # Run the code and collect any output, including paths or data of images
        result = subprocess.run(['python', code_file], capture_output=True, text=True)
        code_output = result.stdout

        # Extract image paths or data from the code output
        image_paths = extract_image_paths(code_output)

        # Display images at the end
        for image_path in image_paths:
            st.image(image_path, caption='Image')

        # Display any other code output if needed
        st.code(code_output, language='python')
    except Exception as e:
        st.error(f"An error occurred: {e}")

# Function to get coordinates from location name
def get_coordinates(location_name):
    geolocator = Nominatim(user_agent="geo_app")
    location = geolocator.geocode(location_name)
    if location:
        return location.latitude, location.longitude
    else:
        return None

# Function to produce color based on cluster label
def color_producer(cluster_label):
    # Define a color mapping logic based on your clusters
    color_mapping = {
        0: 'green',
        1: 'orange',
        2: 'red',
        # Add more cluster labels and corresponding colors if needed
    }

    # Return the color for the given cluster label
    return color_mapping.get(cluster_label, 'gray')  # Default to gray if label not found

# Function to extract image paths from code output
def extract_image_paths(code_output):
    # Example function to extract image paths from code output
    # You should customize this based on how your code generates or saves images
    image_paths = []
    # Your logic here to extract image paths from the code_output
    return image_paths

# Streamlit code
st.title("🌍Geolocational Data Analysis App")

# Sidebar menu
menu_selection = st.sidebar.radio("Menu", ["About the Project", "Enter Coordinates", "Home", "EDA"])

if menu_selection == "About the Project":
    st.header("About the Project")

    about_the_project_text = """
    Welcome to our Geolocational Data Exploratory Analysis application, a powerful tool that integrates k-means, agglomerative hierarchical, and affinity propagation clustering algorithms. This application streamlines the exploration of spatial datasets, empowering users to uncover meaningful patterns and make informed decisions.
        Upon entering user-provided coordinates, the application dynamically updates geographical details for all three clustering algorithms. The user-friendly interface facilitates a seamless exploration process. Marked apartments on an embedded map in HTML format are color-coded into three clusters, providing users with immediate insights into spatial distributions without the need for separate descriptions:

    - **Cluster 0 (Green):** Abundant availability of both restaurants and groceries.
    - **Cluster 1 (Orange):** Plentiful restaurants, with groceries available to a lesser extent.
    - **Cluster 2 (Red):** Relatively limited availability of both restaurants and groceries.

    The visual representation of marked apartments on the map enhances decision-making by offering insights into the amenities available in different regions. Running each clustering algorithm generates box plots, visually representing relationships within the dataset. After each algorithm's execution, the application automatically calculates silhouette scores, enabling users to assess the quality of clusters and choose results based on the clustering method with the highest silhouette score.

    Our application is designed not only for data exploration but also to empower users to make location-based decisions based on the unique characteristics of their geolocational data. With customizable coordinates, dynamic visualizations, embedded maps, and automatic silhouette score calculations, this application ensures a comprehensive and user-friendly geospatial analysis experience. Your journey to uncover spatial insights and make data-driven decisions begins here—effortlessly explore and understand the nuances of your data.

    """

    st.markdown(about_the_project_text)

    # Add images after the text using image names
    st.image("clusters.jpg", use_column_width=True)

elif menu_selection == "Enter Coordinates":
    st.header("Enter Coordinates")

    # Input fields for latitude and longitude
    user_latitude = st.number_input("Enter Latitude:")
    user_longitude = st.number_input("Enter Longitude:")

    # Display the user's input
    st.write(f"Coordinates - Latitude: {user_latitude}, Longitude: {user_longitude}")

    # Button to update coordinates in source codes
    if st.button("Update Coordinates"):
        # Update coordinates in all three source codes
        update_coordinates_in_code("code_file_1.py", user_latitude, user_longitude)
        update_coordinates_in_code("code_file_2.py", user_latitude, user_longitude)
        update_coordinates_in_code("code_file_3.py", user_latitude, user_longitude)

        st.success("Coordinates updated in all source codes. To run the updated codes, use the respective 'Run Code' options.")

elif menu_selection == "Home":
    st.header("Home")

    # Create a single row with three columns for the buttons
    col1, col2, col3 = st.columns(3)

    # Dropdown button for code 1
    selected_option_1 = col1.selectbox("Select an option for kmeans:", ["Select Option", "View Code", "Run Code"], key="code1")

    # Process the selected option for code 1
    if selected_option_1 == "View Code":
        st.code(open("code_file_1.py").read(), language='python')
    elif selected_option_1 == "Run Code":
        run_code("code_file_1.py")

    # Dropdown button for code 2
    selected_option_2 = col2.selectbox("Select an option for Hierarchial clustering:", ["Select Option", "View Code", "Run Code"], key="code2")

    # Process the selected option for code 2
    if selected_option_2 == "View Code":
        st.code(open("code_file_2.py").read(), language='python')
    elif selected_option_2 == "Run Code":
        run_code("code_file_2.py")

    # Dropdown button for code 3
    selected_option_3 = col3.selectbox("Select an option for Affinity propogation:", ["Select Option", "View Code", "Run Code"], key="code3")

    # Process the selected option for code 3
    if selected_option_3 == "View Code":
        st.code(open("code_file_3.py").read(), language='python')
    elif selected_option_3 == "Run Code":
        run_code("code_file_3.py")

elif menu_selection == "EDA":
    st.header("Exploratory Data Analysis (EDA)")

    eda_option = st.sidebar.selectbox("Select an option for EDA:", ["Select Option", "Maps", "Cluster Info"])

    # Process the selected EDA option
    if eda_option == "Maps":
        st.subheader("Maps")

        # File uploader for uploading multiple HTML files
        uploaded_files = st.file_uploader("Upload your HTML files", type=["html"], accept_multiple_files=True)

        if uploaded_files is not None:
            for file_number, uploaded_file in enumerate(uploaded_files, start=1):
                # Display each uploaded HTML file using st.components.v1.html
                st.subheader(f"Map {file_number}")
                map_html = uploaded_file.read().decode('utf-8')
                st.components.v1.html(map_html, height=600)

    elif eda_option == "Cluster Info":
        st.subheader("Cluster Info")

        # Display cluster information in an expander
        with st.expander("Cluster Information"):
            # Define cluster information
            cluster_data = {
                'Cluster 0 (Green)': 'Abundant availability of both restaurants and groceries.',
                'Cluster 1 (Orange)': 'Plentiful restaurants, with groceries available to a lesser extent.',
                'Cluster 2 (Red)': 'Relatively limited availability of both restaurants and groceries.'
            }

            # Display colored circle and cluster information
            for cluster, description in cluster_data.items():
                color = color_producer(int(cluster.split()[1]))
                st.markdown(f'<span style="color: {color}">&#11044;</span> **{cluster} Info:** {description}', unsafe_allow_html=True)
