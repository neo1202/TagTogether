import React, { useState } from "react";
import { useOutletContext } from "react-router-dom";
import { useApi } from "../hooks/useApi";

function Home() {
  const [username, setUsername] = useState("");
  const { setAlertMessage, setAlertClassName } = useOutletContext();
  const { fetchWithToken } = useApi();

  const fetchUsername = async () => {
    try {
      // 使用 fetchWithToken 替代原生 fetch
      const response = await fetchWithToken("/api/users/me", {
        method: "GET",
      });

      if (response.ok) {
        const data = await response.json();
        setUsername(data.username);
        setAlertMessage("Username fetched successfully!");
        setAlertClassName("alert-success");
      } else {
        const errorData = await response.json();
        setAlertMessage(errorData.detail || "Failed to fetch username.");
        setAlertClassName("alert-danger");
      }
    } catch (error) {
      setAlertMessage("An error occurred while fetching username.");
      setAlertClassName("alert-danger");
    }
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-gradient-to-br from-blue-500 via-indigo-500 to-purple-500 text-gray-100">
      <div className="w-full max-w-lg bg-white bg-opacity-10 backdrop-blur-lg p-6 rounded-lg shadow-lg text-center">
        <h1 className="text-3xl font-bold mb-4 text-white">Welcome to Home</h1>
        {username ? (
          <p className="text-lg">
            Hello, <span className="font-bold text-blue-200">{username}</span>!
          </p>
        ) : (
          <button
            onClick={fetchUsername}
            className="mt-4 bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg transition-all focus:ring-2 focus:ring-blue-300"
          >
            Get My Username
          </button>
        )}
      </div>
    </div>
  );
}

export default Home;
