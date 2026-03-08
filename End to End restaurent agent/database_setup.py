import sqlite3

# ============================================================
# STEP 1 — Connect to database (creates file automatically)
# ============================================================
conn = sqlite3.connect('restaurant.db')
cursor = conn.cursor()
print("✅ Database connected!")


# ============================================================
# STEP 2 — Create Tables
# ============================================================

# Table 1: Restaurant Tables (the physical tables in restaurant)
cursor.execute("""
    CREATE TABLE IF NOT EXISTS tables (
        table_id    INTEGER PRIMARY KEY,
        capacity    INTEGER NOT NULL,
        location    TEXT NOT NULL   -- 'indoor', 'outdoor', 'private'
    )
""")
print("✅ 'tables' table created!")


# Table 2: Customers
cursor.execute("""
    CREATE TABLE IF NOT EXISTS customers (
        customer_id   INTEGER PRIMARY KEY AUTOINCREMENT,
        name          TEXT NOT NULL,
        phone         TEXT NOT NULL,
        email         TEXT
    )
""")
print("✅ 'customers' table created!")


# Table 3: Reservations
cursor.execute("""
    CREATE TABLE IF NOT EXISTS reservations (
        booking_id    INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id   INTEGER NOT NULL,
        table_id      INTEGER NOT NULL,
        date          TEXT NOT NULL,   -- format: 'YYYY-MM-DD'
        time          TEXT NOT NULL,   -- format: 'HH:MM'
        party_size    INTEGER NOT NULL,
        status        TEXT DEFAULT 'confirmed',  -- 'confirmed', 'cancelled', 'completed'
        created_at    TEXT DEFAULT (datetime('now')),
        FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
        FOREIGN KEY (table_id)    REFERENCES tables(table_id)
    )
""")
print("✅ 'reservations' table created!")


# ============================================================
# STEP 3 — Seed Data (add sample tables in the restaurant)
# ============================================================

# Check if tables already seeded (avoid duplicates on re-run)
cursor.execute("SELECT COUNT(*) FROM tables")
count = cursor.fetchone()[0]

if count == 0:
    tables_data = [
        (1, 2, 'indoor'),    # Table 1 — 2 seater, indoor
        (2, 2, 'indoor'),    # Table 2 — 2 seater, indoor
        (3, 4, 'indoor'),    # Table 3 — 4 seater, indoor
        (4, 4, 'indoor'),    # Table 4 — 4 seater, indoor
        (5, 4, 'outdoor'),   # Table 5 — 4 seater, outdoor
        (6, 4, 'outdoor'),   # Table 6 — 4 seater, outdoor
        (7, 6, 'outdoor'),   # Table 7 — 6 seater, outdoor
        (8, 6, 'private'),   # Table 8 — 6 seater, private room
        (9, 8, 'private'),   # Table 9 — 8 seater, private room
        (10, 10, 'private'), # Table 10 — 10 seater, private room
    ]
    cursor.executemany("INSERT INTO tables VALUES (?, ?, ?)", tables_data)
    print("✅ Sample tables seeded!")
else:
    print("ℹ️  Tables already seeded, skipping...")


# ============================================================
# STEP 4 — Add some sample customers and reservations for testing
# ============================================================

cursor.execute("SELECT COUNT(*) FROM customers")
cust_count = cursor.fetchone()[0]

if cust_count == 0:
    # Add sample customers
    customers_data = [
        ('Arjun Kumar',   '9876543210', 'arjun@email.com'),
        ('Priya Sharma',  '9123456780', 'priya@email.com'),
        ('Rahul Nair',    '9988776655', 'rahul@email.com'),
    ]
    cursor.executemany(
        "INSERT INTO customers (name, phone, email) VALUES (?, ?, ?)",
        customers_data
    )

    # Add sample reservations
    reservations_data = [
        (1, 3, '2025-03-10', '19:00', 4, 'confirmed'),
        (2, 5, '2025-03-10', '20:00', 2, 'confirmed'),
        (3, 8, '2025-03-11', '19:30', 5, 'confirmed'),
    ]
    cursor.executemany(
        """INSERT INTO reservations 
           (customer_id, table_id, date, time, party_size, status) 
           VALUES (?, ?, ?, ?, ?, ?)""",
        reservations_data
    )
    print("✅ Sample customers and reservations added!")
else:
    print("ℹ️  Sample data already exists, skipping...")


# ============================================================
# STEP 5 — Save everything
# ============================================================
conn.commit()
print("✅ All data saved (committed)!")


# ============================================================
# STEP 6 — Verify everything looks correct
# ============================================================
print("\n" + "="*50)
print("📋 DATABASE SUMMARY")
print("="*50)

# Show all tables
cursor.execute("SELECT * FROM tables")
rows = cursor.fetchall()
print(f"\n🪑 Restaurant Tables ({len(rows)} total):")
print(f"  {'ID':<5} {'Capacity':<10} {'Location'}")
print(f"  {'-'*30}")
for row in rows:
    print(f"  {row[0]:<5} {row[1]:<10} {row[2]}")

# Show all customers
cursor.execute("SELECT * FROM customers")
rows = cursor.fetchall()
print(f"\n👤 Customers ({len(rows)} total):")
print(f"  {'ID':<5} {'Name':<20} {'Phone'}")
print(f"  {'-'*40}")
for row in rows:
    print(f"  {row[0]:<5} {row[1]:<20} {row[2]}")

# Show all reservations
cursor.execute("""
    SELECT r.booking_id, c.name, r.date, r.time, r.party_size, r.status, t.location
    FROM reservations r
    JOIN customers c ON r.customer_id = c.customer_id
    JOIN tables t    ON r.table_id    = t.table_id
""")
rows = cursor.fetchall()
print(f"\n📅 Reservations ({len(rows)} total):")
print(f"  {'ID':<5} {'Name':<15} {'Date':<12} {'Time':<8} {'Party':<7} {'Status':<12} {'Location'}")
print(f"  {'-'*65}")
for row in rows:
    print(f"  {row[0]:<5} {row[1]:<15} {row[2]:<12} {row[3]:<8} {row[4]:<7} {row[5]:<12} {row[6]}")


# ============================================================
# STEP 7 — Close connection
# ============================================================
conn.close()
print("\n✅ Database setup complete! File saved as 'restaurant.db'")
print("🚀 You are ready for Day 2 — building the agent tools!")
