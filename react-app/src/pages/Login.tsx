import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import AuthForm from "../components/AuthForm";
import * as authApi from "../api/auth";

const Login: React.FC = () => {
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleLogin = async (username: string, password: string) => {
    try {
      await authApi.login(username, password);
      navigate("/dashboard");
    } catch (err) {
      setError("Wrong username or password.");
    }
  };

  return (
    <div className="container mt-3">
      <h1>React Cookie Auth</h1>
      <br />
      <h2>Login</h2>
      <AuthForm onSubmit={handleLogin} error={error} />
    </div>
  );
};

export default Login;