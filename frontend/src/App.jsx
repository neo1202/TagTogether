import React, { useEffect, useState } from "react";
import { Outlet, Link, useNavigate, useLocation } from "react-router-dom";
import Alert from "./pages/status/Alert";

function App() {
  const [jwtToken, setJwtToken] = useState("");
  const [alertMessage, setAlertMessage] = useState("");
  const [alertClassName, setAlertClassName] = useState("hidden");
  const location = useLocation(); // 用於追踪當前路徑變化

  // 每次路徑變化時清除警告訊息
  useEffect(() => {
    setAlertMessage("");
    setAlertClassName("hidden");
  }, [location.pathname]);

  const navigate = useNavigate();

  const logOut = () => {
    setJwtToken("");
    setAlertMessage("You have been logged out.");
    setAlertClassName("alert-success");
    navigate("/login");
  };

  return (
    <div className="flex flex-col min-h-screen bg-slate-100">
      {/* Navigation Bar */}
      <header className="flex items-center justify-between px-6 py-4 text-white bg-blue-600">
        <h1 className="text-xl font-bold">Event Platform</h1>
        <nav className="flex space-x-4">
          <Link to="/" className="hover:underline">
            Home
          </Link>
          <Link to="/leaderboard" className="hover:underline">
            Leaderboard
          </Link>
          {jwtToken && (
            <>
              <Link to="/sign-up-team" className="hover:underline">
                Sign Up Team
              </Link>
              <Link to="/upload-post" className="hover:underline">
                Upload Post
              </Link>
            </>
          )}
          <button onClick={logOut} className="text-red-400 hover:underline">
            {jwtToken ? "Logout" : <Link to="/login">Login</Link>}
          </button>
        </nav>
      </header>

      {/* Alert Component */}
      <Alert message={alertMessage} className={alertClassName} />

      {/* Main Content */}
      <main className="flex-1 p-4">
        <Outlet
          context={{
            jwtToken,
            setJwtToken,
            setAlertMessage,
            setAlertClassName,
          }}
        />
      </main>
    </div>
  );
}

export default App;
