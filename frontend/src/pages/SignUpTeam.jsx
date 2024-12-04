import React, { useState, useEffect, useCallback } from "react";
import { useOutletContext } from "react-router-dom";

const TeamsPage = () => {
  const [teams, setTeams] = useState([]); // 存储团队列表
  const [isModalOpen, setIsModalOpen] = useState(false); // 控制模态视窗显示
  const [newTeamName, setNewTeamName] = useState(""); // 新团队名称
  const [alertClassName, setAlertClassName] = useState("hidden"); // 状态消息样式
  const [alertMessage, setAlertMessage] = useState(""); // 状态消息内容
  const { jwtToken } = useOutletContext(); // 从 context 获取 JWT token

  // 从后端获取团队列表
  const fetchTeams = useCallback(async () => {
    try {
      const response = await fetch("/api/team/all-teams/", {
        headers: {
          Authorization: `Bearer ${jwtToken}`,
        },
      });
      const data = await response.json();
      if (response.ok) {
        setTeams(data);
        setAlertClassName("hidden");
        setAlertMessage("");
      } else {
        setAlertClassName(
          "bg-red-500 text-white p-4 rounded border border-red-700"
        );
        setAlertMessage("Failed to load teams.");
      }
    } catch (error) {
      console.error(error);
      setAlertClassName(
        "bg-red-500 text-white p-4 rounded border border-red-700"
      );
      setAlertMessage("An error occurred while fetching teams.");
    }
  }, [jwtToken]);

  // 创建新团队
  const handleCreateTeam = async () => {
    try {
      const response = await fetch("/api/team/create-team/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${jwtToken}`,
        },
        body: JSON.stringify({ team_name: newTeamName }),
      });
      const data = await response.json();
      if (response.ok) {
        setAlertClassName(
          "bg-green-500 text-white p-4 rounded border border-green-700"
        );
        setAlertMessage("Team created successfully!");
        setNewTeamName("");
        setIsModalOpen(false);
        fetchTeams(); // 创建团队后刷新列表
      } else {
        setAlertClassName(
          "bg-red-500 text-white p-4 rounded border border-red-700"
        );
        setAlertMessage(data.detail || "Failed to create team.");
      }
    } catch (error) {
      console.error(error);
      setAlertClassName(
        "bg-red-500 text-white p-4 rounded border border-red-700"
      );
      setAlertMessage("An error occurred while creating the team.");
    }
  };

  // 加入团队
  const handleJoinTeam = async (teamName) => {
    try {
      const response = await fetch("/api/team/join-team/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${jwtToken}`,
        },
        body: JSON.stringify({
          team_name: teamName, // 只发送团队名称
        }),
      });
      if (response.ok) {
        setAlertClassName(
          "bg-green-500 text-white p-4 rounded border border-green-700"
        );
        setAlertMessage("Successfully joined the team!");
        fetchTeams(); // 刷新列表以反映加入状态
      } else {
        const data = await response.json();
        setAlertClassName(
          "bg-red-500 text-white p-4 rounded border border-red-700"
        );
        setAlertMessage(data.detail || "Failed to join team.");
      }
    } catch (error) {
      console.error(error);
      setAlertClassName(
        "bg-red-500 text-white p-4 rounded border border-red-700"
      );
      setAlertMessage("An error occurred while joining the team.");
    }
  };

  useEffect(() => {
    fetchTeams(); // 初始化加载团队
  }, [fetchTeams]);

  return (
    <div className="max-w-4xl p-4 mx-auto">
      <h1 className="mb-4 text-2xl font-bold">Teams</h1>

      <button
        onClick={() => setIsModalOpen(true)}
        className="px-4 py-2 mb-4 text-white bg-blue-500 rounded"
      >
        Create New Team
      </button>

      {alertMessage && (
        <p className={`mb-4 ${alertClassName}`}>{alertMessage}</p>
      )}

      <div className="space-y-4">
        {teams.map((team) => (
          <div
            key={team.id}
            className="flex items-center justify-between p-4 border rounded shadow"
          >
            <span>{team.name}</span>
            <button
              onClick={() => handleJoinTeam(team.name)}
              className="px-4 py-2 text-white bg-green-500 rounded"
            >
              Join
            </button>
          </div>
        ))}
      </div>

      {/* Modal for creating a new team */}
      {isModalOpen && (
        <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50">
          <div className="p-6 bg-white rounded shadow-lg w-80">
            <h2 className="mb-4 text-lg font-bold">Create a New Team</h2>
            <input
              type="text"
              value={newTeamName}
              onChange={(e) => setNewTeamName(e.target.value)}
              placeholder="Team Name"
              className="w-full p-2 mb-4 border border-gray-300 rounded"
            />
            <div className="flex justify-end space-x-2">
              <button
                onClick={() => setIsModalOpen(false)}
                className="px-4 py-2 text-gray-700 bg-gray-300 rounded"
              >
                Cancel
              </button>
              <button
                onClick={handleCreateTeam}
                className="px-4 py-2 text-white bg-blue-500 rounded"
              >
                Create
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default TeamsPage;
