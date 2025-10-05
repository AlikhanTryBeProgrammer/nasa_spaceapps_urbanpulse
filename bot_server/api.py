# api.py
from flask import Flask, request, jsonify
import pandas as pd
import numpy as np

app = Flask(__name__)

# --- Данные ---
manual_data = pd.DataFrame({
    "city": [
        "Almaty","Almaty","Almaty","Almaty","Almaty","Almaty","Almaty","Almaty","Almaty","Almaty","Almaty","Almaty",
        "Astana","Astana","Astana","Astana","Astana","Astana","Astana","Astana","Astana","Astana","Astana","Astana",
        "Shymkent", "Shymkent", "Shymkent", "Shymkent", "Shymkent", "Shymkent","Shymkent", "Shymkent", "Shymkent", "Shymkent", "Shymkent","Shymkent"
    ],
    "month": list(range(1,13))*3,
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

# --- Правила для рекомендаций ---
rules = {
    "temp_surface": {
        "too_hot": (lambda x: x > 32, "🌡 Hot → add green roofs, shade, water elements."),
        "too_cold": (lambda x: x < -5, "❄ Very cold → improve insulation.")
    },
    "pm25": {
        "polluted": (lambda x: x > 35, "💨 High PM2.5 → more trees, green barriers.")
    },
    "humidity": {
        "too_dry": (lambda x: x < 30, "💧 Dry → add irrigation, drought-resistant plants."),
        "too_humid": (lambda x: x > 85, "💦 Humid → improve ventilation.")
    },
    "precipitation": {
        "too_low": (lambda x: x < 50, "🌵 Low precipitation → save water."),
        "too_high": (lambda x: x > 200, "🌊 High precipitation → improve drainage.")
    }
}

def get_recommendations_for_row(row):
    recs = []
    for key, rule_set in rules.items():
        for _, (cond, msg) in rule_set.items():
            if cond(row[key]):
                recs.append(msg)
    return recs

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

def analyze(month=None):
    df_selected = manual_data.copy()
    if month is not None:
        df_selected = df_selected[df_selected['month'] == month]
    df_selected['recommendations'] = df_selected.apply(get_recommendations_for_row, axis=1)
    df_selected['health_index'] = df_selected.apply(compute_health_index_row, axis=1)
    return df_selected[['city','month','temp_surface','pm25','humidity','precipitation','health_index','recommendations']].to_dict(orient='records')

@app.route("/analyze", methods=["POST"])
def analyze_month():
    data = request.json
    month = data.get("month")
    try:
        month = int(month)
    except:
        month = None
    results = analyze(month)
    return jsonify({"results": results})  # ✅ Flutter ожидает именно такой формат!

if __name__ == "__main__":
    # Если тестируешь на Android эмуляторе — используй host="0.0.0.0"
    app.run(host="127.0.0.1", port=5000)
