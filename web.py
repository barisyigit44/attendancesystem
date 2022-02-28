from fastapi import FastAPI , Request
from fastapi.responses import HTMLResponse
import psycopg2
from jinja2 import Environment, FileSystemLoader

app = FastAPI()

db = psycopg2.connect(
    database="your_db_name",
    user="your_database_user_name",
    password="pass",
    host="localhost"
)
@app.get("/attendance")
async def root():

    curr = db.cursor()
    curr.execute("SELECT users.name , users.surname , users.schoolid , attendance.lastlogin FROM attendance INNER JOIN users ON attendance.account_id = users.id")
    record = curr.fetchall()
    file_loader = FileSystemLoader('./')
    env = Environment(loader=file_loader)
    template = env.get_template("index.html")
    output = template.render(record=record)
    return HTMLResponse(output)
    
@app.get("/account")
async def root():

    curr = db.cursor()
    curr.execute("SELECT * FROM users ")
    record = curr.fetchall()
    file_loader = FileSystemLoader('./')
    env = Environment(loader=file_loader)
    template = env.get_template("index.html")
    output = template.render(record=record)
    return HTMLResponse(output)

@app.get("/count")
async def root():
    curr = db.cursor()
    curr.execute("SELECT users.schoolid, users.name, users.surname , COUNT(attendance.account_id) from attendance INNER JOIN users ON attendance.account_id = users.id GROUP BY users.schoolid, users.name, users.surname ")
    record = curr.fetchall()
    file_loader = FileSystemLoader('./')
    env = Environment(loader=file_loader)
    template = env.get_template("index.html")
    output = template.render(record=record)
    return HTMLResponse(output)

