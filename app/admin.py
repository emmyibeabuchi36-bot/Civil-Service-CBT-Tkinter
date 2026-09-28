class AdminService:
    def __init__(self, question_bank, result_service): self.question_bank, self.result_service = question_bank, result_service
    def add_question(self, text,a,b,c,d,correct,category):
        if not all(x.strip() for x in [text,a,b,c,d,correct]): raise ValueError("Complete all required fields.")
        if correct.upper() not in {"A","B","C","D"}: raise ValueError("Correct answer must be A, B, C or D.")
        self.question_bank.add(text,a,b,c,d,correct,category)
    def delete_question(self, question_id): self.question_bank.delete(question_id)
