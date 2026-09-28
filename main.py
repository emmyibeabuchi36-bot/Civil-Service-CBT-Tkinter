from app.database import Database
from app.auth import AuthenticationService
from app.questions import QuestionBank
from app.exam import ExamEngine
from app.results import ResultService
from app.admin import AdminService
from app.gui import CBTApplication

def build_application():
    db=Database(); bank=QuestionBank(db); auth=AuthenticationService(db); exam=ExamEngine(db,bank); results=ResultService(db); admin=AdminService(bank,results)
    return CBTApplication(db,auth,bank,exam,results,admin)

if __name__ == "__main__":
    build_application().mainloop()
