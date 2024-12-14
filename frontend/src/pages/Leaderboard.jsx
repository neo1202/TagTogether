import React, { useState, useEffect, useCallback } from "react";
import { useApi } from "../hooks/useApi";

const LeaderboardPage = () => {
  const [leaderboard, setLeaderboard] = useState([]);
  const { fetchWithToken } = useApi();

  const fetchLeaderboard = useCallback(async () => {
    console.log("Fetching leaderboard...");
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
    <div className="max-w-4xl p-4 mx-auto">
      <h1 className="mb-4 text-2xl font-bold">Leaderboard</h1>
      <div className="space-y-4">
        {leaderboard.map((team, index) => (
          <div
            key={team.team_name}
            className="flex items-center justify-between p-4 border rounded shadow"
          >
            <span className="font-bold">
              {index + 1}. {team.team_name}
            </span>
            <span className="font-medium text-blue-600">
              {team.score.toFixed(2)}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
};

export default LeaderboardPage;
