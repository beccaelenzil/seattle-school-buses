# view most recent bus data table

import pandas as pd

df = pd.read_pickle("current_bus_data.pk1")
print(df)
