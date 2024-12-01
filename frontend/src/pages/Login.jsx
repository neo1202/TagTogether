import { useState } from "react";
import { useNavigate, useOutletContext } from "react-router-dom";
import Input from "../components/form/Input";

const Login = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const { setJwtToken, setAlertClassName, setAlertMessage } = useOutletContext();
  const navigate = useNavigate();

  const handleSubmit = async (event) => {
    event.preventDefault();
    try {
      const payload = { username, password };
      const response = await fetch("/api/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      const data = await response.json();
      if (response.ok) {
        setJwtToken(data.access_token);
        setAlertClassName("hidden");
        setAlertMessage("");
        navigate("/");
      } else {
        setAlertClassName("bg-red-500 text-white p-4 rounded border border-red-700");
        setAlertMessage(data.detail || "Login failed.");
      }
    } catch (error) {
      setAlertClassName("bg-red-500 text-white p-4 rounded border border-red-700");
      setAlertMessage("An error occurred during login.");
    }
  };

  return (
    <div className="max-w-md mx-auto p-4 bg-white rounded shadow">
      <h2 className="text-xl font-bold mb-4">Login</h2>
      <form onSubmit={handleSubmit}>
        <Input
          title="Username"
          type="text"
          name="username"
          className="w-full px-3 py-2 text-sm border border-gray-300 rounded focus:border-blue-500 focus:ring focus:ring-blue-200"
          onChange={(e) => setUsername(e.target.value)}
        />
        <Input
          title="Password"
          type="password"
          name="password"
          className="w-full px-3 py-2 text-sm border border-gray-300 rounded focus:border-blue-500 focus:ring focus:ring-blue-200"
          onChange={(e) => setPassword(e.target.value)}
        />
        <button type="submit" className="w-full bg-blue-600 text-white p-2 rounded mt-4">
          Login
        </button>
      </form>
    </div>
  );
};

export default Login;
