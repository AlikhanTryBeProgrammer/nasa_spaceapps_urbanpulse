import { useEffect, useState } from "react";
import { MapContainer, TileLayer, GeoJSON } from "react-leaflet";
import { getCityHealth } from "../api/health";
import "leaflet/dist/leaflet.css";

export default function MapView() {
  const [data, setData] = useState(null);

  useEffect(() => {
    getCityHealth().then(res => {
      const geojson = {
        type: "FeatureCollection",
        features: res.features.map(f => ({
          type: "Feature",
          properties: { name: f.name, ndvi: f.ndvi },
          geometry: { type: "Polygon", coordinates: [f.coords] }
        }))
      };
      setData(geojson);
    });
  }, []);

  const style = feature => {
    const ndvi = feature.properties.ndvi;
    let color = ndvi > 0.6 ? "#4CAF50" : ndvi > 0.4 ? "#FFC107" : "#F44336";
    return { color, weight: 2, fillOpacity: 0.5 };
  };

  return (
    <div className="map-container" style={{ height: "500px", borderRadius: "10px", overflow: "hidden", boxShadow: "0 0 10px rgba(0,0,0,0.2)" }}>
      <MapContainer center={[55.75, 37.62]} zoom={12} style={{ height: "100%", width: "100%" }}>
        <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
        {data && <GeoJSON data={data} style={style} />}
      </MapContainer>
    </div>
  );
}
