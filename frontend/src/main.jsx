import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";
import "./index.css";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import Login from "./pages/Login";
import Home from "./pages/Home";
import ErrorPage from "./pages/status/Error";
import Leaderboard from "./pages/Leaderboard";
import SignUpGroup from "./pages/SignUpGroup";
import UploadPost from "./pages/UploadPost";
const router = createBrowserRouter([
  {
    path: "/",
    element: <App />,
    errorElement: <ErrorPage />,
    children: [
      { index: true, element: <Home /> },
      {
        path: "/login",
        element: <Login />,
      },
      {
        path: "/leaderboard",
        element: <Leaderboard />,
      },
      {
        path: "/sign-up-group",
        element: <SignUpGroup />,
      },
      {
        path: "/upload-post",
        element: <UploadPost />,
      },
      // {
      //   path: "/movies/:id",
      //   element: <Movie />,
      // },
    ],
  },
]);

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>
);
