import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import koreanize_matplotlib

# Load the dataset
file_path = '2023_인구.csv'
population_data = pd.read_csv(file_path, encoding='euc-kr')

# Extract necessary columns and clean the data
population_data = population_data[['행정구역', '총인구수'] + [col for col in population_data.columns if '세' in col]]

# Streamlit app
st.title('연령대별 인구수 시각화')

# User selects the region
regions = population_data['행정구역'].unique()
selected_region = st.selectbox('지역을 선택하세요:', regions)

# Filter data for the selected region
region_data = population_data[population_data['행정구역'] == selected_region]

# Prepare data for plotting
age_columns = [col for col in region_data.columns if '세' in col]
age_data = region_data[age_columns].T
age_data.columns = ['인구수']

# Plotting the data
fig, ax = plt.subplots()
ax.bar(age_data.index, age_data['인구수'], color='skyblue')
ax.set_title(f'{selected_region} 연령대별 인구수')
ax.set_xlabel('연령')
ax.set_ylabel('인구수')
ax.tick_params(axis='x', rotation=90)

st.pyplot(fig)
