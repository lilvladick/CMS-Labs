from fastapi import FastAPI,File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from all_labs.lab_1.second_task import get_trends
from all_labs.lab_1.first_task import maximize_profit
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.post("/lab_1/get_trends/")
async def trends_endpoint(file: UploadFile = File(...)):
    contents = await file.read()
    with open("data.csv", "wb") as f:
        f.write(contents)
    return {"image_url": get_trends("data.csv")}

@app.post("/lab_1/maximize_profit/")
async def maximize_profit_endpoint(data: dict):
    result = maximize_profit(json.dumps(data))
    return json.loads(result)
