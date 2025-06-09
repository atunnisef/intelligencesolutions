import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';

const ChatWidget = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [userId] = useState("customer-123@example.com"); // This can be passed in
  const [message, setMessage] = useState("");
  const [chatLog, setChatLog] = useState([]);
  const chatContainerRef = useRef(null);

  const toggleChat = () => setIsOpen(!isOpen);

  const sendMessage = async () => {
    if (!message.trim()) return;

    const userMsg = { role: "user", content: message };
    setChatLog(prev => [...prev, userMsg]);
    setMessage("");

    try {
      const res = await axios.post("http://localhost:8000/chat", {
        user_id: userId,
        message
      });

      const botMsg = { role: "assistant", content: res.data.response };
      setChatLog(prev => [...prev, botMsg]);
    } catch (err) {
      setChatLog(prev => [...prev, {
        role: "assistant",
        content: "Something went wrong. Try again later."
      }]);
    }
  };

  useEffect(() => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
    }
  }, [chatLog]);

  return (
    <>
      {/* Floating button */}
      <div style={styles.bubble} onClick={toggleChat}>
        💬
      </div>

      {/* Chat window */}
      {isOpen && (
        <div style={styles.chatBox}>
          <div style={styles.header}>
            <strong>Support Chat</strong>
            <span style={styles.closeBtn} onClick={toggleChat}>×</span>
          </div>

          <div style={styles.messages} ref={chatContainerRef}>
            {chatLog.map((msg, i) => (
              <div key={i} style={{ ...styles.message, alignSelf: msg.role === 'user' ? 'flex-end' : 'flex-start', background: msg.role === 'user' ? '#4e9af1' : '#eee', color: msg.role === 'user' ? '#fff' : '#000' }}>
                {msg.content}
              </div>
            ))}
          </div>

          <div style={styles.inputContainer}>
            <input
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              placeholder="Type a message..."
              style={styles.input}
              onKeyDown={(e) => e.key === 'Enter' && sendMessage()}
            />
            <button onClick={sendMessage} style={styles.sendBtn}>Send</button>
          </div>
        </div>
      )}
    </>
  );
};

const styles = {
  bubble: {
    position: 'fixed',
    bottom: 20,
    right: 20,
    width: 60,
    height: 60,
    borderRadius: '50%',
    background: '#4e9af1',
    color: '#fff',
    fontSize: 24,
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    cursor: 'pointer',
    zIndex: 9999
  },
  chatBox: {
    position: 'fixed',
    bottom: 90,
    right: 20,
    width: 320,
    height: 450,
    background: '#fff',
    borderRadius: 12,
    boxShadow: '0 2px 10px rgba(0,0,0,0.2)',
    display: 'flex',
    flexDirection: 'column',
    overflow: 'hidden',
    zIndex: 9999
  },
  header: {
    background: '#4e9af1',
    color: '#fff',
    padding: '10px 15px',
    fontSize: 16,
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center'
  },
  closeBtn: {
    cursor: 'pointer',
    fontWeight: 'bold',
    fontSize: 18
  },
  messages: {
    flex: 1,
    padding: 10,
    display: 'flex',
    flexDirection: 'column',
    gap: 10,
    overflowY: 'auto'
  },
  message: {
    padding: 10,
    borderRadius: 10,
    maxWidth: '80%',
    wordBreak: 'break-word'
  },
  inputContainer: {
    display: 'flex',
    padding: 10,
    borderTop: '1px solid #ddd'
  },
  input: {
    flex: 1,
    padding: 8,
    borderRadius: 8,
    border: '1px solid #ccc'
  },
  sendBtn: {
    marginLeft: 8,
    padding: '8px 12px',
    background: '#4e9af1',
    color: '#fff',
    border: 'none',
    borderRadius: 8,
    cursor: 'pointer'
  }
};

export default ChatWidget;
