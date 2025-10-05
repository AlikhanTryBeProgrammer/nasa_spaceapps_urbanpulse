export default function Recommendations() {
  const tips = [
    "Сажайте деревья в районах с низким NDVI",
    "Избегайте прогулок в районах с высоким PM2.5",
    "Организуйте парки и зоны отдыха"
  ];

  return (
    <div className="recommendations" style={{ padding: "20px", borderRadius: "10px", background: "#f5f5f5", boxShadow: "0 0 10px rgba(0,0,0,0.1)" }}>
      <h2>Рекомендации</h2>
      <ul>
        {tips.map((tip, idx) => <li key={idx}>• {tip}</li>)}
      </ul>
    </div>
  );
}
