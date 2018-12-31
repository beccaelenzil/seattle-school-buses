# view most recent bus data table

import pandas as pd

df = pd.read_pickle("bus_data.pk1")
print(df)
