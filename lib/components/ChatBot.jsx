import { useState } from "react";

export default function ChatBot() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");

  const sendMessage = () => {
    if (!input) return;
    setMessages([...messages, { text: input, fromUser: true }]);
    setMessages(prev => [...prev, { text: "Спасибо, мы обработаем ваш запрос!", fromUser: false }]);
    setInput("");
  };

  return (
    <div style={{ marginTop: "20px", padding: "20px", border: "1px solid #ddd", borderRadius: "10px", maxWidth: "400px" }}>
      <h3>Чат-бот</h3>
      <div style={{ minHeight: "100px", marginBottom: "10px" }}>
        {messages.map((m, idx) => (
          <div key={idx} style={{ textAlign: m.fromUser ? "right" : "left" }}>
            <span style={{ background: m.fromUser ? "#4CAF50" : "#eee", padding: "5px 10px", borderRadius: "10px", display: "inline-block", margin: "2px 0" }}>
              {m.text}
            </span>
          </div>
        ))}
      </div>
      <input type="text" value={input} onChange={e => setInput(e.target.value)} style={{ width: "70%" }} />
      <button onClick={sendMessage} style={{ width: "28%", marginLeft: "2%" }}>Отправить</button>
    </div>
  );
}
