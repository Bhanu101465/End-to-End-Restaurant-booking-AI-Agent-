import sqlite3

def cancel_booking(booking_id: int) -> dict:
    conn = sqlite3.connect('restaurant.db')
    cursor = conn.cursor()

    cursor.execute("""
        SELECT r.booking_id, c.name, c.phone, c.email, r.status
        FROM reservations r
        JOIN customers c ON r.customer_id = c.customer_id
        WHERE r.booking_id = ?
    """, (booking_id,))
    existing = cursor.fetchone()

    if not existing:
        conn.close()
        return {"found": False, "message": f"No booking found with ID {booking_id}"}

    cursor.execute("""
        UPDATE reservations SET status = 'cancelled' WHERE booking_id = ?
    """, (booking_id,))
    conn.commit()
    conn.close()

    return {
        "booking_id": existing[0],
        "name":       existing[1],
        "phone":      existing[2],
        "email":      existing[3],
        "status":     "cancelled"
    }
