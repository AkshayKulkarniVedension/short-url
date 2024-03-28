import React, { useState, useEffect } from "react";
import "./ShortenUrlForm.css";

function ShortenUrlForm({ handleLogout }) {
  const [originalUrl, setOriginalUrl] = useState("");
  const [urls, setUrls] = useState([]);

  const token = localStorage.getItem("token");
  const userName = localStorage.getItem("userName");

  const fetchUserUrls = async () => {
    const token = localStorage.getItem("token");
    console.log(token)
    const response = await fetch('http://127.0.0.1:8000/myurls/', {
      headers: {
        Authorization: `Bearer ${token}`,  // Use the stored token for authentication
      },
    });
    if (response.ok) {
      const data = await response.json();
      // Assuming you have a state to store these URLs
      console.log(data)
      setUrls(data);  // Save the fetched URLs
    } else {
      console.error('Failed to fetch URLs');
    }
  };


  const handleSubmit = async (event) => {
    console.log(token);
    event.preventDefault();
    // Replace `YOUR_BACKEND_ENDPOINT` with your actual endpoint for creating short URLs
    console.log(token);
    const response = await fetch("http://127.0.0.1:8000/urls/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        // Include the authentication token in the request header if needed
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({ original_url: originalUrl }),
    });
    const data = await response.json();
    console.log(data);
    fetchUserUrls();
    setOriginalUrl("")
    // Handle response data
  };

  useEffect(() => {
     
    if (token) {
      fetchUserUrls();
    }
  }, [token]);  // Dependency array, re-fetch if token changes
  

  const handleLogouthandler = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("userName"); // Clear the stored user name
    handleLogout();
  };

  return (
    <div className="container-url">
      <div className="user-info">
        <span className="user-name">{userName}</span>
        <button onClick={handleLogouthandler} className="logout-button">
          Logout
        </button>
      </div>
      <form onSubmit={handleSubmit} className="url-form">
        <input
          type="text"
          value={originalUrl}
          onChange={(e) => setOriginalUrl(e.target.value)}
          placeholder="Enter URL to shorten"
          required
        />
        <button type="submit" className="url-button">Shorten URL</button>
      </form>
      <div className="url-list">
        <h3>Your Shortened URLs</h3>
        {urls.length > 0 ? (
          <ul>
            {urls.map((url, index) => (
              <li key={index}>
                <div>Original: <a href={url.original_url} target="_blank" rel="noopener noreferrer">{url.original_url}</a></div>
                <div>Shortened: <a href={`http://127.0.0.1:8000/${url.short_url}`} target="_blank" rel="noopener noreferrer">{`http://127.0.0.1:8000/${url.short_url}`}</a></div>
              </li>
            ))}
          </ul>
        ) : (
          <p>No URLs created yet.</p>
        )}
      </div>
    </div>
  );
}

export default ShortenUrlForm;
