import React, { useState } from "react";
import axios from "axios";

const SalesChatbot = () => {
  const [chatbotInput, setChatbotInput] = useState("");
  const [chatbotResponse, setChatbotResponse] = useState(null);
  const [loadingChatbot, setLoadingChatbot] = useState(false);

  const handleChatbotQuery = async () => {
    setLoadingChatbot(true);
    try {
      const response = await axios.post("http://127.0.0.1:5000/chatbot", {
        query: chatbotInput,
      });
      setChatbotResponse(response.data.response); //backend returns {response: "..."}
    } catch (error) {
      console.error("Error with chatbot query:", error);
    } finally {
      setLoadingChatbot(false);
    }
  };

  return (
    <div className="p-4 bg-white rounded-lg shadow mt-4">
      <h3 className="font-bold text-lg mb-4">Sales Prediction Chatbot</h3>
      <textarea
        placeholder="Ask a sales-related question..."
        value={chatbotInput}
        onChange={(e) => setChatbotInput(e.target.value)}
        className="w-full p-2 border rounded"
      />
      <button
        onClick={handleChatbotQuery}
        disabled={loadingChatbot}
        className="mt-4 px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600 disabled:bg-green-300"
      >
        {loadingChatbot ? "Thinking..." : "Ask Chatbot"}
      </button>
      {chatbotResponse && (
        <div className="mt-4">
          <h4 className="font-medium">Chatbot Response</h4>
          <pre className="p-4 bg-gray-100 rounded">{chatbotResponse}</pre>
        </div>
      )}
    </div>
  );
};

export default SalesChatbot;
