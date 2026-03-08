# End-to-End-Restaurant-booking-AI-Agent-
An intelligent conversational AI agent that handles restaurant reservations in real time — built using **Groq API**, **LLaMA3**, and **SQLite**.

---

## 📌 Project Overview

This project is a fully functional AI-powered restaurant booking system that allows users to check table availability, make reservations, view booking details, and cancel bookings — all through natural language conversation.

The agent remembers the full conversation history throughout the session, so users can have a natural back-and-forth dialogue without repeating themselves.

---

## 🎥 Demo

```
🍽️  Welcome to Restaurant Booking Agent!
Type 'quit' to exit

You: Is there a table for 4 people on 2025-03-15 at 19:00?
Agent: Yes! There are 7 tables available for 4 people on March 15 at 19:00.
       Would you like me to book one for you?

You: Yes please
Agent: Sure! What is your name?

You: Arjun
Agent: Got it Arjun! What is your phone number?

You: 9876543210
Agent: And your email address?

You: arjun@email.com
Agent: Booking confirmed! Your Booking ID is 6.
       See you on March 15 at 7:00 PM! 🎉

You: Get details for booking 6
Agent: Booking ID: 6 | Name: Arjun | Date: 2025-03-15 |
       Time: 19:00 | Party: 4 | Status: confirmed | Location: indoor

You: Cancel booking 6
Agent: Booking 6 has been successfully cancelled!

You: quit
Goodbye! 👋
```

---

## 🏗️ Architecture

```
User Input (Natural Language)
        ↓
   messages list (conversation history)
        ↓
   Groq API — LLaMA3 -4-scout
        ↓
   Tool Calling (ReAct Loop)
   ┌──────────────────────────────────┐
   │  check_availability()            │
   │  create_booking()                │
   │  get_booking_details()           │
   │  cancel_booking()                │
   └──────────────────────────────────┘
        ↓
   SQLite Database (restaurant.db)
   ┌──────────────────────────────────┐
   │  tables       (restaurant tables)│
   │  customers    (customer info)    │
   │  reservations (booking records)  │
   └──────────────────────────────────┘
        ↓
   Natural Language Response to User
```

---

## 🧠 How Memory Works

Unlike basic chatbots, this agent remembers the **full conversation history** using a `messages` list:

```python
messages = [
    {"role": "system",    "content": "You are a restaurant booking assistant..."},
    {"role": "user",      "content": "Is there a table for 4 on March 15?"},
    {"role": "assistant", "content": "Yes! 7 tables available. Shall I book?"},
    {"role": "user",      "content": "Yes, my name is Arjun"},
    {"role": "assistant", "content": "Booking confirmed! ID is 6"},
]
```

Every message is added to the list and the **entire history is sent to Groq on every turn** — so the agent always knows what was said before.

> Note: Memory is session-based — it resets when the program restarts. Future enhancement: persist messages to database for permanent memory.

---

## ✨ Features

- **Check Availability** — Find available tables by date, time, and party size in real time
- **Create Booking** — Reserve a table and store customer details in the database
- **Get Booking Details** — Retrieve full reservation info using a booking ID
- **Cancel Booking** — Update reservation status to cancelled instantly
- **Multi-turn Conversation** — Agent remembers full context throughout the session
- **Real-time Database** — All data is live — no hardcoded or mock responses
- **Tool Calling** — Agent decides which tool to call automatically based on user intent

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python 3.12 | Core programming language |
| Groq API | LLM inference platform (free & fast) |
| Llama-4-scout | Large Language Model for conversation |
| SQLite | Lightweight real-time database |
| messages list | Session-based conversation memory |

---

## 📁 Project Structure

```
End to End Restaurant Agent/
│
├── database_setup.py       # Creates and seeds the SQLite database
├── check_availability.py   # Tool: checks available tables in real time
├── create_booking.py       # Tool: creates a new reservation in DB
├── get_booking_details.py  # Tool: fetches booking info from DB
├── cancel_booking.py       # Tool: cancels an existing booking in DB
├── agent.py                # Main agent — Groq + tools + chat loop
└── restaurant.db           # SQLite database (auto-created on setup)
```

---

## ⚙️ Setup & Installation

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/restaurant-booking-agent.git
cd restaurant-booking-agent
```

### 2. Install Dependencies
```bash
pip install groq
```

### 3. Get Free Groq API Key
```
1. Go to https://console.groq.com
2. Sign up for free
3. Go to API Keys → Create key
4. Copy your key
```

### 4. Set API Key
```bash
# Windows
set GROQ_API_KEY=your_api_key_here

# Mac/Linux
export GROQ_API_KEY=your_api_key_here
```

### 5. Initialize the Database
```bash
python database_setup.py
```

You will see:
```
✅ Database connected!
✅ tables table created!
✅ customers table created!
✅ reservations table created!
✅ Sample data added!
🚀 Database ready!
```

### 6. Run the Agent
```bash
python agent.py
```

---

## 🗄️ Database Schema

```sql
-- Physical tables in the restaurant
CREATE TABLE tables (
    table_id   INTEGER PRIMARY KEY,
    capacity   INTEGER,
    location   TEXT        -- 'indoor', 'outdoor', 'private'
);

-- Customer information
CREATE TABLE customers (
    customer_id  INTEGER PRIMARY KEY AUTOINCREMENT,
    name         TEXT,
    phone        TEXT,
    email        TEXT
);

-- Reservations (links customers + tables)
CREATE TABLE reservations (
    booking_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id  INTEGER,
    table_id     INTEGER,
    date         TEXT,      -- format: YYYY-MM-DD
    time         TEXT,      -- format: HH:MM
    party_size   INTEGER,
    status       TEXT,      -- 'confirmed', 'cancelled', 'completed'
    created_at   TEXT,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (table_id)    REFERENCES tables(table_id)
);
```

---

## 🤖 Agent Tools

| Tool | Description | DB Operation |
|---|---|---|
| `check_availability()` | Finds free tables for given date/time/party size | SELECT |
| `create_booking()` | Creates reservation, adds customer if new | INSERT + INSERT |
| `get_booking_details()` | Fetches full booking info using SQL JOINs | SELECT + JOIN |
| `cancel_booking()` | Updates reservation status to cancelled | SELECT + UPDATE |

---

## 🔄 Agent Loop (ReAct Pattern)

```
User sends message
      ↓
Added to messages history
      ↓
Sent to Groq (LLaMA3)
      ↓
Agent REASONS: what does the user want?
      ↓
Agent ACTS: calls the right tool
      ↓
Tool queries SQLite database
      ↓
Result returned to agent
      ↓
Agent OBSERVES result
      ↓
Agent responds naturally to user
      ↓
Response added to messages history
      ↓
Loop continues...
```

---

## 🧑‍💻 Concepts Demonstrated

- **AI Agent with Tool Calling** — ReAct pattern (Reason → Act → Observe)
- **Conversation Memory** — Full history management using messages list
- **Real-time Database Integration** — Live SQLite queries on every tool call
- **Natural Language Understanding** — LLM converts user intent to tool calls
- **SQL JOINs** — Combining data across multiple related tables
- **Error Handling** — Graceful responses when bookings not found or tables full
- **Function Calling** — Structured tool definitions with JSON schema

---

## 🚀 Future Enhancements

- **RAG Integration** — Answer menu and dietary questions from restaurant documents
- **Email/SMS Notifications** — Send booking confirmations via Twilio/SendGrid
- **Streamlit UI** — Web interface for non-technical users
- **Permanent Memory** — Save conversation history to database across sessions
- **A2A Protocol** — Multi-agent architecture with separate booking, payment, and notification agents
- **MCP Integration** — Standardized tool connectivity for scalability
- **PostgreSQL** — Production-grade database replacing SQLite

---

## 👨‍💻 Author

**Bhanu**
Software Developer | AI/ML Enthusiast
Completed: Google 5-Day Agentic AI Course

---

## 📄 License

This project is open source and available under the MIT License.
