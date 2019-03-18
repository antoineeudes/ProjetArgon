from pandas import read_csv
from matplotlib import pyplot as plt

sales_data = read_csv('data/Sales.csv')
plot_data = sales_data.groupby('Location (Code)')['Sales units'].sum()
plot_data.sort_values()[-10:].plot(kind='bar')
# plot_data.plot(kind='bar')
plt.show()
