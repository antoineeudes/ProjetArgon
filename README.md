# ProjetArgon

## Installation
Create the folders `data/` and `data/data_raw/`:
```
mkdir data
mkdir data/data_raw
```

Move the files Articles.csv, Sales.csv, Stock.csv, Market_Data.csv, Location.csv in the folder `data/data_raw/`,
```
mv /path/to/the/file ./data/data_raw/
```

### Cleaning of the dataset

Clean the dataset by running :
```
cd data_cleaning
python main.py
```

#### Operations made on the raw dataset
In the file `Articles.csv`, we removed the column(s):
```
Budget Class
```

In the file `Location.csv`, we removed the comumn(s):
```
isWFJactive
```

In the file `Stock.csv`, we replaced `Zone (BR Vision)` by `Zone`

In the file `Stocks.csv`, we replaced `ITEM_CODE` by `Item_Code`.

In all the files, we removes spaces and parentheses from the column names.

### Making joins
Once data are cleaned, make all joins by running :
```
python make_joins.py
```
