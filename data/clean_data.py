import pandas as pd

# Cargar el archivo stops.txt
path_file = "data/stops.txt"
stops_df = pd.read_csv(path_file, sep=",", encoding="utf-8")

#stops_clean = stops_df[["stop_name", "stop_lat", "stop_lon"]].drop_duplicates(subset="stop_name", keep="first")
stops_clean = stops_df[stops_df["stop_name"].str.isupper() & stops_df["stop_lat"].notnull() & stops_df["stop_lon"].notnull()]

stops_clean.to_csv("data/stops_clean.csv", index=False, encoding="utf-8")
# Mostrar una muestra del resultado
print(stops_clean.head(50))