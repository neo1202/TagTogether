import { useState } from "react";
import { useNavigate, useOutletContext } from "react-router-dom";
import Input from "../components/form/Input";

const Login = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const { setJwtToken, setAlertClassName, setAlertMessage } =
    useOutletContext();
  const navigate = useNavigate();

  const handleSubmit = async (event) => {
    event.preventDefault();
    try {
      const payload = { user_name: username, password };
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
        setAlertClassName(
          "bg-red-500 text-white p-4 rounded border border-red-700"
        );
        setAlertMessage(data.detail || "Login failed.");
      }
    } catch (error) {
      setAlertClassName(
        "bg-red-500 text-white p-4 rounded border border-red-700"
      );
      const errorMessage =
        error instanceof Error ? error.message : "An unknown error occurred";
      setAlertMessage(`${errorMessage} occurred during login.`);
    }
  };

  return (
    <div className="max-w-md p-4 mx-auto bg-white rounded shadow">
      <h2 className="mb-4 text-xl font-bold">Login</h2>
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
        <button
          type="submit"
          className="w-full p-2 mt-4 text-white bg-blue-600 rounded"
        >
          Login
        </button>
      </form>
    </div>
  );
};

export default Login;
