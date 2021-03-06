from pandas import read_csv

sales_data = read_csv('data/data_raw/Sales.csv')
plot_data = sales_data.groupby('Location (Code)')['Sales units'].sum()
plot_data.sort_values()[-10:].plot(kind='bar')
# plot_data.plot(kind='bar')
plt.show()
