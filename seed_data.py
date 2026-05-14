from database.db_manager import DatabaseManager
import random

def seed():
    db = DatabaseManager()
    db.init_db()
    
    with db.get_connection() as conn:
        cursor = conn.cursor()
        
        # 1. Talabalar
        students = [
            ("Aziz Karimov", "Software Engineering"),
            ("Malika Ergasheva", "Data Science"),
            ("Jasur Rahimov", "Cyber Security")
        ]
        for s in students:
            cursor.execute("INSERT INTO RatingStudents (FullName, Major) VALUES (?, ?)", s)
        
        # 2. Fanlar (Kreditlari bilan)
        courses = [
            ("Mathematics", 5),
            ("Programming", 6),
            ("Database Systems", 4),
            ("Physics", 3)
        ]
        for c in courses:
            cursor.execute("INSERT INTO RatingCourses (Name, Credits) VALUES (?, ?)", c)
        
        # 3. Baholar (Har bir talabaga barcha fanlardan baho qo'yamiz)
        cursor.execute("SELECT ID FROM RatingStudents")
        student_ids = [row[0] for row in cursor.fetchall()]
        
        cursor.execute("SELECT ID FROM RatingCourses")
        course_ids = [row[0] for row in cursor.fetchall()]
        
        for s_id in student_ids:
            for c_id in course_ids:
                grade = random.randint(60, 100)
                cursor.execute("INSERT INTO RatingGrades (StudentID, CourseID, Grade) VALUES (?, ?, ?)", (s_id, c_id, grade))
        
        conn.commit()
    print("Ma'lumotlar muvaffaqiyatli yuklandi!")

if __name__ == "__main__":
    seed()
