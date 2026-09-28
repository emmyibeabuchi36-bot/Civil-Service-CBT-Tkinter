from .database import Database
from .models import ExamResult
class ResultService:
    def __init__(self, db: Database): self.db = db
    def history(self, user_id):
        with self.db.connect() as conn:
            return conn.execute("SELECT score,total,percentage,grade,passed,taken_at FROM results WHERE user_id=? ORDER BY id DESC", (user_id,)).fetchall()
    def all_results(self):
        with self.db.connect() as conn:
            return conn.execute("SELECT results.*,users.username,users.full_name FROM results JOIN users ON users.id=results.user_id ORDER BY results.id DESC").fetchall()
