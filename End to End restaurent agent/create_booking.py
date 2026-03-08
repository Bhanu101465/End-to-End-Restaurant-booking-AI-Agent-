import sqlite3

def create_booking ( name:str,phone : int ,email_id:str,party_size: int,date:int,time:str ) ->dict :
    "this creates booking" 
    conn=sqlite3.connect('restaurant.db')
    cursor=conn.cursor()

    cursor.execute("""
          SELECT customer_id FROM customers
         WHERE phone=?
        
         """,(phone,))
    existing=cursor.fetchone()
    if existing:
        customer_id = existing[0]
    else :#if its not there
        cursor.execute("""
             INSERT INTO customers(name,phone,email)
              VALUES(?,?,?);                  
         """,(name,phone,email_id))
    customer_id=cursor.lastrowid
    #find available table

    cursor.execute("""
        SELECT table_id FROM tables 
        WHERE capacity >= ? 
        AND table_id NOT IN (
            SELECT table_id FROM reservations
            WHERE date=? AND time=?
            AND status='confitmed'
                   )
       LIMIT 1            
        """,(party_size,date,time)
    )
    table=cursor.fetchone()
    if not table:
        conn.close()
        return {
            "success": False,
            "message": f"Sorry! No tables available for {party_size} people on {date} at {time}"
        }

    table_id = table[0]

    # STEP 3 — Insert reservation
    cursor.execute("""
        INSERT INTO reservations (customer_id, table_id, date, time, party_size, status)
        VALUES (?, ?, ?, ?, ?, 'confirmed')
    """, (customer_id, table_id, date, time, party_size))

    booking_id = cursor.lastrowid  # auto generated booking ID

    conn.commit()   # ← MOST IMPORTANT LINE — saves to database
    conn.close()

    return {
        "Success" : True,
        "booking_id": booking_id,
        "name" : name,
        "phone ":phone,
        "email_id": email_id,
        "date" : date,
        "Party size": party_size,
        "message": f"booking confimed id is {booking_id}"
    }

