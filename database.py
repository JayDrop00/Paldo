import sqlite3

conn = sqlite3.connect("users.db")
cursor = conn.cursor()

cursor.execute("DELETE FROM users WHERE id = ?", (6,))  
conn.commit()
conn.close()

print("🗑 User with ID 6 deleted successfully!")
