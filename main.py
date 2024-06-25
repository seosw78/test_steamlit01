import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import koreanize_matplotlib

# Load the dataset
file_path = '2023_인구.csv'
population_data = pd.read_csv(file_path, encoding='euc-kr')

# Extract necessary columns and clean the data
population_data = population_data[['행정구역'] + [col for col in population_data.columns if '세' in col]]

# Split the columns for male and female populations
male_columns = [col for col in population_data.columns if '남' in col]
female_columns = [col for col in population_data.columns if '여' in col]

# Ensure the columns are in the same order
male_columns.sort()
female_columns.sort()

# Streamlit app
st.title('연령대별 인구수 시각화')

# User selects the region
regions = population_data['행정구역'].unique()
selected_region = st.selectbox('지역을 선택하세요:', regions)

# Filter data for the selected region
region_data = population_data[population_data['행정구역'] == selected_region]

# Prepare data for plotting
male_data = region_data[male_columns].T
male_data.columns = ['인구수']
female_data = region_data[female_columns].T
female_data.columns = ['인구수']

# Convert data to numeric
male_data['인구수'] = pd.to_numeric(male_data['인구수'].str.replace(',', ''), errors='coerce')
female_data['인구수'] = pd.to_numeric(female_data['인구수'].str.replace(',', ''), errors='coerce')

# Extract age groups from column names
age_groups = [col.split('_')[1] for col in male_columns]

# Plotting the data
fig, ax = plt.subplots(figsize=(14, 10))  # Increase figure size

# Plot male population (positive values)
ax.bar(age_groups, male_data['인구수'], color='skyblue', label='남성')

# Plot female population (negative values)
ax.bar(age_groups, -female_data['인구수'], color='lightpink', label='여성')

ax.set_title(f'{selected_region} 연령대별 인구수')
ax.set_ylabel('인구수')
ax.set_xlabel('연령')
ax.legend()

# Rotate x-axis labels
plt.xticks(rotation=45)

# Add the ticks for both positive and negative values
max_population = max(male_data['인구수'].max(), female_data['인구수'].max())
ax.set_ylim(-max_population, max_population)

st.pyplot(fig)
