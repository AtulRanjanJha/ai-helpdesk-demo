import sqlite3
import time

# Improved: Includes created_at for timeout handling
def init_db():
    conn = sqlite3.connect('../helpdesk.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS help_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT,
            customer TEXT,
            status TEXT,
            answer TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# Hardcoded knowledge base for demo
knowledge_base = {
    "opening hours": "We are open from 9am to 7pm, Monday to Saturday.",
    "location": "123 Main Street, Hometown."
}

def ask_agent(question, customer):
    if question.lower() in knowledge_base:
        print(f"AI: {knowledge_base[question.lower()]}")
    else:
        print("AI: Let me check with my supervisor and get back to you.")
        save_help_request(question, customer)

def save_help_request(question, customer):
    conn = sqlite3.connect('../helpdesk.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO help_requests (question, customer, status)
        VALUES (?, ?, 'pending')
    ''', (question, customer))
    conn.commit()
    conn.close()
    print("AI: Request for help has been submitted.")

def poll_for_answers():
    print("AI: Checking for supervisor responses (Ctrl+C to stop)...")
    while True:
        conn = sqlite3.connect('../helpdesk.db')
        c = conn.cursor()
        c.execute("SELECT id, question, answer FROM help_requests WHERE status='resolved'")
        rows = c.fetchall()
        for row in rows:
            print(f"AI: Supervisor answered '{row[1]}': {row[2]}")
            # Update knowledge base
            knowledge_base[row[1].lower()] = row[2]
            # Mark as 'done'
            c.execute("UPDATE help_requests SET status='done' WHERE id = ?", (row[0],))
            conn.commit()
        conn.close()
        time.sleep(5)  # Poll every 5 seconds

if __name__ == "__main__":
    init_db()
    print("AI Agent started. Type your questions. Type 'poll' to check for answers.")
    while True:
        question = input("You: ")
        if question.strip().lower() == "poll":
            poll_for_answers()
        else:
            ask_agent(question, "customer1")
