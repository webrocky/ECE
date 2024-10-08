# -*- coding: utf-8 -*-
"""ghedpop(C).ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1WrIdLNRZ91Bt0Ho1vHvy3ReOY83YcSUy

***Loading the elderly_specific_data. we generated ghedpop after merging ghed and population data and then further filtering it to elderly insights we got elderly_specific_data.***
"""

# prompt: load the file

# Assuming the file is a CSV file
import pandas as pd
df = pd.read_csv('elderly_specific_data.csv')
print(df)

"""***Basic information***"""

# prompt: basic information

df.info()
df.describe()

"""***Distribution by country***"""

# Explore the distribution of a specific column (replace 'column_name' with the actual column name)
column_name = 'country'  # Replace with the actual column name you want to explore
print(f"\nDistribution of {column_name}:")
df[column_name].value_counts()

"""***Descriptive statistics for numerical columns***"""

# Descriptive statistics for numerical columns
print("\nDescriptive Statistics:")
print(df.describe())

"""***Check for missing values in the dataset***"""

# Check for missing values in the dataset
print("\nMissing Values:")
df.isnull().sum()

"""***Calculate and display the correlation matrix***"""

# Calculate and display the correlation matrix
# Select only numeric columns for correlation calculation
numeric_df = df.select_dtypes(include=['number'])
correlation_matrix = numeric_df.corr()

print("\nCorrelation Matrix:")
print(correlation_matrix)

import matplotlib.pyplot as plt
import seaborn as sns

# Select only numeric columns for correlation calculation
numeric_df = df.select_dtypes(include=['number'])

# Calculate the correlation matrix
correlation_matrix = numeric_df.corr()

# Set up the matplotlib figure
plt.figure(figsize=(14, 10))

# Create a heatmap to visualize the correlation matrix
sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap="coolwarm", linewidths=0.5, square=True)

# Add a title
plt.title('Correlation Matrix Heatmap', fontsize=18)

# Show the plot
plt.show()

"""***Calculate the composite score using the first principal component***"""

from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

# Selecting only the numeric columns for PCA, excluding 'country' and 'Year'
numeric_features = df.drop(columns=['country', 'Year'])

# Normalizing the data using StandardScaler
scaler = StandardScaler()
scaled_data = scaler.fit_transform(numeric_features)

# Applying PCA
pca = PCA()
pca.fit(scaled_data)

# Getting the explained variance and the PCA components (loadings)
explained_variance = pca.explained_variance_ratio_
loadings = pca.components_

# Display the explained variance and the loadings for the first few components
explained_variance, loadings[:3]  # Displaying loadings for the first 3 components for brevity

# Calculate the composite score using the first principal component
composite_scores = pca.transform(scaled_data)[:, 0]  # First principal component scores

# Add the composite score to the original dataframe
df['composite_score'] = composite_scores

# Display the updated dataframe with the composite score to the user
print(df.head())  # To display the first few rows of the dataframe

"""***Predict the composite score for 2022 to 2030 using linear regression.***


"""

# Recalculate the composite score using PCA as before
import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression

# Selecting only the numeric columns for PCA, excluding 'country' and 'Year'
numeric_features = df.drop(columns=['country', 'Year'])

# Normalizing the data using StandardScaler
scaler = StandardScaler()
scaled_data = scaler.fit_transform(numeric_features)

# Applying PCA
pca = PCA()
pca.fit(scaled_data)

# Calculate the composite score using the first principal component
composite_scores = pca.transform(scaled_data)[:, 0]  # First principal component scores

# Add the composite score to the original dataframe
df['composite_score'] = composite_scores

# Now proceed with predicting for 2022-2030 for India

# Filter India's data with the composite score
india_data = df[df['country'] == 'India'][['Year', 'composite_score']]

# Prepare the data for regression (only the available years and composite scores)
india_years = india_data['Year'].values.reshape(-1, 1)
india_scores = india_data['composite_score'].values

# Fit a linear regression model
model = LinearRegression()
model.fit(india_years, india_scores)

# Predict the composite scores for the years 2022 to 2030
future_years = np.array(range(2022, 2031)).reshape(-1, 1)
predicted_scores = model.predict(future_years)

# Create a dataframe for the predicted years and scores
predicted_data = pd.DataFrame({
    'country': 'India',
    'Year': future_years.flatten(),
    'composite_score': predicted_scores
})

# Append the predicted data to the original data for India
india_extended_data = pd.concat([india_data, predicted_data])

# Display the first few rows of the extended dataset with the predicted composite scores for India
india_extended_data.tail(15)  # Displaying the last 15 rows, including predictions for 2022 to 2030

from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Make predictions on the historical data (up to 2021) for India
historical_predictions = model.predict(india_years)

# Calculate accuracy metrics
mae = mean_absolute_error(india_scores, historical_predictions)
mse = mean_squared_error(india_scores, historical_predictions)
r2 = r2_score(india_scores, historical_predictions)

# Display the accuracy metrics
mae, mse, r2

# Get the list of unique countries in the dataset
countries = df['country'].unique()

# Create a dictionary to store accuracy metrics for each country
accuracy_metrics = {}

# Loop through each country, fit a linear regression model, and calculate accuracy metrics
for country in countries:
    country_data = df[df['country'] == country][['Year', 'composite_score']].dropna()

    if len(country_data) > 1:  # Ensure there is enough data for fitting
        years = country_data['Year'].values.reshape(-1, 1)
        scores = country_data['composite_score'].values

        # Fit the linear regression model
        model = LinearRegression()
        model.fit(years, scores)

        # Make predictions on the historical data
        predictions = model.predict(years)

        # Calculate accuracy metrics
        mae = mean_absolute_error(scores, predictions)
        mse = mean_squared_error(scores, predictions)
        r2 = r2_score(scores, predictions)

        # Store the metrics in the dictionary
        accuracy_metrics[country] = {'MAE': mae, 'MSE': mse, 'R²': r2}

# Convert the accuracy metrics to a DataFrame for easy viewing
accuracy_df = pd.DataFrame(accuracy_metrics).T

# Display the accuracy metrics DataFrame for all countries directly
accuracy_df.head()  # Display the first few rows of the accuracy metrics for all countries

# We already have predicted values for India until 2030. Let's now extend predictions for all countries until 2030.
# Create a dictionary to store the extended data for each country
extended_data = []

# Loop through each country, fit a linear regression model, and predict scores up to 2030
for country in countries:
    country_data = df[df['country'] == country][['Year', 'composite_score']].dropna()

    if len(country_data) > 1:  # Ensure there is enough data for fitting
        years = country_data['Year'].values.reshape(-1, 1)
        scores = country_data['composite_score'].values

        # Fit the linear regression model
        model = LinearRegression()
        model.fit(years, scores)

        # Predict the composite scores for the years 2022 to 2030
        future_years = np.array(range(2022, 2031)).reshape(-1, 1)
        predicted_scores = model.predict(future_years)

        # Create a dataframe for the predicted years and scores
        predicted_data = pd.DataFrame({
            'country': country,
            'Year': future_years.flatten(),
            'composite_score': predicted_scores
        })

        # Append the predicted data to the extended dataset
        extended_data.append(pd.concat([country_data, predicted_data]))

# Combine all the extended data into a single dataframe
extended_df = pd.concat(extended_data)

# Display the extended dataframe with the predicted composite scores till 2030 directly
extended_df.head(30)  # Display the first 20 rows of the extended data

"""***Visualizations for composite score for all countries , linear regression model***"""

import plotly.express as px

# Create an interactive plot with a dropdown to select the country
fig = px.line(extended_df, x='Year', y='composite_score', color='country',
              title='Composite Score Trends (2000 - 2030)',
              labels={'composite_score': 'Composite Score'},
              hover_name='country')

# Update the layout for better interaction
fig.update_layout(
    xaxis_title='Year',
    yaxis_title='Composite Score',
    legend_title_text='Country',
    hovermode='closest'
)

# Display the interactive plot
fig.show()

"""***Visualization for top 10 countries using linear regression***"""

import pandas as pd
import plotly.express as px

def display_ranked_countries(year):
    # Filter and rank the data for the specified year
    filtered_data = extended_df[extended_df['Year'] == year]
    ranked_data = filtered_data.sort_values(by='composite_score', ascending=False).head(10)

    # Create the bar chart
    fig = px.bar(ranked_data, x='composite_score', y='country', orientation='h',
                 title=f'Top 10 Countries by Composite Score in {year}',
                 labels={'composite_score': 'Composite Score', 'country': 'Country'})

    # Update layout for better visualization
    fig.update_layout(xaxis_title='Composite Score', yaxis_title='Country', showlegend=False)

    # Show the plot
    fig.show()

# Example: Display the top 10 ranked countries for the year 2020
display_ranked_countries(2021)

"""***Predicting yhat(composite score) and top countries using prophet model 2022-2030***"""

import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt

# Step 1: Load the dataset
df = pd.read_csv('/content/elderly_specific_data.csv')

# Step 2: Normalize each feature individually
from sklearn.preprocessing import MinMaxScaler

scalers = {}
for feature in ['population_60_plus', 'gdp_elderly', 'che_elderly', 'gghed_elderly', 'pvtd_elderly']:
    scaler = MinMaxScaler()
    df[feature] = scaler.fit_transform(df[[feature]])
    scalers[feature] = scaler

# Recalculate the composite score as the sum of normalized features
df['composite_score_scaled'] = df[['population_60_plus', 'gdp_elderly', 'che_elderly', 'gghed_elderly', 'pvtd_elderly']].sum(axis=1)

df['ds'] = pd.to_datetime(df['Year'], format='%Y')

# Step 3: Forecast for Each Country
all_forecasts = []

countries = df['country'].unique()

for country in countries:
    # Filter data for the current country
    df_country = df[df['country'] == country][['ds', 'composite_score_scaled']].rename(columns={'composite_score_scaled': 'y'})

    # Fit the Prophet model
    model = Prophet(yearly_seasonality=True, changepoint_prior_scale=0.1)
    model.fit(df_country)

    # Make future predictions for 2022-2030
    future = model.make_future_dataframe(periods=11, freq='Y')  # Forecast for 2022-2030
    forecast = model.predict(future)

    # Add country column to forecast
    forecast['country'] = country

    # Collect the forecasted values
    all_forecasts.append(forecast[['ds', 'yhat', 'country']])

# Step 4: Combine all forecasts into a single dataframe
combined_forecasts = pd.concat(all_forecasts)

# Step 5: Rank the Top 10 Countries for Each Year
# Filter the data to include only the future predictions (2022-2030)
future_forecasts = combined_forecasts[combined_forecasts['ds'] >= '2022-01-01']

# Group by year and rank the countries by predicted composite scores
future_forecasts['year'] = future_forecasts['ds'].dt.year

# Define a function to rank and display the top 10 countries for each year
def rank_top_countries(year):
    # Filter data for the specified year
    year_data = future_forecasts[future_forecasts['year'] == year]

    # Rank countries by their predicted composite score (yhat)
    ranked_countries = year_data.sort_values(by='yhat', ascending=False).head(10)

    # Display the results
    print(f"Top 10 Countries for {year}:")
    print(ranked_countries[['country', 'yhat']])

# Example: Rank the top 10 countries for 2025
rank_top_countries(2021)

# Optional: You can loop through the years and display the rankings for each year
for year in range(2022, 2031):
    rank_top_countries(year)

"""***Accuracy for the prophet model***"""

from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Calculate accuracy metrics for each country
for country in countries:
    # Filter data for the current country
    df_country = df[df['country'] == country][['ds', 'composite_score_scaled']].rename(columns={'composite_score_scaled': 'y'})

    # Fit the Prophet model (re-fitting for consistency)
    model = Prophet(yearly_seasonality=True, changepoint_prior_scale=0.1)
    model.fit(df_country)

    # Make predictions on the historical data
    df_country_history = model.predict(df_country)

    # Extract actual and predicted values
    y_true = df_country['y'].values
    y_pred = df_country_history['yhat'].values

    # Calculate accuracy metrics
    mae = mean_absolute_error(y_true, y_pred)
    mse = mean_squared_error(y_true, y_pred)
    r2 = r2_score(y_true, y_pred)

    # Print the results
    print(f"Accuracy Metrics for {country}:")
    print(f"MAE: {mae:.4f}")
    print(f"MSE: {mse:.4f}")
    print(f"R²: {r2:.4f}")
    print("-" * 30)

"""***Top 10 countries from 2000 to 2030 using prophet along with yhat***"""

# prompt: print the top 10 countries from 2000 to 2030 as per the prophet model we used

# Filter the data to include only the future predictions (2022-2030)
future_forecasts = combined_forecasts[combined_forecasts['ds'] >= '2000-01-01']

# Group by year and rank the countries by predicted composite scores
future_forecasts['year'] = future_forecasts['ds'].dt.year




# Define a function to rank and display the top 10 countries for each year
def rank_top_countries(year):
    # Filter data for the specified year
    year_data = future_forecasts[future_forecasts['year'] == year]

    # Drop duplicates by country, keeping only the highest predicted composite score
    year_data = year_data.sort_values(by='yhat', ascending=False).drop_duplicates(subset='country')

    # Rank countries by their predicted composite score (yhat)
    ranked_countries = year_data.head(10)

    # Display the results
    print(f"Top 10 Countries for {year}:")
    print(ranked_countries[['country', 'yhat']])

# Loop through the years and display the rankings for each year
for year in range(2000, 2031):
    rank_top_countries(year)

import plotly.graph_objects as go

# Assuming 'combined_forecasts' is your DataFrame from the Prophet model
# with columns 'ds' (datetime), 'yhat' (predicted value), and 'country'

# Filter the data to include only the future predictions (2000-2030)
future_forecasts = combined_forecasts[combined_forecasts['ds'] >= '2000-01-01']
future_forecasts['year'] = future_forecasts['ds'].dt.year

# Create a list of years for the slider
years = list(range(2000, 2031))

# Create a figure
fig = go.Figure()

# Create a bar trace for each year but make them invisible except for the first year (2000)
for year in years:
    year_data = future_forecasts[future_forecasts['year'] == year]
    ranked_countries = year_data.sort_values(by='yhat', ascending=False).head(10)

    # Add bar chart trace for this year
    fig.add_trace(go.Bar(
        x=ranked_countries['yhat'],
        y=ranked_countries['country'],
        orientation='h',
        name=str(year),
        visible=(year == 2000)  # Make only the first year's data visible initially
    ))

# Create steps for the slider
steps = []
for i, year in enumerate(years):
    step = dict(
        method="update",
        args=[{"visible": [False] * len(fig.data)},  # Hide all traces
              {"title": f"Top 10 Countries for expanding Geriatric care services in {year}"}],  # Update title
        label=str(year)
    )
    # Toggle the visibility of the current year's trace
    step["args"][0]["visible"][i] = True
    steps.append(step)

# Create a slider with the steps
sliders = [dict(
    active=0,
    currentvalue={"prefix": "Year: "},
    pad={"t": 50},
    steps=steps
)]

# Update the layout to include the slider
fig.update_layout(
    sliders=sliders,
    title="Top 10 Countries for expanding Geriatric care services in 2000",
    xaxis_title="Predicted Composite Score (yhat)",
    yaxis_title="Country",
    height=600
)

# Show the figure
fig.show()

# prompt: store the top 10  countries from 2000 to 2030 as per the prophet model we used in a csv file as per year

# Create an empty list to store the top 10 countries for each year
top_countries_by_year = []

# Loop through the years 2000 to 2030
for year in range(2000, 2031):
    # Filter data for the current year
    year_data = future_forecasts[future_forecasts['year'] == year]

    # Rank countries by their predicted composite score (yhat)

    def rank_top_countries(year):
        # Filter data for the specified year
        year_data = future_forecasts[future_forecasts['year'] == year]

        # Drop duplicates by country, keeping only the highest predicted composite score
        year_data = year_data.sort_values(by='yhat', ascending=False).drop_duplicates(subset='country')

        ranked_countries = year_data.sort_values(by='yhat', ascending=False).head(10)

        # Store the top 10 countries for the current year
        for _, row in ranked_countries.iterrows():
            top_countries_by_year.append({
                'Year': year,
                'Country': row['country'],
                'Predicted Composite Score': row['yhat']
            })
    # Call the function to rank and store data for the current year
    rank_top_countries(year)

# Create a DataFrame from the collected data
top_countries_df = pd.DataFrame(top_countries_by_year)

# Save the DataFrame to a CSV file
top_countries_df.to_csv('top_10_countries_elderly.csv', index=False)

import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import MinMaxScaler

# Step 1: Load the historical dataset
df = pd.read_csv('/content/elderly_specific_data.csv')

# Step 2: Normalize each feature individually and keep track of the scalers to reverse the transformation later
features_to_normalize = ['population_60_plus', 'gdp_elderly', 'che_elderly', 'gghed_elderly', 'pvtd_elderly']
scalers = {}

for feature in features_to_normalize:
    scaler = MinMaxScaler()
    df[feature] = scaler.fit_transform(df[[feature]])
    scalers[feature] = scaler

# Step 3: Add composite score column
df['composite_score_scaled'] = df[features_to_normalize].sum(axis=1)
df['ds'] = pd.to_datetime(df['Year'], format='%Y')

# Step 4: Load the predicted composite scores for 2022-2030 from Prophet
# Assuming `combined_forecasts` contains the future predictions you have already calculated
# Format it as `ds`, `yhat`, `country`, and `Year`
future_forecasts = combined_forecasts[['ds', 'yhat', 'country']].rename(columns={'yhat': 'predicted_composite_score'})
future_forecasts['Year'] = future_forecasts['ds'].dt.year

# Step 5: Merge historical data with predicted composite scores
df['composite_score_scaled'] = df[features_to_normalize].sum(axis=1)
historical_df = df[['Year', 'country', 'composite_score_scaled'] + features_to_normalize]
future_forecasts.rename(columns={'predicted_composite_score': 'composite_score_scaled'}, inplace=True)

# Combine historical and future composite scores
combined_data = pd.concat([historical_df, future_forecasts], ignore_index=True)

# Step 6: Predict individual features based on composite scores for 2022-2030
predictions = {}

# Loop over each feature, fit a Linear Regression model using composite score, and predict the future values
for feature in features_to_normalize:
    # Use historical data to model the relationship between composite score and the feature
    valid_data = combined_data[['composite_score_scaled', feature]].dropna()

    if len(valid_data) > 1:
        X = valid_data[['composite_score_scaled']]
        y = valid_data[feature]

        # Fit the Linear Regression model
        model = LinearRegression()
        model.fit(X, y)

        # Predict the future values using the predicted composite scores
        future_composite_scores = future_forecasts[['composite_score_scaled']]
        predictions[feature] = model.predict(future_composite_scores)

        # Reverse the scaling to return to the original scale
        predictions[feature] = scalers[feature].inverse_transform(predictions[feature].reshape(-1, 1)).flatten()

        # Add the predicted values to the future_forecasts DataFrame
        future_forecasts[feature] = predictions[feature]

# Step 7: Combine historical data (2000-2021) with predicted data (2022-2030)
final_combined_df = pd.concat([historical_df, future_forecasts], ignore_index=True)

# Display the final dataset with all features and composite scores from 2000 to 2030
print(final_combined_df[['Year', 'country'] + features_to_normalize + ['composite_score_scaled']])

# Combine the actual historical data (2000-2021) and predicted data (2022-2030)
final_combined_df = pd.concat([historical_df, future_forecasts], ignore_index=True)

# Save the combined data to a CSV file
final_combined_df.to_csv("GeriatricPredictions.csv", index=False)

# Provide the path to download the CSV file
print("Final combined data saved to: GeriatricPredictions.csv")