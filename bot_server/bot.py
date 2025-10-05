import time
import pandas as pd
import geopandas as gpd
import folium
import osmnx as ox
from shapely.geometry import Point
import numpy as np
import os


manual_data = pd.DataFrame({
    "city": [
        "Almaty","Almaty","Almaty","Almaty","Almaty","Almaty","Almaty","Almaty","Almaty","Almaty","Almaty","Almaty",
        "Astana","Astana","Astana","Astana","Astana","Astana","Astana","Astana","Astana","Astana","Astana","Astana",
        "Shymkent", "Shymkent", "Shymkent", "Shymkent", "Shymkent", "Shymkent","Shymkent", "Shymkent", "Shymkent", "Shymkent", "Shymkent","Shymkent"
    ],
    "month": [
        1,2,3,4,5,6,7,8,9,10,11,12,
        1,2,3,4,5,6,7,8,9,10,11,12,
        1,2,3,4,5,6,7,8,9,10,11,12
    ],

    "temp_surface": [
        -8.67, -5.92, 1.11, 15.85, 15.63, 26.97, 28.29, 26.04, 19.22, 9.36, 0.79, -4.96,
        -16.0, -16.45, -6.23, 7.64, 11.01, 20.31, 20.74, 18.34, 10.14, 3.58, -6.24, -12.53,
        1.42, 0.26, 6.39, 14.18, 18.51, 27.66, 29.32, 28.57, 20.27, 12.96, 6.68, -1.48
    ],
    "pm25": [
        23.18, 40.34, 54.11, 98.23, 123.13, 118.24, 127.34, 111.96, 85.51, 45.15, 23.47, 14.7,
        22.6, 44.84, 74.65, 86.46, 102.66, 126.32, 113.74, 83.82, 69.45, 40.28, 19.57, 19.12,
        29.06,45.3, 66.17, 104.95, 115.13, 143.89, 135.79, 122.42, 92.97, 59.67, 39.4, 27.89
    ],
    "humidity": [
        1.81, 2.12, 3.02, 6.59, 5.29, 9.33, 9.2, 7.5, 4.43, 4.19, 3.19, 2.15,
        1.15, 1.21, 2.34, 4.76, 5.89, 10.23, 10.59, 8.88, 5.56, 3.73, 2.21, 1.35,
        3.38, 3.12, 4.87, 7.42, 8.7, 8.35, 7.52, 5.77, 3.93, 4.9, 4.19, 2.57
    ],
    "precipitation": [
        0.84, 1.07, 1.13, 0.18, 0.64, 0.83, 0.25, 0.11, 0.05, 0.82, 0.87, 0.46,
        1.14, 1.1, 0.76, 1.15, 2.79, 1.99, 2.63, 2.4, 0.83, 1.44, 1.26, 0.85,
        2.23, 1.94, 3.26, 1.79, 2.21, 0.16, 0.58, 0.02, 0.11, 2.2, 2.09, 1.68
    ]
})

coords = {
    "Almaty": (43.2389, 76.8897),
    "Astana": (51.1694, 71.4491),
    "Shymkent": (42.3167, 69.5958)
}

manual_data["lat"] = manual_data["city"].apply(lambda x: coords[x][0])
manual_data["lon"] = manual_data["city"].apply(lambda x: coords[x][1])

manual_data.head()
manual_data.head()

disaster_data=pd.DataFrame({
    "city": ["Almaty"]*12 + ["Astana"]*12 + ["Shymkent"]*12,
    "month":list(range(1,13))*3,
    "fires":[0,0,0,0,0,0,0,0,0,0,0,0,  0,0,0,0,0,0,0,0,0,0,0,0,  0,0,0,0,0,1,0,0,0,0,0,0],
    "floods":[0,0,0,6,6,0,0,0,7,0,0,0,  0,0,0,0,0,4,0,0,4,0,0,6,  0,6,6,0,0,0,0,0,0,0,0,0],
    "storms":[0,0,0,0,5,5,0,0,5,0,0,0, 0,0,0,3,0,1,0,1,0,0,0,0,  0,0,0,0,1,1,0,0,1,1,0,0 ],
    "earthquakes":[6,2,7,8,7,2,4,3,4,2,3,7,  2,1,2,0,1,1,1,2,1,1,0,2, 2,1,2,0,1,1,1,2,1,1,0,2 ],
})
manual_data=manual_data.merge(disaster_data, on=["city", "month"], how="left")

manual_data.head()
rules = {
    "temp_surface": {
        "too_hot": (
            lambda x: (x is not None) and (not pd.isna(x)) and x > 32,
            "Hot surface → add green roofs, green zones, shade areas, water elements, and plan ventilated spaces."
        ),
        "too_cold": (
            lambda x: (x is not None) and (not pd.isna(x)) and x < -5,
            "Very cold → plan insulation, use reflective coatings, insulate walls and ceilings."
        )
    },
    "pm25": {
        "polluted": (
            lambda x: (x is not None) and (not pd.isna(x)) and x > 35,
            "High PM2.5 → improve transport policy, create green barriers (alleys, shrubs, vertical gardens), and air filtration in buildings."
        )
    },
    "humidity": {
        "too_dry": (
            lambda x: (x is not None) and (not pd.isna(x)) and x < 30,
            "Dry → irrigation, drought-resistant plants."
        ),
        "too_humid": (
            lambda x: (x is not None) and (not pd.isna(x)) and x > 85,
            "Very humid → pay attention to drainage and ventilation."
        )
    },
    "precipitation": {
        "too_low": (
            lambda x: (x is not None) and (not pd.isna(x)) and x < 50,
            "Low precipitation this month → drought risk, plan water-saving strategies."
        ),
        "too_high": (
lambda x: (x is not None) and (not pd.isna(x)) and x > 200,
            "High precipitation this month → ensure drainage, flood protection, and safe urban islands."
        )
    }
}
user_input = input("Enter the month number (1–12) or '0' for annual analysis: ")


try:
    selected_month = int(user_input)
    if selected_month == 0:
        selected_month = None
except:
    selected_month = None


if selected_month is None:

    agg = gdf.groupby('city').agg({
        'temp_surface':'mean',
        'pm25':'mean',
        'humidity':'mean',
        'precipitation':'sum',
        'lat':'first',
        'lon':'first'
    }).reset_index()
    agg['month'] = 'yearly'
    df_selected = agg
    print("Агрегировано по годам (mean по городу).")
else:

    if gdf['month'].dtype == object:
        try:
            df_selected = gdf[gdf['month'].astype(int) == int(selected_month)].copy()
        except Exception:
            df_selected = gdf[gdf['month'].astype(str).str.contains(str(selected_month), na=False)].copy()
    else:
        df_selected = gdf[gdf['month'] == int(selected_month)].copy()

    if df_selected.empty:
        raise ValueError(f"Нет данных для месяца {selected_month}. Проверь Ячейку 3 (month values).")

    df_selected = df_selected[['city','month','temp_surface','pm25','humidity','precipitation','lat','lon','geometry']].copy()
    print(f"Отобрано строк: {len(df_selected)} для месяца {selected_month}.")


if 'geometry' not in df_selected.columns:
    df_selected['geometry'] = gpd.points_from_xy(df_selected['lon'], df_selected['lat'])

df_selected = gpd.GeoDataFrame(df_selected, geometry='geometry', crs="EPSG:4326")
df_selected.head()
df_selected['recommendations'] = df_selected.apply(lambda r: get_recommendations_for_row(r, rules), axis=1)


def compute_health_index_row(row):
    score = 0.0
    t = row.get('temp_surface', np.nan)
    if not pd.isna(t):
        score += max(0, 2.0 - abs(t - 20)/6.0)
    pm = row.get('pm25', np.nan)
    if not pd.isna(pm):
        score -= 0.03 * pm
    h = row.get('humidity', np.nan)
    if not pd.isna(h):
        if h < 40: score -= 0.2
        if h > 80: score -= 0.2
    p = row.get('precipitation', np.nan)
    if not pd.isna(p):

        if p < 20: score -= 0.2
        if p > 200: score -= 0.2
    return score

df_selected['raw_score'] = df_selected.apply(compute_health_index_row, axis=1)
mn = df_selected['raw_score'].min()
mx = df_selected['raw_score'].max()
df_selected['health_index'] = (df_selected['raw_score'] - mn) / (mx - mn + 1e-9)

df_selected[['city','month','temp_surface','pm25','humidity','precipitation','health_index','recommendations']].head(20)
valid = df_selected.dropna(subset=['lat','lon'])
if valid.empty:
    raise ValueError("Нет координат в df_selected — заполни lat/lon для городов.")

center_lat = valid['lat'].mean()
center_lon = valid['lon'].mean()

m = folium.Map(location=[center_lat, center_lon], zoom_start=5, tiles='CartoDB positron')

def color_by_index(v):
    if pd.isna(v): return "#888888"
    if v < 0.2: return "#d73027"
    if v < 0.4: return "#fc8d59"
    if v < 0.6: return "#fee08b"
    if v < 0.8: return "#d9ef8b"
    return "#1a9850"

for _, row in df_selected.iterrows():
    lat = row['lat']; lon = row['lon']
    if pd.isna(lat) or pd.isna(lon):
        continue
    popup = f"<b>{row['city']}</b><br>"
    popup += f"<b>Месяц:</b> {row['month']}<br>"
    popup += f"🌡 Темп: {row['temp_surface']} °C<br>"
    popup += f"💨 PM2.5: {row['pm25']} µg/m³<br>"
    popup += f"💧 Влажность: {row['humidity']}%<br>"
    popup += f"🌧 Осадки: {row['precipitation']}<br>"
    popup += f"<b>Health index:</b> {row['health_index']:.2f}<br><br>"
    popup += "<b>Рекомендации:</b><ul>"
    for r in row['recommendations']:
        popup += f"<li>{r}</li>"
    popup += "</ul>"

    folium.CircleMarker(
        location=[lat, lon],
        radius=8,
        color=color_by_index(row['health_index']),
        fill=True,
        fill_color=color_by_index(row['health_index']),
        fill_opacity=0.9,
        popup=folium.Popup(popup, max_width=420)
).add_to(m)


out_html = "manual_monthly_map.html" if selected_month is not None else "manual_yearly_map.html"
m.save(out_html)
print("Карта сохранена в файл:", out_html)
csv_name = "manual_monthly_results.csv" if selected_month is not None else "manual_yearly_results.csv"
gjson_name = "manual_monthly_results.geojson" if selected_month is not None else "manual_yearly_results.geojson"

df_selected.drop(columns='geometry').to_csv(csv_name, index=False)
df_selected.to_file(gjson_name, driver="GeoJSON")

print("Экспортированы:", csv_name, gjson_name)
csv_name = "manual_monthly_results.csv" if selected_month is not None else "manual_yearly_results.csv"
gjson_name = "manual_monthly_results.geojson" if selected_month is not None else "manual_yearly_results.geojson"

df_selected.drop(columns='geometry').to_csv(csv_name, index=False)
df_selected.to_file(gjson_name, driver="GeoJSON")

print("Экспортированы:", csv_name, gjson_name)
from google.colab import files

files.download(csv_name)
files.download(gjson_name)