URL Shortener
This project is a URL shortening service, built with FastAPI for the backend and React (Vite) for the frontend. It allows users to create shorter aliases for long URLs, making them easier to share. The application supports user authentication, URL creation, and click tracking for each shortened URL.

Getting Started
Follow these instructions to get the project up and running on your local machine for development and testing purposes.

Prerequisites
Before you begin, ensure you have the following installed:

Node.js (14.x or higher recommended)
Python (3.8 or higher)
Git
Backend Setup
Clone the repository and navigate to the backend directory:

bash
Copy code
git clone https://github.com/AkshayKulkarniVedension/short-url.git
cd backend

Install the required Python dependencies:
pip install -r requirements.txt

Start the FastAPI server:
cd app
uvicorn app.main:app --reload
The backend API will be available at http://127.0.0.1:8000.

Frontend Setup
Navigate to the frontend directory from the project root:

cd ../frontend
Install the necessary Node.js dependencies:

npm install
Start the React development server using Vite:

npm run dev
The frontend will be available at http://localhost:3000.

Features
User Registration and Authentication
URL Shortening
Click Tracking for each URL
Viewing all URLs created by a user
