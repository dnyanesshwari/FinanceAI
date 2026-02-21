from app.db.database import conn, cursor

def add_user(username: str, hashed_password: str, role: str = "user"):
    cursor.execute(
        "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
        (username, hashed_password, role)
    )
    conn.commit()


def get_user(username: str):
    cursor.execute(
        "SELECT username, password, role FROM users WHERE username = ?",
        (username,)
    )

    row = cursor.fetchone()

    if row:
        return {
            "username": row[0],
            "password": row[1],
            "role": row[2]
        }

    return None
