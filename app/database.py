import hashlib
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "civil_service_cbt.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 username TEXT UNIQUE NOT NULL,
 password_hash TEXT NOT NULL,
 role TEXT NOT NULL DEFAULT 'candidate',
 full_name TEXT NOT NULL,
 created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS questions (
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 question_text TEXT NOT NULL,
 option_a TEXT NOT NULL,
 option_b TEXT NOT NULL,
 option_c TEXT NOT NULL,
 option_d TEXT NOT NULL,
 correct_answer TEXT NOT NULL CHECK(correct_answer IN ('A','B','C','D')),
 category TEXT DEFAULT 'General',
 created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS results (
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 user_id INTEGER NOT NULL,
 score INTEGER NOT NULL,
 total INTEGER NOT NULL,
 percentage REAL NOT NULL,
 grade TEXT NOT NULL,
 passed INTEGER NOT NULL,
 taken_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
 FOREIGN KEY(user_id) REFERENCES users(id)
);
CREATE TABLE IF NOT EXISTS exam_attempts (
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 user_id INTEGER NOT NULL,
 started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
 submitted_at TIMESTAMP,
 FOREIGN KEY(user_id) REFERENCES users(id)
);
"""

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

class Database:
    def __init__(self, path=DB_PATH):
        self.path = Path(path)
        self.initialize()

    def connect(self):
        conn = sqlite3.connect(self.path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys=ON")
        return conn

    def initialize(self):
        with self.connect() as conn:
            conn.executescript(SCHEMA)
            self.seed(conn)

    def seed(self, conn):
        users = [
            ("admin", hash_password("admin123"), "admin", "System Administrator"),
            ("candidate", hash_password("candidate123"), "candidate", "Demo Candidate"),
        ]
        for row in users:
            conn.execute("INSERT OR IGNORE INTO users(username,password_hash,role,full_name) VALUES(?,?,?,?)", row)
        if conn.execute("SELECT COUNT(*) FROM questions").fetchone()[0] == 0:
            questions = [
                ("Which institution coordinates the NYSC programme?","NYSC","NITDA","CBN","FIRS","A","Civic"),
                ("What does CPU stand for?","Central Processing Unit","Computer Personal Unit","Central Program Utility","Computer Processing Utility","A","ICT"),
                ("Which Python type stores key-value pairs?","list","tuple","dictionary","set","C","Python"),
                ("Which protocol is used for secure web traffic?","HTTP","FTP","HTTPS","SMTP","C","Networking"),
                ("What is binary 1010 in decimal?","8","10","12","14","B","Number Systems"),
                ("Which SQL command retrieves records?","SELECT","PUSH","READ","FETCH","A","Database"),
                ("What does HTML stand for?","HyperText Markup Language","HighText Machine Language","Hyperlink Text Management Language","Home Tool Markup Language","A","Web"),
                ("Which Python keyword defines a function?","func","define","def","function","C","Python"),
                ("Which structure follows FIFO?","Stack","Queue","Tree","Graph","B","Computer Science"),
                ("Which device forwards packets between networks?","Switch","Router","Monitor","Keyboard","B","Networking"),
                ("What is hexadecimal 2F in decimal?","45","46","47","48","C","Number Systems"),
                ("Which database does this project use?","MongoDB","SQLite","Oracle","Redis","B","Database"),
                ("Which HTTP method commonly submits form data?","GET","POST","TRACE","HEAD","B","Web"),
                ("What does API stand for?","Application Programming Interface","Application Program Internet","Advanced Programming Input","Applied Protocol Interface","A","Web"),
                ("Which symbol starts a Python comment?","//","#","<!--","/*","B","Python"),
                ("Which is an operating system?","Python","Windows","HTML","SQLite","B","ICT"),
                ("Which OSI layer handles IP addressing?","Physical","Data Link","Network","Application","C","Networking"),
                ("How many bits make one byte?","4","8","16","32","B","Computer Science"),
                ("Which keyword exits a loop early?","stop","exit","break","return","C","Python"),
            ]
            conn.executemany("INSERT INTO questions(question_text,option_a,option_b,option_c,option_d,correct_answer,category) VALUES(?,?,?,?,?,?,?)", questions)
