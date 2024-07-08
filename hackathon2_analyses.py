# -*- coding: utf-8 -*-
"""Hackathon2/analyses.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1VHZKY_rQXrxrZbgWk6ENfVD5dAU-mgoQ

## **The Objectives: to explore the Weather conditions in Israel and compare them with Global Trends.**

**The Temperature trends and the Precipitation trends were selected for analysis of the weather conditions.**

**Temperature Trends Analyses.**

From NASA's GISTEMP retrieved data for temperature anomalies Globaly, from  Israel Meteorological Service (IMS) retrieved data with average temperature yearly and using the whole period (1951-2023) as a baseline transformed the Israely data to average yearly temperature anomalies, joined two data saved it as a csv file.
For comparing Israely and Global trends used 3 different methods (Polynomial Trend, LOESS Trend, Rolling Mean) to define the trend lines and analyse them in order to find the most relevant.
"""

import pandas as pd
import numpy as np
import plotly.graph_objects as go
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
from statsmodels.nonparametric.smoothers_lowess import lowess

# Load the data
data = pd.read_csv('/content/temperature_data.csv')

data['Year'] = pd.to_datetime(data['Year'], format='%Y')

# Polynomial Regression
degree = 3  # Change the degree for different polynomial fits
israel_poly_coeff = np.polyfit(data['Year'].dt.year, data['Israel Anomaly'], degree)
global_poly_coeff = np.polyfit(data['Year'].dt.year, data['Global Anomaly'], degree)

data['Israel_Poly_Trend'] = np.polyval(israel_poly_coeff, data['Year'].dt.year)
data['Global_Poly_Trend'] = np.polyval(global_poly_coeff, data['Year'].dt.year)

# LOESS Smoothing
israel_loess = lowess(data['Israel Anomaly'], data['Year'].dt.year, frac=0.1)
global_loess = lowess(data['Global Anomaly'], data['Year'].dt.year, frac=0.1)

data['Israel_Loess_Trend'] = np.array([x[1] for x in israel_loess])
data['Global_Loess_Trend'] = np.array([x[1] for x in global_loess])

# Rolling Statistics
window = 10
data['Israel_Rolling_Mean'] = data['Israel Anomaly'].rolling(window=window).mean()
data['Global_Rolling_Mean'] = data['Global Anomaly'].rolling(window=window).mean()
data['Israel_Rolling_Std'] = data['Israel Anomaly'].rolling(window=window).std()
data['Global_Rolling_Std'] = data['Global Anomaly'].rolling(window=window).std()

# Define a function to calculate metrics
def evaluate_model(true_values, predicted_values):
    r2 = r2_score(true_values, predicted_values)
    mae = mean_absolute_error(true_values, predicted_values)
    rmse = np.sqrt(mean_squared_error(true_values, predicted_values))
    return r2, mae, rmse

# Evaluate Polynomial Regression
israel_poly_metrics = evaluate_model(data['Israel Anomaly'], data['Israel_Poly_Trend'])
global_poly_metrics = evaluate_model(data['Global Anomaly'], data['Global_Poly_Trend'])

# Evaluate LOESS Smoothing
israel_loess_metrics = evaluate_model(data['Israel Anomaly'], data['Israel_Loess_Trend'])
global_loess_metrics = evaluate_model(data['Global Anomaly'], data['Global_Loess_Trend'])

# Align series for Rolling Mean evaluation
rolling_mean_df = data[['Israel Anomaly', 'Israel_Rolling_Mean', 'Global Anomaly', 'Global_Rolling_Mean']].dropna()
israel_rolling_metrics = evaluate_model(rolling_mean_df['Israel Anomaly'], rolling_mean_df['Israel_Rolling_Mean'])
global_rolling_metrics = evaluate_model(rolling_mean_df['Global Anomaly'], rolling_mean_df['Global_Rolling_Mean'])

# Print the results
print("Israel Polynomial Regression Metrics: R2 = {:.3f}, MAE = {:.3f}, RMSE = {:.3f}".format(*israel_poly_metrics))
print("Global Polynomial Regression Metrics: R2 = {:.3f}, MAE = {:.3f}, RMSE = {:.3f}".format(*global_poly_metrics))
print("Israel LOESS Metrics: R2 = {:.3f}, MAE = {:.3f}, RMSE = {:.3f}".format(*israel_loess_metrics))
print("Global LOESS Metrics: R2 = {:.3f}, MAE = {:.3f}, RMSE = {:.3f}".format(*global_loess_metrics))
print("Israel Rolling Mean Metrics: R2 = {:.3f}, MAE = {:.3f}, RMSE = {:.3f}".format(*israel_rolling_metrics))
print("Global Rolling Mean Metrics: R2 = {:.3f}, MAE = {:.3f}, RMSE = {:.3f}".format(*global_rolling_metrics))

# Create the visualization
fig = go.Figure()

# Add Israel data
fig.add_trace(go.Scatter(x=data['Year'], y=data['Israel Anomaly'], mode='lines', name='Israel Anomaly'))
fig.add_trace(go.Scatter(x=data['Year'], y=data['Israel_Poly_Trend'], mode='lines', name='Israel Polynomial Trend', line=dict(dash='dash')))
fig.add_trace(go.Scatter(x=data['Year'], y=data['Israel_Loess_Trend'], mode='lines', name='Israel LOESS Trend', line=dict(dash='dot')))
fig.add_trace(go.Scatter(x=data['Year'], y=data['Israel_Rolling_Mean'], mode='lines', name='Israel Rolling Mean', line=dict(dash='dashdot')))

# Add Global data
fig.add_trace(go.Scatter(x=data['Year'], y=data['Global Anomaly'], mode='lines', name='Global Anomaly'))
fig.add_trace(go.Scatter(x=data['Year'], y=data['Global_Poly_Trend'], mode='lines', name='Global Polynomial Trend', line=dict(dash='dash')))
fig.add_trace(go.Scatter(x=data['Year'], y=data['Global_Loess_Trend'], mode='lines', name='Global LOESS Trend', line=dict(dash='dot')))
fig.add_trace(go.Scatter(x=data['Year'], y=data['Global_Rolling_Mean'], mode='lines', name='Global Rolling Mean', line=dict(dash='dashdot')))

# Update layout
fig.update_layout(
    title='Temperature Anomalies: Israel vs. Global',
    xaxis_title='Year',
    yaxis_title='Temperature Anomaly (°C)',
    legend_title='Legend',
    template='plotly'
)

fig.show()

"""As the result of using R2, MAE and RMSE metriks the most statistically correct trend given by LOESS Smoothing. Make the Result Plot"""

import pandas as pd
import numpy as np
import plotly.graph_objects as go
from statsmodels.nonparametric.smoothers_lowess import lowess

# Load the data
data = pd.read_csv('/content/temperature_data.csv')

data['Year'] = pd.to_datetime(data['Year'], format='%Y')

# LOESS Smoothing
israel_loess = lowess(data['Israel Anomaly'], data['Year'].dt.year, frac=0.1)
global_loess = lowess(data['Global Anomaly'], data['Year'].dt.year, frac=0.1)

data['Israel_Loess_Trend'] = np.array([x[1] for x in israel_loess])
data['Global_Loess_Trend'] = np.array([x[1] for x in global_loess])

# Create the visualization
fig = go.Figure()

# Add Israel data
fig.add_trace(go.Scatter(x=data['Year'], y=data['Israel Anomaly'], mode='lines', name='Israel Anomaly'))
fig.add_trace(go.Scatter(x=data['Year'], y=data['Israel_Loess_Trend'], mode='lines', name='Israel LOESS Trend', line=dict(dash='dot')))

# Add Global data
fig.add_trace(go.Scatter(x=data['Year'], y=data['Global Anomaly'], mode='lines', name='Global Anomaly'))
fig.add_trace(go.Scatter(x=data['Year'], y=data['Global_Loess_Trend'], mode='lines', name='Global LOESS Trend', line=dict(dash='dot')))

# Update layout
fig.update_layout(
    title='Temperature Anomalies: Israel vs. Global with LOESS Trends',
    xaxis_title='Year',
    yaxis_title='Temperature Anomaly (°C)',
    legend_title='Legend',
    template='plotly'
)

fig.show()

"""**Conclusion:** till 1983 year the temperature in Israel decreased instead of increasing Global trend, then till 2012 was growing with the rate higher than Global and after 2012 trends are similar slightly growing.

**Precipitation Analysis**

Retrieved the Precipitation Data from Worldbank, dropped irrelevant period of time, saved as csv
"""

import pandas as pd

# Load the CSV file
file_path = '/content/Precipitation_global_1950-2022_mean_historical_cru_ts4.07_mean (1).xlsx - all.csv'
df = pd.read_csv(file_path)

# Step 1: Drop -07 from the column names
df.columns = [col.replace('-07', '') if '-07' in col else col for col in df.columns]

# Step 2: Calculate mean Precipitation for every year and add as a new row
year_columns = df.columns[2:]  # Skip 'code' and 'name' columns
global_avg_precipitation = df[year_columns].mean()

# Add the 'Global Average Precipitation' row to the DataFrame
df.loc['Global Average Precipitation'] = [None, 'Global Average Precipitation'] + list(global_avg_precipitation)

# Step 3: Extract Israel data and add as a new row
israel_precipitation = df[df['name'] == 'Israel'][year_columns].values.flatten()

# Ensure that Israel data is found
if israel_precipitation.size == 0:
    raise ValueError("No data found for Israel in the 'name' column")

# Add the 'Israel Precipitation' row to the DataFrame
df.loc['Israel Precipitation'] = [None, 'Israel Precipitation'] + list(israel_precipitation)

# Step 4: Prepare the final DataFrame with 'year', 'Global Average Precipitation', and 'Israel Precipitation'
final_df = pd.DataFrame({
    'year': year_columns,
    'Global Average Precipitation': df.loc['Global Average Precipitation', year_columns].values,
    'Israel Precipitation': df.loc['Israel Precipitation', year_columns].values
})

# Save to a new CSV file
output_file_path = '/content/Precipitation_analysis.csv'
final_df.to_csv(output_file_path, index=False)

print(f"File saved to {output_file_path}")

"""For comparing Israely and Global trends used 3 different methods to define the trend lines and analyse them in order to find the most relevant."""

import pandas as pd
import numpy as np
import plotly.graph_objects as go
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
from statsmodels.nonparametric.smoothers_lowess import lowess

# Load the data
data = pd.read_csv('/content/Precipitation_analysis.csv')

# Convert the 'year' column to datetime
data['year'] = pd.to_datetime(data['year'], format='%Y')

# Polynomial Regression
degree = 3  # Change the degree for different polynomial fits
israel_poly_coeff = np.polyfit(data['year'].dt.year, data['Israel Precipitation'], degree)
global_poly_coeff = np.polyfit(data['year'].dt.year, data['Global Average Precipitation'], degree)

data['Israel_Poly_Trend'] = np.polyval(israel_poly_coeff, data['year'].dt.year)
data['Global_Poly_Trend'] = np.polyval(global_poly_coeff, data['year'].dt.year)

# LOESS Smoothing
israel_loess = lowess(data['Israel Precipitation'], data['year'].dt.year, frac=0.1)
global_loess = lowess(data['Global Average Precipitation'], data['year'].dt.year, frac=0.1)

data['Israel_Loess_Trend'] = np.array([x[1] for x in israel_loess])
data['Global_Loess_Trend'] = np.array([x[1] for x in global_loess])

# Rolling Statistics
window = 10
data['Israel_Rolling_Mean'] = data['Israel Precipitation'].rolling(window=window).mean()
data['Global_Rolling_Mean'] = data['Global Average Precipitation'].rolling(window=window).mean()
data['Israel_Rolling_Std'] = data['Israel Precipitation'].rolling(window=window).std()
data['Global_Rolling_Std'] = data['Global Average Precipitation'].rolling(window=window).std()

# Define a function to calculate metrics
def evaluate_model(true_values, predicted_values):
    r2 = r2_score(true_values, predicted_values)
    mae = mean_absolute_error(true_values, predicted_values)
    rmse = np.sqrt(mean_squared_error(true_values, predicted_values))
    return r2, mae, rmse

# Evaluate Polynomial Regression
israel_poly_metrics = evaluate_model(data['Israel Precipitation'], data['Israel_Poly_Trend'])
global_poly_metrics = evaluate_model(data['Global Average Precipitation'], data['Global_Poly_Trend'])

# Evaluate LOESS Smoothing
israel_loess_metrics = evaluate_model(data['Israel Precipitation'], data['Israel_Loess_Trend'])
global_loess_metrics = evaluate_model(data['Global Average Precipitation'], data['Global_Loess_Trend'])

# Align series for Rolling Mean evaluation
rolling_mean_df = data[['Israel Precipitation', 'Israel_Rolling_Mean', 'Global Average Precipitation', 'Global_Rolling_Mean']].dropna()
israel_rolling_metrics = evaluate_model(rolling_mean_df['Israel Precipitation'], rolling_mean_df['Israel_Rolling_Mean'])
global_rolling_metrics = evaluate_model(rolling_mean_df['Global Average Precipitation'], rolling_mean_df['Global_Rolling_Mean'])

# Print the results
print("Israel Polynomial Regression Metrics: R2 = {:.3f}, MAE = {:.3f}, RMSE = {:.3f}".format(*israel_poly_metrics))
print("Global Polynomial Regression Metrics: R2 = {:.3f}, MAE = {:.3f}, RMSE = {:.3f}".format(*global_poly_metrics))
print("Israel LOESS Metrics: R2 = {:.3f}, MAE = {:.3f}, RMSE = {:.3f}".format(*israel_loess_metrics))
print("Global LOESS Metrics: R2 = {:.3f}, MAE = {:.3f}, RMSE = {:.3f}".format(*global_loess_metrics))
print("Israel Rolling Mean Metrics: R2 = {:.3f}, MAE = {:.3f}, RMSE = {:.3f}".format(*israel_rolling_metrics))
print("Global Rolling Mean Metrics: R2 = {:.3f}, MAE = {:.3f}, RMSE = {:.3f}".format(*global_rolling_metrics))

# Create the visualization
fig = go.Figure()

# Add Israel data
fig.add_trace(go.Scatter(x=data['year'], y=data['Israel Precipitation'], mode='lines', name='Israel Precipitation'))
fig.add_trace(go.Scatter(x=data['year'], y=data['Israel_Poly_Trend'], mode='lines', name='Israel Polynomial Trend', line=dict(dash='dash')))
fig.add_trace(go.Scatter(x=data['year'], y=data['Israel_Loess_Trend'], mode='lines', name='Israel LOESS Trend', line=dict(dash='dot')))
fig.add_trace(go.Scatter(x=data['year'], y=data['Israel_Rolling_Mean'], mode='lines', name='Israel Rolling Mean', line=dict(dash='dashdot')))

# Add Global data
fig.add_trace(go.Scatter(x=data['year'], y=data['Global Average Precipitation'], mode='lines', name='Global Average Precipitation'))
fig.add_trace(go.Scatter(x=data['year'], y=data['Global_Poly_Trend'], mode='lines', name='Global Polynomial Trend', line=dict(dash='dash')))
fig.add_trace(go.Scatter(x=data['year'], y=data['Global_Loess_Trend'], mode='lines', name='Global LOESS Trend', line=dict(dash='dot')))
fig.add_trace(go.Scatter(x=data['year'], y=data['Global_Rolling_Mean'], mode='lines', name='Global Rolling Mean', line=dict(dash='dashdot')))

# Update layout
fig.update_layout(
    title='Precipitation: Israel vs. Global (1950-2022)',
    xaxis_title='Year',
    yaxis_title='Precipitation (mm)',
    legend_title='Legend',
    template='plotly'
)

fig.show()

"""The best result demonstrated by LOESS Smoothing. Make the Result Plot"""

import pandas as pd
import numpy as np
import plotly.graph_objects as go
from statsmodels.nonparametric.smoothers_lowess import lowess

# Load the data
data = pd.read_csv('/content/Precipitation_analysis.csv')

# Convert the 'year' column to datetime
data['year'] = pd.to_datetime(data['year'], format='%Y')

# LOESS Smoothing
israel_loess = lowess(data['Israel Precipitation'], data['year'].dt.year, frac=0.1)
global_loess = lowess(data['Global Average Precipitation'], data['year'].dt.year, frac=0.1)

data['Israel_Loess_Trend'] = np.array([x[1] for x in israel_loess])
data['Global_Loess_Trend'] = np.array([x[1] for x in global_loess])

# Create the visualization
fig = go.Figure()

# Add Israel data
fig.add_trace(go.Scatter(x=data['year'], y=data['Israel Precipitation'], mode='lines', name='Israel Precipitation'))
fig.add_trace(go.Scatter(x=data['year'], y=data['Israel_Loess_Trend'], mode='lines', name='Israel LOESS Trend', line=dict(dash='dot')))

# Add Global data
fig.add_trace(go.Scatter(x=data['year'], y=data['Global Average Precipitation'], mode='lines', name='Global Average Precipitation'))
fig.add_trace(go.Scatter(x=data['year'], y=data['Global_Loess_Trend'], mode='lines', name='Global LOESS Trend', line=dict(dash='dot')))

# Update layout
fig.update_layout(
    title='Precipitation Trends: Israel vs. Global with LOESS Trends (1950-2022)',
    xaxis_title='Year',
    yaxis_title='Precipitation (mm)',
    legend_title='Legend',
    template='plotly'
)

fig.show()

"""**Conclusion:** In the world precipitation gained the maximum in 2010 and stabilised after the small dropping. In Israel after the declining trend from 1992 to 2008 we can observe a growing trend.

**Total conclusiot:** in Israel, things aren't so bad
"""

