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
      const response = await fetchWithToken("/api/user/me", {
        method: "GET",
      });

      if (response.ok) {
        const data = await response.json();
        setUsername(data.user_name);
        setAlertMessage("User_name fetched successfully!");
        setAlertClassName("alert-success");
      } else {
        const errorData = await response.json();
        setAlertMessage(errorData.detail || "Failed to fetch user_name.");
        setAlertClassName("alert-danger");
      }
    } catch (error) {
      console.log(error);
      setAlertMessage("An error occurred while fetching user_name.");
      setAlertClassName("alert-danger");
    }
  };

  return (
    <div className="flex items-center justify-center min-h-screen text-gray-100 bg-gradient-to-br from-blue-500 via-indigo-500 to-purple-500">
      <div className="w-full max-w-lg p-6 text-center bg-white rounded-lg shadow-lg bg-opacity-10 backdrop-blur-lg">
        <h1 className="mb-4 text-3xl font-bold text-white">Welcome to Home</h1>
        {username ? (
          <p className="text-lg">
            Hello, <span className="font-bold text-blue-200">{username}</span>!
          </p>
        ) : (
          <button
            onClick={fetchUsername}
            className="px-4 py-2 mt-4 text-white transition-all bg-blue-600 rounded-lg hover:bg-blue-700 focus:ring-2 focus:ring-blue-300"
          >
            Get My Username
          </button>
        )}
      </div>
    </div>
  );
}

export default Home;
