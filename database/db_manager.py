import pyodbc
import os
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

class DatabaseManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self.conn_str = (
            f"DRIVER={os.getenv('AZURE_SQL_DRIVER')};"
            f"SERVER={os.getenv('AZURE_SQL_SERVER')};"
            f"DATABASE={os.getenv('AZURE_SQL_DATABASE')};"
            f"UID={os.getenv('AZURE_SQL_USERNAME')};"
            f"PWD={os.getenv('AZURE_SQL_PASSWORD')}"
        )

    def get_connection(self):
        return pyodbc.connect(self.conn_str)

    def init_db(self):
        """Jadvallarni yaratish"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            # Talabalar jadvali
            cursor.execute("""
                IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'RatingStudents')
                CREATE TABLE RatingStudents (
                    ID INT PRIMARY KEY IDENTITY(1,1),
                    FullName NVARCHAR(100) NOT NULL,
                    Major NVARCHAR(50),
                    CreatedDate DATETIME DEFAULT GETDATE()
                )
            """)
            # Fanlar jadvali
            cursor.execute("""
                IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'RatingCourses')
                CREATE TABLE RatingCourses (
                    ID INT PRIMARY KEY IDENTITY(1,1),
                    Name NVARCHAR(100) NOT NULL,
                    Credits INT NOT NULL
                )
            """)
            # Baholar jadvali
            cursor.execute("""
                IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'RatingGrades')
                CREATE TABLE RatingGrades (
                    ID INT PRIMARY KEY IDENTITY(1,1),
                    StudentID INT FOREIGN KEY REFERENCES RatingStudents(ID),
                    CourseID INT FOREIGN KEY REFERENCES RatingCourses(ID),
                    Grade FLOAT NOT NULL
                )
            """)
            conn.commit()

    def get_all_data_for_pandas(self):
        """Barcha baholarni Pandas DataFrame ko'rinishida olish"""
        query = """
            SELECT g.StudentID as student_id, g.Grade as grade, c.Credits as credits
            FROM RatingGrades g
            JOIN RatingCourses c ON g.CourseID = c.ID
        """
        with self.get_connection() as conn:
            return pd.read_sql(query, conn)

    def get_students_with_names(self):
        query = "SELECT ID, FullName, Major FROM RatingStudents"
        with self.get_connection() as conn:
            return pd.read_sql(query, conn)
