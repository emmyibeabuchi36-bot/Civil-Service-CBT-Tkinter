from .database import Database
from .models import Question

class QuestionBank:
    def __init__(self, db: Database): self.db = db
    def all(self):
        with self.db.connect() as conn:
            rows = conn.execute("SELECT * FROM questions ORDER BY id").fetchall()
        return [Question(r["id"],r["question_text"],r["option_a"],r["option_b"],r["option_c"],r["option_d"],r["correct_answer"],r["category"]) for r in rows]
    def add(self, text, a, b, c, d, correct, category="General"):
        with self.db.connect() as conn:
            conn.execute("INSERT INTO questions(question_text,option_a,option_b,option_c,option_d,correct_answer,category) VALUES(?,?,?,?,?,?,?)", (text,a,b,c,d,correct.upper(),category or "General"))
    def delete(self, question_id):
        with self.db.connect() as conn: conn.execute("DELETE FROM questions WHERE id=?", (question_id,))
