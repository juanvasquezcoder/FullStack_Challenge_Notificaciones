import sqlite3
import sys

email = sys.argv[1] if len(sys.argv) > 1 else input("Email a promover a admin: ")

conn = sqlite3.connect("notifications.db")
cur = conn.cursor()

admin_role_id = cur.execute("SELECT id FROM roles WHERE name = 'admin'").fetchone()[0]
cur.execute("UPDATE users SET role_id = ? WHERE email = ?", (admin_role_id, email))
conn.commit()

if cur.rowcount == 0:
    print(f"No se encontró ningún usuario con email {email}")
else:
    print(f"{email} ahora es admin.")

conn.close()