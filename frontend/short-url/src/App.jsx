import { useState, useEffect } from "react";
import ShortenUrlForm from "./components/ShortenUrlForm";
import "./App.css";

import Login from "./pages/Login";

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [token, setToken] = useState("");

  useEffect(() => {
    // Check for the token in local storage on app load
    const token = localStorage.getItem("token");
    if (token) {
      setIsAuthenticated(true);
      setToken(token);
    }
  }, []);

  const handleLogout = () => {
    localStorage.removeItem("token");
    setIsAuthenticated(false);
  };

  return (
    <>
      <div>
        {!isAuthenticated ? (
          <Login setIsAuthenticated={setIsAuthenticated} />
        ) : (
          <ShortenUrlForm token={token} handleLogout={() => handleLogout()} />
        )}
      </div>
    </>
  );
}

export default App;
