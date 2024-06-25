import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import koreanize_matplotlib

# Streamlit app
st.title('연령대별 인구수 시각화')

# File uploader
uploaded_file = st.file_uploader("CSV 파일을 업로드하세요", type=["csv"])

if uploaded_file is not None:
    # Load the dataset
    population_data = pd.read_csv(uploaded_file, encoding='euc-kr')

    # Extract necessary columns and clean the data
    population_data = population_data[['행정구역'] + [col for col in population_data.columns if '세' in col]]

    # Split the columns for male and female populations
    male_columns = [col for col in population_data.columns if '남' in col]
    female_columns = [col for col in population_data.columns if '여' in col]

    # Ensure the columns are in the same order
    male_columns.sort(key=lambda x: int(x.split('_')[1][:-1]))  # Sort by age
    female_columns.sort(key=lambda x: int(x.split('_')[1][:-1]))  # Sort by age

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
    fig, ax = plt.subplots(figsize=(16, 18))  # Increase figure size, height is 1.5x

    # Plot male population (positive values)
    ax.barh(age_groups, male_data['인구수'], color='skyblue', label='남성')

    # Plot female population (negative values)
    ax.barh(age_groups, -female_data['인구수'], color='lightpink', label='여성')

    ax.set_title(f'{selected_region} 연령대별 인구수')
    ax.set_ylabel('연령')
    ax.set_xlabel('인구수')
    ax.legend()

    # Rotate x-axis labels
    plt.xticks(rotation=45)

    # Add the ticks for both positive and negative values
    max_population = max(male_data['인구수'].max(), female_data['인구수'].max())
    ax.set_xlim(-max_population, max_population)
    ax.xaxis.set_major_locator(plt.MultipleLocator(1000))  # Set x-axis interval to 1000

    # Adjust layout for better fit
    fig.tight_layout(pad=3.0)

    st.pyplot(fig)
else:
    st.write("CSV 파일을 업로드해주세요.")
