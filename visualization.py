import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from preprocessing import data

# Assuming 'data' is the DataFrame that contains your preprocessed data

# 1. Line plot for Annual Inflation Rate over the years
plt.figure(figsize=(10, 6))
plt.plot(data['year'], data['annual_inflation_rate'], marker='o', color='b', label='Annual Inflation Rate')
plt.title('Annual Inflation Rate Over the Years')
plt.xlabel('Year')
plt.ylabel('Annual Inflation Rate (%)')
plt.grid(True)
plt.legend()
plt.show()

# 2. Cumulative Inflation Rate plot
plt.figure(figsize=(10, 6))
plt.plot(data['year'], data['cumulative_inflation_rate'], marker='s', color='g', label='Cumulative Inflation Rate')
plt.title('Cumulative Inflation Rate Over the Years')
plt.xlabel('Year')
plt.ylabel('Cumulative Inflation Rate (%)')
plt.grid(True)
plt.legend()
plt.show()

# 3. Plot Inflation for Future
plt.figure(figsize=(10, 6))
plt.plot(data['year'], data['inflation_for_future'], marker='^', color='r', label='Inflation for Future (%)')
plt.title('Inflation for Future Over the Years')
plt.xlabel('Year')
plt.ylabel('Inflation for Future (%)')
plt.grid(True)
plt.legend()
plt.show()

# 4. Correlation Heatmap to analyze relationships between variables
correlation_matrix = data[['annual_inflation_rate', 'cumulative_inflation_rate', 'avg_cpi_present', 'inflation_for_future']].corr()

plt.figure(figsize=(8, 6))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5)
plt.title('Correlation Heatmap')
plt.show()

# 5. Histogram of Inflation for Future to check the distribution
plt.figure(figsize=(10, 6))
sns.histplot(data['inflation_for_future'], bins=20, kde=True, color='purple')
plt.title('Distribution of Inflation for Future')
plt.xlabel('Inflation for Future (%)')
plt.ylabel('Frequency')
plt.show()
