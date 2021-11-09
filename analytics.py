"""Data analysis, create pandas dataframe adn clean data."""
from datetime import datetime
from json import load

import pandas as pd

with open("juejin_articles.json", "r", encoding="utf-8") as file:
    json_data = load(file)

data = []
for key in json_data.keys():
    data += json_data[key]
del json_data

df = pd.DataFrame(data)
del data

df = df[~df.duplicated(subset="article_id")]
df["mtime"] = pd.to_datetime(df['mtime'], unit='s')
df["time_diff"] = (datetime.now() - df["mtime"]).dt.days
# Custom way of counting score
df["score"] = (df["view_count"] * 0.1 +
               df["comment_count"] * 0.2 +
               df["digg_count"] * 0.3 +
               df["collect_count"] * 0.4) / (df["time_diff"] + 2) ** 1.5
