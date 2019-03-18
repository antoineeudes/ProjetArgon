# ProjetArgon

## Installation
Create the folders `data` and `data/data_raw`:
```
mkdir data
mkdir data/data_raw
```

Move the files Articles.csv, Sales.csv, Stock.csv, Market_Data.csv, Location.csv in the folder `data/data_raw/`,
```
mv /path/to/the/file ./data/data_raw
```

## Cleaning of the dataset

In the file `Articles.csv`, we removed the column(s):
```
Budget Class
```

In the file `Location.csv`, we removed the comumn(s):
```
isWFJactive
```

In the file `Market_Data.csv`, we renamed `Zone` by `Zone (BR Vision)`