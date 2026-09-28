import sqlite3
from .database import Database, hash_password
from .models import User

class AuthenticationService:
    def __init__(self, db: Database): self.db = db

    def register(self, full_name, username, password):
        full_name, username = full_name.strip(), username.strip().lower()
        if not full_name or not username or not password: return False, "All fields are required."
        try:
            with self.db.connect() as conn:
                conn.execute("INSERT INTO users(username,password_hash,role,full_name) VALUES(?,?,?,?)", (username, hash_password(password), "candidate", full_name))
            return True, "Registration successful."
        except sqlite3.IntegrityError:
            return False, "Username already exists."

    def login(self, username, password):
        with self.db.connect() as conn:
            row = conn.execute("SELECT id,username,role,full_name,password_hash FROM users WHERE username=?", (username.strip().lower(),)).fetchone()
        if row and row["password_hash"] == hash_password(password):
            return User(row["id"], row["username"], row["role"], row["full_name"])
        return None
