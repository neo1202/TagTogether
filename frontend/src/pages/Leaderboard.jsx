import React, { useState, useEffect, useCallback } from "react";
import { useApi } from "../hooks/useApi";

const LeaderboardPage = () => {
  const [leaderboard, setLeaderboard] = useState([]);
  const { fetchWithToken } = useApi();

  const fetchLeaderboard = useCallback(async () => {
    try {
      const response = await fetchWithToken("/api/team/leaderboard/");
      const data = await response.json();
      if (response.ok) {
        setLeaderboard(data);
      } else {
        console.error("Failed to fetch leaderboard.");
      }
    } catch (error) {
      console.error("Error fetching leaderboard:", error);
    }
  }, [fetchWithToken]);

  useEffect(() => {
    fetchLeaderboard();
  }, [fetchLeaderboard]);

  return (
    <div className="max-w-4xl p-6 mx-auto mt-2 text-gray-100 bg-gray-900 rounded-lg shadow-lg">
      <h1 className="mb-6 text-3xl font-bold text-center text-purple-400">
        Leaderboard
      </h1>
      <div className="space-y-4">
        {leaderboard.map((team, index) => (
          <div
            key={team.team_name}
            className="flex items-center justify-between p-4 bg-gray-800 border border-gray-700 rounded shadow"
          >
            <span className="text-lg font-semibold text-gold-500">
              {index + 1}. {team.team_name}
            </span>
            <span className="text-xl font-medium text-purple-400">
              {team.score.toFixed(2)}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
};

export default LeaderboardPage;
