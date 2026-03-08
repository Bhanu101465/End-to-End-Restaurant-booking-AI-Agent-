import sqlite3

def check_availability(date: str, time: str, party_size: int) -> dict:
    "checks real available tables from database"
    
    conn = sqlite3.connect('restaurant.db')
    cursor = conn.cursor()
    
    # Query actual database in real time
    cursor.execute("""
        SELECT COUNT(*) FROM tables 
        WHERE capacity >= ? 
        AND table_id NOT IN (
            SELECT table_id FROM reservations
            WHERE date = ? AND time = ?
        )
    """, (party_size, date, time))
    
    available = cursor.fetchone()[0]
    conn.close()
    
    return {
        "date": date,
        "time": time,
        "available_tables": available,  # ← REAL data from DB
        "can_book": available > 0
    }