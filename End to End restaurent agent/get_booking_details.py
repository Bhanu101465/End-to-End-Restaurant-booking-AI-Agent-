import sqlite3

def get_booking_details(booking_id: str) -> dict:
    conn = sqlite3.connect('restaurant.db')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT r.booking_id, c.name, c.phone, c.email,
               r.date, r.party_size, r.time, r.status, t.location
        FROM reservations r
        JOIN customers c ON r.customer_id = c.customer_id
        JOIN tables t ON r.table_id = t.table_id
        WHERE r.booking_id = ?
    """, (booking_id,))
    existing = cursor.fetchone()
    conn.close()

    if existing:
        return {
            "booking_id": existing[0],
            "name":       existing[1],
            "phone":      existing[2],
            "email":      existing[3],
            "date":       existing[4],
            "party_size": existing[5],
            "time":       existing[6],
            "status":     existing[7],
            "location":   existing[8]
        }
    else:
        return {"found": False, "message": f"No booking found with ID {booking_id}"}