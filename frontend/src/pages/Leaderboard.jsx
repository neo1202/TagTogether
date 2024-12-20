import React, { useState, useEffect, useCallback } from "react";
import { useApi } from "../hooks/useApi";

const LeaderboardPage = () => {
  const [leaderboard, setLeaderboard] = useState([]);
  const [expandedTeamIds, setExpandedTeamIds] = useState([]); // 記錄展開的隊伍 ID
  const [teamDetails, setTeamDetails] = useState({}); // 存儲隊伍詳細信息
  const { fetchWithToken } = useApi();

  // 獲取排行榜數據
  const fetchLeaderboard = useCallback(async () => {
    try {
      const response = await fetchWithToken("/api/team/leaderboard/");
      const data = await response.json();
      if (response.ok) {
        console.log(data);
        setLeaderboard(data);
      } else {
        console.error("Failed to fetch leaderboard.");
      }
    } catch (error) {
      console.error("Error fetching leaderboard:", error);
    }
  }, [fetchWithToken]);

  // 獲取單個隊伍的詳細數據
  const fetchTeamInfo = async (teamId) => {
    if (teamDetails[teamId]) {
      return; // 如果已加載過，則不再發請求
    }
    try {
      const response = await fetchWithToken(`/api/team/score-info/${teamId}`);
      const data = await response.json();
      if (response.ok) {
        setTeamDetails((prevDetails) => ({
          ...prevDetails,
          [teamId]: data,
        }));
      } else {
        console.error(`Failed to fetch team info for team ID ${teamId}.`);
      }
    } catch (error) {
      console.error(`Error fetching team info for team ID ${teamId}:`, error);
    }
  };

  // 切換展開狀態
  const toggleTeamExpansion = (teamId) => {
    if (expandedTeamIds.includes(teamId)) {
      setExpandedTeamIds(expandedTeamIds.filter((id) => id !== teamId));
    } else {
      setExpandedTeamIds([...expandedTeamIds, teamId]);
      fetchTeamInfo(teamId);
    }
  };

  useEffect(() => {
    fetchLeaderboard();
  }, [fetchLeaderboard]);

  return (
    <div className="max-w-4xl px-4 py-4 mx-auto mt-2 text-gray-100 bg-gray-900 rounded-md shadow">
      <h1 className="mb-4 text-2xl font-bold text-center text-purple-300">
        Leaderboard
      </h1>
      <div className="space-y-2">
        {leaderboard.map((team, index) => (
          <div
            key={team.team_id}
            className={`relative cursor-pointer transition ${
              team.is_user_team
                ? "group"
                : "bg-gray-800 border border-gray-700 hover:bg-gray-700"
            }`}
            onClick={() => toggleTeamExpansion(team.team_id)}
          >
            {/* Highlight effect for is_user_team */}
            {team.is_user_team && (
              <div className="absolute -inset-0.5 bg-gradient-to-r from-pink-600 to-purple-600 rounded-lg blur opacity-75 group-hover:opacity-100 transition duration-1000 group-hover:duration-200 animate-tilt"></div>
            )}

            {/* Main team block and expanded content */}
            <div
              className={`relative px-4 py-3 rounded-lg transition-all ${
                team.is_user_team
                  ? "bg-black border border-gray-900 group-hover:bg-gray-800"
                  : "hover:bg-gray-700"
              }`}
            >
              <div className="flex items-center justify-between">
                <span
                  className={`text-base font-medium ${
                    team.is_user_team ? "text-white" : "text-purple-300"
                  }`}
                >
                  {index + 1}. {team.team_name}
                </span>
                <span
                  className={`text-base font-semibold ${
                    team.is_user_team ? "text-white" : "text-purple-300"
                  }`}
                >
                  {team.score.toFixed(2)}
                </span>
              </div>

              {/* Expanded content */}
              {expandedTeamIds.includes(team.team_id) &&
                teamDetails[team.team_id] && (
                  <div
                    className={`mt-2 p-4 rounded-lg ${
                      team.is_user_team
                        ? "bg-black text-white"
                        : "bg-gray-800 text-gray-300"
                    }`}
                  >
                    <p>
                      <span className="font-semibold">Total Members:</span>{" "}
                      {teamDetails[team.team_id].total_members.toFixed(2)} |{" "}
                      <span className="font-semibold">New Members:</span>{" "}
                      {teamDetails[team.team_id].new_members.toFixed(2)}
                    </p>
                    <p>
                      <span className="font-semibold">Earliest Check-in:</span>{" "}
                      {teamDetails[team.team_id].earliest_checkin
                        ? `${
                            teamDetails[team.team_id].earliest_checkin.name
                          } (${new Date(
                            teamDetails[team.team_id].earliest_checkin.time
                          ).toLocaleString()})`
                        : "N/A"}
                    </p>
                    <p>
                      <span className="font-semibold">Latest Check-in:</span>{" "}
                      {teamDetails[team.team_id].latest_checkin
                        ? `${
                            teamDetails[team.team_id].latest_checkin.name
                          } (${new Date(
                            teamDetails[team.team_id].latest_checkin.time
                          ).toLocaleString()})`
                        : "N/A"}
                    </p>
                  </div>
                )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default LeaderboardPage;
