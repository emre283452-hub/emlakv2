import React, { useState } from "react";

function App() {
  const [form, setForm] = useState({
    area: "",
    room_count: "",
    building_age: "",
    city: ""
  });
  const [result, setResult] = useState(null);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setResult(null);
    const res = await fetch("http://localhost:5000/api/value", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(form)
    });
    const data = await res.json();
    setResult(data.estimated_value);
  };

  return (
    <div style={{ maxWidth: 400, margin: "2rem auto", fontFamily: "Arial" }}>
      <h2>Emlak Değerleme</h2>
      <form onSubmit={handleSubmit}>
        <label>
          Şehir:
          <input type="text" name="city" value={form.city} onChange={handleChange} required />
        </label>
        <br />
        <label>
          Metrekare:
          <input type="number" name="area" value={form.area} onChange={handleChange} required />
        </label>
        <br />
        <label>
          Oda Sayısı:
          <input type="number" name="room_count" value={form.room_count} onChange={handleChange} required />
        </label>
        <br />
        <label>
          Bina Yaşı:
          <input type="number" name="building_age" value={form.building_age} onChange={handleChange} required />
        </label>
        <br />
        <button type="submit">Değerle</button>
      </form>
      {result && (
        <div style={{ marginTop: 20, fontWeight: "bold" }}>
          Tahmini Değer: {result.toLocaleString("tr-TR")} TL
        </div>
      )}
    </div>
  );
}

export default App;