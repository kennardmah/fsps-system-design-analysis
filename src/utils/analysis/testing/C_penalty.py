import pandas as pd
import matplotlib.pyplot as plt

# Read the data from the CSV file into a DataFrame called 'table'
table = pd.read_csv('src/utils/analysis/testing/robust_strategy_table.csv')

# Group the data by 'capacity'
grouped_data = table.groupby('Capacity')

# Plot the sensitivity analysis visualization
plt.figure(figsize=(8, 6))
# Plot each capacity as a separate line
for capacity, capacity_data in grouped_data:
    plt.plot(capacity_data['C_penalty'], capacity_data['C_total'], marker='o', label=f'Capacity {capacity}')
plt.xlabel('C_penalty')
plt.ylabel('C_total')
plt.title('Sensitivity Analysis')
plt.legend()
plt.grid(True)
plt.show()
