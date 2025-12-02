from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db import init_db, get_db

app = FastAPI()

# ◾ Allow Frontend Access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ◾ Init DB on Start
init_db()

@app.get("/")
def root():
    return {"message": "Leaflet API is running"}

@app.get("/buildings")
def get_buildings():
    con = get_db()
    cur = con.cursor()
    cur.execute("SELECT * FROM buildings")
    data = [dict(row) for row in cur.fetchall()]
    return {"data": data}

@app.post("/buildings")
def add_building(name: str, lat: float, lng: float, height: float):
    con = get_db()
    cur = con.cursor()
    cur.execute(
        "INSERT INTO buildings (name, lat, lng, height) VALUES (?, ?, ?, ?)",
        (name, lat, lng, height)
    )
    con.commit()
    return {"message": "Added!"}
