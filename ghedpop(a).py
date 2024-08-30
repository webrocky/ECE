# -*- coding: utf-8 -*-
"""ghedpop(A).ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1gBIr7vk8cN5Qe2i-0ffO8gvW9cpBw6UJ

***#Loading the data***

---> **GHED_data.csv is Global healthcare expenditure data**

---> **population_data.csv is the agewise population of data.**
"""

import pandas as pd

# Load GHED and population data
ghed_data = pd.read_csv('/content/GHED_data.csv')
population_data = pd.read_csv('/content/population_data.csv')

# Display initial rows of the datasets
print(ghed_data.head())
print(population_data.head())

"""***#Basic information of GHED_data***"""

# Display basic information about the dataset
print("Basic Information:")
ghed_data.info()

"""***#Basic information of population_data.***"""

# Display basic information about the dataset
print("Basic Information:")
population_data.info()

"""***#Distribution of country***"""

# Explore the distribution of a specific column (replace 'column_name' with the actual column name)
column_name = 'country'  # Replace with the actual column name you want to explore
print(f"\nDistribution of {column_name}:")
ghed_data[column_name].value_counts()

"""***#Descriptive statistics of GHED_data***"""

# Descriptive statistics for numerical columns
print("\nDescriptive Statistics:")
print(ghed_data.describe())

"""***#Descriptive statistics of population_data***"""

# Descriptive statistics for numerical columns
print("\nDescriptive Statistics:")
print(population_data.describe())

"""**#Data cleaning**

***#Missing values in GHED dataset***
"""

# Check for missing values in the dataset
print("\nMissing Values:")
ghed_data.isnull().sum()

# Remove rows where the Year is 2022
ghed_data_filtered = ghed_data[ghed_data['Year'] != 2022]

# Display the filtered data to confirm
print(ghed_data_filtered)

"""***#Missing values in population_data***"""

# Check for missing values in the dataset
print("\nMissing Values:")
population_data.isnull().sum()

"""***#Merging the dataset ghed_data and population_data and replacing missing values.***"""

import pandas as pd
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer

# Merge datasets on 'country' and 'year'
merged_data = pd.merge(ghed_data_filtered, population_data, on=['country', 'Year'])

# Function to iteratively fill missing values with neighboring values
def iterative_fill(df):
    missing_before = df.isnull().sum().sum()

    # Iteratively apply forward fill and backward fill until no missing values are left
    while missing_before > 0:
        df.fillna(method='ffill', inplace=True)
        df.fillna(method='bfill', inplace=True)
        missing_after = df.isnull().sum().sum()
        if missing_after == missing_before:
            break
        missing_before = missing_after

    return df

# Apply the iterative fill function to the merged data
ghedpop = iterative_fill(merged_data.copy()) # Create the ghedpop DataFrame here



# Check if there are any missing values left
print("Total Missing Values After Cleaning:", ghedpop.isnull().sum().sum())

"""**####**

***#Handling outliers***
"""

# Handling outliers using the Interquartile Range (IQR) method
def identify_outliers(df, column):
    # Convert the column to numeric, handling errors by coercing non-numeric values to NaN
    df[column] = pd.to_numeric(df[column], errors='coerce')

    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1

    # Identify the rows with outliers
    outliers = df[(df[column] < (Q1 - 1.5 * IQR)) | (df[column] > (Q3 + 1.5 * IQR))]

    return outliers

# List of columns you want to check for outliers
columns_to_check = [

    'che'

]

# Loop through each column and identify outliers
for col in columns_to_check:
    outliers = identify_outliers(df=ghedpop.copy(), column=col) # Use a copy of the DataFrame to avoid modifying the original
    if not outliers.empty:
        print(f"Outliers in column {col}:")
        print(outliers)
        print("\n")

"""***#Checking column names in ghedpop (merged dataset)***"""

print("\nColumn Names:")
ghedpop.columns

"""***#Data type of each column***"""

# Display the data types of each column
print("\nData Types:")
ghedpop.dtypes

"""***#Downloaded our dataset ghedpop***"""

ghedpop.to_csv('ghedpop.csv', index=False)

from google.colab import files
files.download('ghedpop.csv')

"""***#Total population of country(2000-2021)***"""

import pandas as pd



# Here, we aggregate all the relevant population columns to calculate the total population for each country and year

ghedpop['total_population'] = (
    ghedpop['Population - Sex: all - Age: 0-4 - Variant: estimates'] +
    ghedpop['Population - Sex: all - Age: 5-9 - Variant: estimates'] +
    ghedpop['Population - Sex: all - Age: 10-14 - Variant: estimates'] +
    ghedpop['Population - Sex: all - Age: 15-19 - Variant: estimates'] +
    ghedpop['Population - Sex: all - Age: 20-24 - Variant: estimates'] +
    ghedpop['Population - Sex: all - Age: 25-29 - Variant: estimates'] +
    ghedpop['Population - Sex: all - Age: 30-34 - Variant: estimates'] +
    ghedpop['Population - Sex: all - Age: 35-39 - Variant: estimates'] +
    ghedpop['Population - Sex: all - Age: 40-44 - Variant: estimates'] +
    ghedpop['Population - Sex: all - Age: 45-49 - Variant: estimates'] +
    ghedpop['Population - Sex: all - Age: 50-54 - Variant: estimates'] +
    ghedpop['Population - Sex: all - Age: 55-59 - Variant: estimates'] +
    ghedpop['Population - Sex: all - Age: 60-64 - Variant: estimates'] +
    ghedpop['Population - Sex: all - Age: 65-69 - Variant: estimates'] +
    ghedpop['Population - Sex: all - Age: 70-74 - Variant: estimates'] +
    ghedpop['Population - Sex: all - Age: 75-79 - Variant: estimates'] +
    ghedpop['Population - Sex: all - Age: 80-84 - Variant: estimates'] +
    ghedpop['Population - Sex: all - Age: 85-89 - Variant: estimates'] +
    ghedpop['Population - Sex: all - Age: 90-94 - Variant: estimates'] +
    ghedpop['Population - Sex: all - Age: 95-99 - Variant: estimates'] +
    ghedpop['Population - Sex: all - Age: 100+ - Variant: estimates']
)

# Check the result of the total population calculation
print(ghedpop[['country', 'Year', 'total_population']].head())



# add column total_population in ghedpop

"""***#Elderly population by country(Age 60+) and Elderly population growth rate***"""

import pandas as pd



df = ghedpop  # Assuming ghedp_data is your DataFrame

# Aggregating population for age 60+ based on the given column names
df['population_60_plus'] = (
    df['Population - Sex: all - Age: 60-64 - Variant: estimates'] +
    df['Population - Sex: all - Age: 65-69 - Variant: estimates'] +
    df['Population - Sex: all - Age: 70-74 - Variant: estimates'] +
    df['Population - Sex: all - Age: 75-79 - Variant: estimates'] +
    df['Population - Sex: all - Age: 80-84 - Variant: estimates'] +
    df['Population - Sex: all - Age: 85-89 - Variant: estimates'] +
    df['Population - Sex: all - Age: 90-94 - Variant: estimates'] +
    df['Population - Sex: all - Age: 95-99 - Variant: estimates'] +
    df['Population - Sex: all - Age: 100+ - Variant: estimates']
)

# Checking if the new column was created successfully
print(df[['country', 'Year', 'population_60_plus']].head())

# Use the new population_60_plus column to calculate elderly population growth rate
ghedpop['elderly_population_growth_rate'] = (
    ghedpop.groupby('country')['population_60_plus'].pct_change() * 100
)

# Display a preview of the updated columns
print(ghedpop[['country', 'Year', 'elderly_population_growth_rate']].head())

"""***#Visualizations for Elderly population by country(Age 60+)***

--> **Line chart**

--> **Bubble chart**
"""

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# Assuming df is your dataframe with the 'population_60_plus' column

# Filter for a specific country (e.g., Germany) to visualize its elderly population growth
country_data = df[df['country'] == 'India']

# 1. **Line Chart**: Futuristic line chart showing elderly population growth
line_chart = px.line(
    country_data, x='Year', y='population_60_plus',
    title='Elderly Population Growth (60+) in India',
    labels={'population_60_plus': 'Elderly Population (60+)', 'Year': 'Year'},
    template='plotly_dark',
    markers=True,
    line_shape='spline'
)
line_chart.update_traces(line=dict(width=4), marker=dict(size=10, symbol='circle'))
line_chart.update_layout(font=dict(size=16, color="white"), title_x=0.5)
line_chart.show()


# Create the Bubble Chart with the filtered data
bubble_chart = px.scatter(
    country_data, x='Year', y='population_60_plus',
    size='population_60_plus',
    title='Elderly Population Growth (60+) in India - Bubble Chart',
    labels={'population_60_plus': 'Elderly Population (60+)', 'Year': 'Year'},
    template='plotly_dark',
    color='population_60_plus',
    color_continuous_scale=px.colors.sequential.Plasma
)

# Update x-axis to show ticks at 5-year intervals and limit the range
bubble_chart.update_xaxes(dtick=5, range=[country_data['Year'].min(), 2021])

# Update marker and layout settings
bubble_chart.update_traces(marker=dict(sizemode='diameter', line_width=2))
bubble_chart.update_layout(font=dict(size=16, color="white"), title_x=0.5)

# Show the bubble chart
bubble_chart.show()

"""**Our dataset ghedpop**


"""

import pandas as pd  # Import the pandas library and give it the alias 'pd'

ghedpop = pd.read_csv('ghedpop.csv')

import pandas as pd

# Step 1: Load the ghedpop CSV file
ghedpop = pd.read_csv('ghedpop.csv')  # Replace with the actual path to your CSV file

# Step 2: Aggregate all the relevant population columns to calculate total_population for each country and year
ghedpop['total_population'] = (
    ghedpop['Population - Sex: all - Age: 0-4 - Variant: estimates'] +
    ghedpop['Population - Sex: all - Age: 5-9 - Variant: estimates'] +
    ghedpop['Population - Sex: all - Age: 10-14 - Variant: estimates'] +
    ghedpop['Population - Sex: all - Age: 15-19 - Variant: estimates'] +
    ghedpop['Population - Sex: all - Age: 20-24 - Variant: estimates'] +
    ghedpop['Population - Sex: all - Age: 25-29 - Variant: estimates'] +
    ghedpop['Population - Sex: all - Age: 30-34 - Variant: estimates'] +
    ghedpop['Population - Sex: all - Age: 35-39 - Variant: estimates'] +
    ghedpop['Population - Sex: all - Age: 40-44 - Variant: estimates'] +
    ghedpop['Population - Sex: all - Age: 45-49 - Variant: estimates'] +
    ghedpop['Population - Sex: all - Age: 50-54 - Variant: estimates'] +
    ghedpop['Population - Sex: all - Age: 55-59 - Variant: estimates'] +
    ghedpop['Population - Sex: all - Age: 60-64 - Variant: estimates'] +
    ghedpop['Population - Sex: all - Age: 65-69 - Variant: estimates'] +
    ghedpop['Population - Sex: all - Age: 70-74 - Variant: estimates'] +
    ghedpop['Population - Sex: all - Age: 75-79 - Variant: estimates'] +
    ghedpop['Population - Sex: all - Age: 80-84 - Variant: estimates'] +
    ghedpop['Population - Sex: all - Age: 85-89 - Variant: estimates'] +
    ghedpop['Population - Sex: all - Age: 90-94 - Variant: estimates'] +
    ghedpop['Population - Sex: all - Age: 95-99 - Variant: estimates'] +
    ghedpop['Population - Sex: all - Age: 100+ - Variant: estimates']
)

# Step 3: Aggregate population for age 60+ based on the given column names
ghedpop['population_60_plus'] = (
    ghedpop['Population - Sex: all - Age: 60-64 - Variant: estimates'] +
    ghedpop['Population - Sex: all - Age: 65-69 - Variant: estimates'] +
    ghedpop['Population - Sex: all - Age: 70-74 - Variant: estimates'] +
    ghedpop['Population - Sex: all - Age: 75-79 - Variant: estimates'] +
    ghedpop['Population - Sex: all - Age: 80-84 - Variant: estimates'] +
    ghedpop['Population - Sex: all - Age: 85-89 - Variant: estimates'] +
    ghedpop['Population - Sex: all - Age: 90-94 - Variant: estimates'] +
    ghedpop['Population - Sex: all - Age: 95-99 - Variant: estimates'] +
    ghedpop['Population - Sex: all - Age: 100+ - Variant: estimates']
)

# Step 4: Calculate elderly population growth rate using the new column
ghedpop['elderly_population_growth_rate'] = (
    ghedpop.groupby('country')['population_60_plus'].pct_change() * 100
)

# Step 5: Verify the newly added columns
print(ghedpop[['country', 'Year', 'total_population', 'population_60_plus', 'elderly_population_growth_rate']].head())

# Step 6: Save the updated DataFrame back to CSV with the new columns
ghedpop.to_csv('updated_ghedpop.csv', index=False)  # Replace with the desired file path

import pandas as pd
from google.colab import files

# Assuming ghedpop DataFrame is already created and updated

# Save the updated DataFrame as CSV in the Colab file system
ghedpop.to_csv('updated_ghedpop.csv', index=False)

# Download the file
files.download('updated_ghedpop.csv')