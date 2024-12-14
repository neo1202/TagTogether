import React, { useState, useEffect, useCallback } from "react";
import { useOutletContext } from "react-router-dom";
import { useApi } from "../hooks/useApi";
import coverImage from "../assets/cover.jpg";

function Home() {
  const [username, setUsername] = useState("");
  const [posts, setPosts] = useState([]);
  const { setAlertMessage, setAlertClassName } = useOutletContext();
  const { fetchWithToken } = useApi();

  // Alert 消息显示三秒后消失
  const showAlert = useCallback(
    (message, className) => {
      setAlertMessage(message);
      setAlertClassName(className);
      setTimeout(() => {
        setAlertMessage("");
        setAlertClassName("hidden");
      }, 3000);
    },
    [setAlertMessage, setAlertClassName]
  );

  // 获取帖子
  const fetchPosts = useCallback(async () => {
    try {
      const response = await fetchWithToken("/api/post/posts/");
      if (response.ok) {
        const data = await response.json();
        setPosts(data);
      } else {
        console.error("Failed to fetch posts.");
        showAlert("Failed to fetch posts.", "alert-danger");
      }
    } catch (error) {
      console.error("An error occurred while fetching posts:", error);
      showAlert("An error occurred while fetching posts.", "alert-danger");
    }
  }, [fetchWithToken, showAlert]);

  // 获取用户名
  useEffect(() => {
    const fetchUsername = async () => {
      try {
        const response = await fetchWithToken("/api/user/me");
        if (response.ok) {
          const data = await response.json();
          setUsername(data.user_name);
        } else {
          console.error("Failed to fetch username.");
        }
      } catch (error) {
        console.error("An error occurred while fetching username:", error);
      }
    };

    fetchUsername();
  }, [fetchWithToken]);

  // 获取帖子
  useEffect(() => {
    fetchPosts();
  }, [fetchPosts]);

  return (
    <div className="min-h-screen text-gray-200 bg-black">
      {/* 横幅图片 */}
      <div className="relative">
        <img
          src={coverImage}
          alt="Cover"
          className="object-cover w-full h-auto"
        />
        <div className="absolute inset-0 flex items-center justify-center bg-black bg-opacity-50">
          <h2 className="text-4xl font-extrabold text-gold-400">
            Welcome, {username || "Guest"}!
          </h2>
        </div>
      </div>

      {/* 帖子流 */}
      <div className="p-6 bg-gray-800">
        {posts.length > 0 ? (
          posts.map((post) => (
            <div
              key={post.id}
              className="p-4 mb-4 bg-gray-900 border rounded-lg shadow-lg border-gold-400"
            >
              <h2 className="text-lg font-bold text-purple-400">
                {post.user_name}
              </h2>
              <p className="text-sm text-gray-300">{post.content}</p>
              <span className="text-xs text-gray-500">
                {new Date(post.timestamp).toLocaleString()}
              </span>
            </div>
          ))
        ) : (
          <p className="text-center text-gray-400">
            No posts yet. Be the first to post!
          </p>
        )}
      </div>
    </div>
  );
}

export default Home;
