import streamlit as st
from PIL import Image
import pandas as pd
import plotly.express as px

# Path to the default CSV file and image file
default_csv_path = 'maws_semarang.csv'
default_image_path = 'hasil_model.jpeg'

# Function to read CSV data
def read_csv_data(file_path):
    df = pd.read_csv(file_path)
    return df

# Load data
if 'data' not in st.session_state:
    st.session_state.data = read_csv_data(default_csv_path)

csv_data = st.session_state.data

# Convert 'time' column to datetime
csv_data['time'] = pd.to_datetime(csv_data['time'])

# Custom CSS to set full-width layout and style for title
st.markdown(
    """
    <style>
    .main .block-container {
        max-width: 100%;
        padding-left: 1rem;
        padding-right: 1rem;
    }
    .title-center {
        text-align: center;
        font-size: 36 px; /* Adjust font size as needed */
        font-weight: bold; /* Make text bold */
        margin-bottom: 1rem; /* Optional: add space below the title */
    }
    </style>
    """,
    unsafe_allow_html=True
)


# Title of the dashboard (using markdown for custom styling)
st.markdown('<h1 class="title-center">ROB Flood Prediction in Semarang City</h1>', unsafe_allow_html=True)


# File uploader to allow user to upload a CSV file
#uploaded_file = st.file_uploader("Upload file CSV dengan data prediksi banjir", type=["csv"])

#if uploaded_file is not None:
    # Read the CSV data from the uploaded file
#    csv_data = read_csv_data(uploaded_file)
#   csv_data['time'] = pd.to_datetime(csv_data['time'])
#  st.session_state.data = csv_data

# Create two columns with a specific width ratio
col1, col2 = st.columns([1, 1])

# Display the JPEG image in the left column
with col1:
    st.markdown('<p class="title-center">ROB Flood Potential Map 6 August 2024</p>', unsafe_allow_html=True)
    image = Image.open(default_image_path)
    st.image(image, caption='Semarang City', use_column_width=True)


# Display the dynamic graph in the right column
with col2:
    st.markdown('<p class="title-center">MAWS Water Level Observation</p>', unsafe_allow_html=True)
    st.write("Pelabuhan Tanjung Mas (lon : -6,94351, lat : 110,43131)")
    
    # Filter data based on selected date range
    min_date = csv_data['time'].min().date()
    max_date = csv_data['time'].max().date()
    
    start_date = st.date_input('Pilih tanggal awal', min_date)
    end_date = st.date_input('Pilih tanggal akhir', max_date)
    
    filtered_data = csv_data[(csv_data['time'].dt.date >= start_date) & (csv_data['time'].dt.date <= end_date)]
    
    if not filtered_data.empty:
        fig = px.line(filtered_data, x='time', y='waterlevel_corrected', title='Water Level Observation at Pelabuhan Tanjung Mas')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.write("Tidak ada data untuk rentang waktu yang dipilih.")