import React, { useEffect, useState } from "react";
import { Outlet, Link, useNavigate, useLocation } from "react-router-dom";
import Alert from "./pages/status/Alert";

function App() {
  const [jwtToken, setJwtToken] = useState("");
  const [alertMessage, setAlertMessage] = useState("");
  const [alertClassName, setAlertClassName] = useState("hidden");
  const location = useLocation(); // 获取当前路径

  // 用以在切換頁面路徑時清除上個頁面留下來的alert訊息
  useEffect(() => {
    setAlertMessage("");
    setAlertClassName("hidden");
  }, [location.pathname]); // 每当路径变化时触发

  const navigate = useNavigate();

  const logOut = () => {
    setJwtToken("");
    setAlertMessage("You have been logged out.");
    setAlertClassName("alert-success");
    navigate("/login");
  };

  return (
    <div className="flex flex-col min-h-screen bg-slate-100">
      <header className="flex justify-between items-center p-4 bg-blue-600 text-white">
        <h1 className="text-xl">JWT Login Test</h1>
        <nav>
          {jwtToken ? (
            <button className="text-red-400" onClick={logOut}>
              Logout
            </button>
          ) : (
            <Link to="/login">Login</Link>
          )}
        </nav>
      </header>
      <Alert message={alertMessage} className={alertClassName} />
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
