from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from database.db_manager import DatabaseManager
from models.core import RatingEngine
import pandas as pd
import uvicorn

app = FastAPI(title="Talabalar Reyting Tizimi")

# Static va Templates papkalarini ulash
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

db = DatabaseManager()

@app.on_event("startup")
async def startup():
    db.init_db()

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    # 1. Ma'lumotlarni bazadan olamiz
    grades_df = db.get_all_data_for_pandas()
    students_df = db.get_students_with_names()
    
    # 2. Pandas orqali reytingni hisoblaymiz
    if not grades_df.empty:
        ratings_df = RatingEngine.calculate_weighted_gpa(grades_df)
        
        # Talaba ismlari bilan birlashtiramiz
        final_df = pd.merge(students_df, ratings_df, left_on='ID', right_on='student_id', how='left')
        final_df['weighted_gpa'] = final_df['weighted_gpa'].fillna(0).round(2)
        
        # Reyting bo'yicha saralaymiz
        final_df = final_df.sort_values(by='weighted_gpa', ascending=False)
        ranking = final_df.to_dict(orient='records')
    else:
        ranking = []

    return templates.TemplateResponse("index.html", {"request": request, "ranking": ranking})

# Ma'lumot qo'shish uchun sodda routelar (Keyinchalik UI dan chaqiriladi)
@app.post("/add_student")
async def add_student(full_name: str = Form(...), major: str = Form(...)):
    with db.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO RatingStudents (FullName, Major) VALUES (?, ?)", (full_name, major))
        conn.commit()
    return RedirectResponse(url="/", status_code=303)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
