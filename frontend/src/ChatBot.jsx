import React, { useState } from 'react';
import axios from 'axios';

const ChatBot = () => {
  const [userId, setUserId] = useState("femi@example.com"); // simulate unique ID per customer
  const [message, setMessage] = useState("");
  const [chatLog, setChatLog] = useState([]);

  const sendMessage = async () => {
    if (!message.trim()) return;

    const userMessage = { role: "user", content: message };
    setChatLog([...chatLog, userMessage]);
    setMessage("");

    try {
      const res = await axios.post("http://localhost:8000/chat", {
        user_id: userId,
        message
      });

      const botMessage = { role: "assistant", content: res.data.response };
      setChatLog(prev => [...prev, botMessage]);

    } catch (error) {
      setChatLog(prev => [...prev, {
        role: "assistant",
        content: "Error: " + (error?.response?.data?.error || error.message)
      }]);
    }
  };

  return (
    <div style={{ maxWidth: 500, margin: "auto", padding: 20 }}>
      <h2>Customer Support Chat</h2>
      <div style={{ border: "1px solid #ccc", padding: 10, minHeight: 200 }}>
        {chatLog.map((msg, i) => (
          <div key={i} style={{ textAlign: msg.role === "user" ? "right" : "left" }}>
            <p><strong>{msg.role === "user" ? "You" : "AI"}:</strong> {msg.content}</p>
          </div>
        ))}
      </div>

      <div style={{ marginTop: 10 }}>
        <input
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder="Type a message..."
          style={{ width: "80%" }}
        />
        <button onClick={sendMessage}>Send</button>
      </div>
    </div>
  );
};

export default ChatBot;
