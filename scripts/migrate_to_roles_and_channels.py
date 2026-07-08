import sqlite3

conn = sqlite3.connect("notifications.db")
cur = conn.cursor()

# 1. Crear tabla roles y sembrar valores
cur.execute("""
CREATE TABLE IF NOT EXISTS roles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL
)
""")
cur.execute("INSERT OR IGNORE INTO roles (name) VALUES ('admin')")
cur.execute("INSERT OR IGNORE INTO roles (name) VALUES ('user')")
conn.commit()

user_role_id = cur.execute("SELECT id FROM roles WHERE name = 'user'").fetchone()[0]

# 2. Crear tabla channels y sembrar los 4 canales originales
cur.execute("""
CREATE TABLE IF NOT EXISTS channels (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    is_active BOOLEAN DEFAULT 1
)
""")
default_channels = [
    ("email", "Correo electrónico"),
    ("sms", "SMS"),
    ("push", "Notificación push"),
    ("in_app", "En la aplicación"),
]
for code, name in default_channels:
    cur.execute("INSERT OR IGNORE INTO channels (code, name) VALUES (?, ?)", (code, name))
conn.commit()

# 3. Agregar role_id a users, asignar 'user' a todos los existentes
cur.execute("ALTER TABLE users ADD COLUMN role_id INTEGER")
cur.execute("UPDATE users SET role_id = ? WHERE role_id IS NULL", (user_role_id,))
conn.commit()

# 4. Agregar channel_id a notifications, migrar desde el campo 'channel' (texto)
cur.execute("ALTER TABLE notifications ADD COLUMN channel_id INTEGER")
for code, _ in default_channels:
    channel_id = cur.execute("SELECT id FROM channels WHERE code = ?", (code,)).fetchone()[0]
    cur.execute("UPDATE notifications SET channel_id = ? WHERE channel = ?", (channel_id, code))
conn.commit()

# 5. Eliminar la columna vieja 'channel' (requiere SQLite 3.35+, incluido en Python 3.13)
cur.execute("ALTER TABLE notifications DROP COLUMN channel")
conn.commit()

conn.close()
print("Migración completada.")