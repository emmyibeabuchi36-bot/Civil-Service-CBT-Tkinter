import random
from .database import Database
from .models import Question, ExamResult, User

class ExamEngine:
    DURATION_SECONDS = 15 * 60
    QUESTIONS_PER_EXAM = 10
    PASS_MARK = 50
    def __init__(self, db: Database, bank): self.db, self.bank = db, bank
    def create_exam(self, user: User):
        questions = self.bank.all()
        selected = random.sample(questions, min(self.QUESTIONS_PER_EXAM, len(questions)))
        with self.db.connect() as conn:
            cur = conn.execute("INSERT INTO exam_attempts(user_id) VALUES(?)", (user.id,))
        return selected, cur.lastrowid
    def grade(self, user: User, questions, answers, attempt_id=None):
        score = sum(answers.get(q.id) == q.correct_answer for q in questions)
        total = len(questions); pct = round(score / total * 100, 2) if total else 0
        grade = "A" if pct >= 70 else "B" if pct >= 60 else "C" if pct >= 50 else "D" if pct >= 45 else "F"
        passed = pct >= self.PASS_MARK
        with self.db.connect() as conn:
            conn.execute("INSERT INTO results(user_id,score,total,percentage,grade,passed) VALUES(?,?,?,?,?,?)", (user.id,score,total,pct,grade,int(passed)))
            if attempt_id: conn.execute("UPDATE exam_attempts SET submitted_at=CURRENT_TIMESTAMP WHERE id=?", (attempt_id,))
        return ExamResult(score,total,pct,grade,passed)
