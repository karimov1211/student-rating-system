import pandas as pd
from typing import List, Dict

class Student:
    def __init__(self, student_id: int, full_name: str, major: str):
        self.student_id = student_id
        self.full_name = full_name
        self.major = major
        self.grades = []

    def to_dict(self):
        return {
            "id": self.student_id,
            "full_name": self.full_name,
            "major": self.major
        }

class Course:
    def __init__(self, course_id: int, name: str, credits: int):
        self.course_id = course_id
        self.name = name
        self.credits = credits # Vazni

class RatingEngine:
    @staticmethod
    def calculate_weighted_gpa(grades_df: pd.DataFrame) -> pd.DataFrame:
        """
        Pandas orqali vaznli GPA hisoblash.
        Formula: sum(grade * credits) / sum(credits)
        """
        if grades_df.empty:
            return pd.DataFrame(columns=['student_id', 'weighted_gpa'])
        
        # Har bir fan uchun vaznli ballni hisoblaymiz
        grades_df['weighted_score'] = grades_df['grade'] * grades_df['credits']
        
        # Talabalar kesimida jamlaymiz
        grouped = grades_df.groupby('student_id').agg({
            'weighted_score': 'sum',
            'credits': 'sum'
        })
        
        # GPA ni hisoblaymiz
        grouped['weighted_gpa'] = grouped['weighted_score'] / grouped['credits']
        
        return grouped[['weighted_gpa']].reset_index()
