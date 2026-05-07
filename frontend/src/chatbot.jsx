import { useState, useRef, useEffect } from "react";
import "./chatbot.css";

function Chatbot() {
  const [messages, setMessages] = useState([
    {
      id: 1,
      type: "bot",
      content: "🐱 Hi! I'm your Cat Facts assistant. Ask me anything about cats!",
    },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const sendMessage = async () => {
    if (!input.trim()) return;

    // Add user message
    const userMessage = {
      id: messages.length + 1,
      type: "user",
      content: input,
    };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setLoading(true);

    try {
      const response = await fetch("http://localhost:5000/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ message: input }),
      });

      if (!response.ok) {
        throw new Error("Server error");
      }

      const data = await response.json();
      const botMessage = {
        id: messages.length + 2,
        type: "bot",
        content: data.answer || "Sorry, I couldn't get a response.",
      };
      setMessages((prev) => [...prev, botMessage]);
    } catch (error) {
      const errorMessage = {
        id: messages.length + 2,
        type: "bot",
        content: "❌ Error connecting to server. Please check if the Flask API is running.",
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <div className="chatbot-container">
      <div className="chatbot-header">
        <div className="header-content">
          <h1>🐱 Cat Facts Chatbot</h1>
          <p>Ask anything about cats and get instant answers!</p>
        </div>
      </div>

      <div className="chatbot-messages">
        {messages.map((msg) => (
          <div key={msg.id} className={`message-block message-${msg.type}`}>
            <div className="message-avatar">
              {msg.type === "user" ? "👤" : "🐱"}
            </div>
            <div className="message-content">
              <p>{msg.content}</p>
            </div>
          </div>
        ))}

        {loading && (
          <div className="message-block message-bot">
            <div className="message-avatar">🐱</div>
            <div className="message-content typing">
              <span></span>
              <span></span>
              <span></span>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      <div className="chatbot-input-area">
        <div className="input-container">
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Ask me about cats... (Press Shift+Enter for new line)"
            className="input-field"
            rows="3"
          />
          <button
            onClick={sendMessage}
            disabled={loading || !input.trim()}
            className="send-button"
          >
            {loading ? "⏳" : "📤"}
          </button>
        </div>
        <p className="input-hint">💡 Try: "How high can a cat jump?" or "What is the oldest cat?"</p>
      </div>
    </div>
  );
}

export default Chatbot;