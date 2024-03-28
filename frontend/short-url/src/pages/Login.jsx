import React, { useState } from "react";
import "./Login.css";

function Login({ setIsAuthenticated }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [errorMessage, setErrorMessage] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    // Assuming the backend endpoint for login is /api/token
    const formData = new URLSearchParams();
    formData.append("username", email);
    formData.append("password", password);
    try {
      const response = await fetch("http://127.0.0.1:8000/token", {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
        body: formData,
      });

      const data = await response.json();

      console.log(data);
      if (!data.access_token) {
        setErrorMessage("Failed to login. Please check your credentials."); 
        setEmail("")
        setPassword("")  
      } else {
        localStorage.setItem("token", data.access_token); // Store the token
        localStorage.setItem("userName", email);
        setIsAuthenticated(true);
      }
       
    } catch (error) {
      console.error("Login error:", error);
      setErrorMessage("Failed to login. Please check your credentials.");
    }
  };

  return (
    <div className="login-container">
      <form onSubmit={handleSubmit} className="login-form">
        <h2>Login</h2>
        {errorMessage && <p className="error">{errorMessage}</p>}
        <div>
          <label htmlFor="email">Email</label>
          <input
            type="email"
            id="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>
        <div>
          <label htmlFor="password">Password</label>
          <input
            type="password"
            id="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        <button type="submit">Login</button>
      </form>
    </div>
  );
}

export default Login;
