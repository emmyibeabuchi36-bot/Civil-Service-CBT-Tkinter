from dataclasses import dataclass
from typing import Optional

@dataclass
class User:
    id: int
    username: str
    role: str
    full_name: str

@dataclass
class Question:
    id: int
    question_text: str
    option_a: str
    option_b: str
    option_c: str
    option_d: str
    correct_answer: str
    category: str = "General"

@dataclass
class ExamResult:
    score: int
    total: int
    percentage: float
    grade: str
    passed: bool
    taken_at: Optional[str] = None
