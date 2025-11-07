# AI Helpdesk with Supervisor System

## Overview
AI agent that answers customer questions. When it doesn't know the answer, it requests help from a human supervisor through a web UI.

## Features
- AI agent with knowledge base
- Supervisor admin panel (pending requests & history)
- Auto-timeout for unresolved requests (5 min)
- Knowledge base updates with supervisor answers

## Setup
1. Install dependencies:
   - Python 3.x
   - Node.js
2. In `supervisor-ui-node/`: `npm install`
3. Run backend: `node index.js` (in supervisor-ui-node/)
4. Run agent: `python agent.py` (in agent-python/)
5. Open browser: http://localhost:3001/requests.html

## Architecture
- Python: AI agent logic
- Node.js + Express: Supervisor backend API
- SQLite: Shared database for help requests
- HTML/CSS/JS: Supervisor UI

## Future Improvements
- Add real-time WebSocket notifications
- Implement Twilio for actual SMS/calls
- Deploy to cloud (AWS/Heroku)
- Add authentication for supervisor panel
