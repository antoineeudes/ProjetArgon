import pandas as pd

def clean_articles():
    articles = pd.read_csv('../data/data_raw/Articles.csv')
    articles = articles.drop(columns="Budget Class")
    articles.to_csv("../data/data_cleaned/Articles.csv", index=False, encoding='utf8')