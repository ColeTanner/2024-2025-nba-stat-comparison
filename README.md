# 2024-2025 NBA Stat Comparison

A full-stack web application for comparing NBA player statistics from the 2024–2025 season. This project utilizes a Python Flask backend and a React frontend.
Player data is fetched in real-time using the API-NBA service from RapidAPI.

## Tech Stack

- Frontend: React
- Backend: Python with Flask
- API: [API-NBA on RapidAPI](https://rapidapi.com/api-sports/api/api-nba)
- Environment Variables: Stored in `.env` file for API key security

## Features

- Fetches and displays live NBA stats from the 2024-2025 season
- Allows users to compare player performance side by side
- Clean separation of frontend and backend logic
- API key securely managed using environment variables

## .env file example
- API_KEY="API_KEY"
- only the backend files use the .env file. 

### What you need to run this program

- Node.js & npm
- Python 3.x
- `pip` for Python
- flask
- python-dontev
- RapidAPI account and API-NBA subscription
