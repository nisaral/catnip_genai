import React, { useState } from "react";
import axios from "axios";

const SalesChatbot = () => {
  const [category, setCategory] = useState("");
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const res = await axios.post("http://localhost:5000/sales_forecast", { category });
      setResponse(res.data);
    } catch (error) {
      setResponse({ error: "Failed to fetch data. Please try again." });
    }
    setLoading(false);
  };

  return (
    <div className="bg-white p-4 shadow-md rounded-md">
      <h2 className="font-bold text-xl mb-4">Sales Prediction Chatbot</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          className="border p-2 rounded-md w-full mb-4"
          placeholder="Enter category"
          value={category}
          onChange={(e) => setCategory(e.target.value)}
        />
        <button
          type="submit"
          className="bg-blue-500 text-white px-4 py-2 rounded-md"
          disabled={loading}
        >
          {loading ? "Loading..." : "Get Forecast"}
        </button>
      </form>

      {response && (
        <div className="mt-4">
          {response.error ? (
            <p className="text-red-500">{response.error}</p>
          ) : (
            <div>
              <p className="font-bold">Forecast Suggestion:</p>
              <p>{response.suggestion}</p>
              <img
                src={`http://localhost:5000/${response.plot_path}`}
                alt="Sales Forecast"
                className="mt-4"
              />
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default SalesChatbot;
