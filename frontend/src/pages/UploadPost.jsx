import React, { useState } from "react";
import { useApi } from "../hooks/useApi"; // 导入 useApi hook

const UploadPost = () => {
  const [content, setContent] = useState(""); // 存储贴文内容
  const [alertClassName, setAlertClassName] = useState("hidden"); // 状态消息样式
  const [alertMessage, setAlertMessage] = useState(""); // 状态消息内容
  const { fetchWithToken } = useApi(); // 使用 fetchWithToken 替代原生 fetch

  // 提交贴文
  const handleSubmit = async (event) => {
    event.preventDefault();

    try {
      const payload = { content }; // 发送到后端的数据
      const response = await fetchWithToken("/api/user/upload-post", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      });

      if (response.ok) {
        setAlertClassName(
          "bg-green-500 text-white p-4 rounded border border-green-700"
        );
        setAlertMessage("Post uploaded successfully!");
        setContent(""); // 清空输入框
      } else {
        const data = await response.json();
        setAlertClassName(
          "bg-red-500 text-white p-4 rounded border border-red-700"
        );
        setAlertMessage(data.detail || "Failed to upload post.");
      }
    } catch (error) {
      console.error("Error uploading post:", error);
      setAlertClassName(
        "bg-red-500 text-white p-4 rounded border border-red-700"
      );
      setAlertMessage("An error occurred while uploading.");
    }
  };

  return (
    <div className="max-w-md p-4 mx-auto bg-white rounded shadow">
      <h2 className="mb-4 text-xl font-bold">Upload Post</h2>

      {alertMessage && (
        <p className={`mb-4 ${alertClassName}`}>{alertMessage}</p>
      )}

      <form onSubmit={handleSubmit}>
        <textarea
          value={content}
          onChange={(e) => setContent(e.target.value)}
          placeholder="Write your post content here..."
          className="w-full p-2 mb-4 bg-blue-100 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <button
          type="submit"
          className="w-full px-4 py-2 text-white bg-blue-600 rounded hover:bg-blue-700"
        >
          Upload
        </button>
      </form>
    </div>
  );
};

export default UploadPost;
