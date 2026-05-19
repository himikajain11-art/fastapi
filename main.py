import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd

app = FastAPI()

CSV_FILE = "data.csv"

class employee(BaseModel):
    id: int
    name: str
    role: str
    department: str

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/csv-data")
def get_csv_data():
    if not os.path.exists(CSV_FILE):
        raise HTTPException(status_code=404, details="CSV file not found")
    
    df = pd.read_csv(CSV_FILE)
    return df.to_dict(orient="records")

@app.post("/csv-data")
def add_csv_data(employee: employee):
    #prepare the new row
    new_data = pd.DataFrame([employee.model_dump()])

    if os.path.exists(CSV_FILE):
        new_data.to_csv(CSV_FILE, mode="a", header=False, index=False)
    else:
        new_data.to_csv(CSV_FILE, mode="a", header=True, index=False)
    return {"message": "Data added successfully", "data":employee}

@app.get("/items/{items_id}")
def read_items(item_id: int, q:str | None = None):
    return {"items_id": item_id, "q": q}