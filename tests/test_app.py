import tempfile
import unittest
from pathlib import Path
from app.database import Database
from app.auth import AuthenticationService
from app.questions import QuestionBank
from app.exam import ExamEngine

class CBTTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.NamedTemporaryFile(suffix=".db",delete=False); self.tmp.close(); self.db=Database(self.tmp.name)
        self.auth=AuthenticationService(self.db); self.bank=QuestionBank(self.db); self.exam=ExamEngine(self.db,self.bank)
    def tearDown(self): Path(self.tmp.name).unlink(missing_ok=True)
    def test_demo_login(self): self.assertIsNotNone(self.auth.login("candidate","candidate123"))
    def test_question_bank_seeded(self): self.assertGreaterEqual(len(self.bank.all()),10)
    def test_exam_grading(self):
        user=self.auth.login("candidate","candidate123"); qs,attempt=self.exam.create_exam(user); result=self.exam.grade(user,qs,{q.id:q.correct_answer for q in qs},attempt); self.assertEqual(result.score,result.total); self.assertEqual(result.percentage,100); self.assertTrue(result.passed)

if __name__=="__main__": unittest.main()
