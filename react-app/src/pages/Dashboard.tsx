import React from "react";
import { useNavigate } from "react-router-dom";
import * as authApi from "../api/auth";

const Dashboard: React.FC = () => {
  const navigate = useNavigate();

  const handleWhoAmI = async () => {
    try {
      const data = await authApi.whoami();
      console.log("You are logged in as: " + data.username);
    } catch (err) {
      console.error(err);
    }
  };

  const handleLogout = async () => {
    try {
      await authApi.logout();
      navigate("/login");
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className="container mt-3">
      <h1>React Cookie Auth</h1>
      <p>You are logged in!</p>
      <button className="btn btn-primary mr-2" onClick={handleWhoAmI}>
        WhoAmI
      </button>
      <button className="btn btn-danger" onClick={handleLogout}>
        Log out
      </button>
    </div>
  );
};

export default Dashboard;