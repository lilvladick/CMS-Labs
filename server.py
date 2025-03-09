import threading
import asyncio
import json
from fastapi import FastAPI, File, UploadFile, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from all_labs.lab_1.second_task import get_trends
from all_labs.lab_1.first_task import maximize_profit
from all_labs.lab_2.drown_balls import drown_balls
from all_labs.lab_3.golden_selection import golden_selection_scipy
from all_labs.lab_3.newton import newton
from all_labs.lab_5.simpy_version.telephone_line import TelephoneLine
from all_labs.lab_5.simpy_version.service_stantion import ServiceStation

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

simulation_instance = None

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

@app.post("/lab_2/drown_balls/")
async def drown_balls_endpoint(data: dict):
    return {"image_url": drown_balls(json.dumps(data))}

@app.get("/lab_3/golden_selection/")
async def extrema_endpoint():
    result = golden_selection_scipy()
    return JSONResponse(content=result)

@app.get("/lab_3/newton/")
async def analyze_endpoint():
    result = newton()
    return JSONResponse(content=result)


@app.post("/lab_5/telephone_line_simulation/")
async def phone_simulation_endpoint():
    global simulation_instance
    
    simulation_instance = TelephoneLine(sim_time=1000000, arrival_rate=0.95, service_time=1.0, seed=42)
    
    thread = threading.Thread(target=simulation_instance.run)
    thread.start()
    
    return {"message": "Telephone simulation started"}


@app.post("/lab_5/service_station_simulation")
async def service_station_endpoint(request: dict):
    """Запускает симуляцию и возвращает начальные результаты"""
    global simulation_instance

    sim_time_hours = 1000
    arrival_rate = 0.95
    service_time = 1.0
    n_posts = 3
    queue_limit = 5 if request.get("queue_limit") == "true" else None

    simulation_instance = ServiceStation(sim_time_hours, arrival_rate, service_time, n_posts, queue_limit=queue_limit)
    
    thread = threading.Thread(target=simulation_instance.run_simulation)
    thread.start()

    return {"message": "Simulation started"}


@app.websocket("/ws/telephone_line_simulation")
async def websocket_phone_simulation(websocket: WebSocket):
    """
    Веб-сокет, отправляющий клиенту обновления состояния симуляции.
    Клиент получает данные каждые 0.1 секунды.
    """
    await websocket.accept()
    try:
        while True:
            if simulation_instance is not None:
                data = simulation_instance.get_state()
                await websocket.send_json(data)
                if data.get("finished"):
                    break
            await asyncio.sleep(0.1)
    except Exception as e:
        print("WebSocket connection closed", e)
        
@app.websocket("/ws/service_station_simulation")
async def websocket_service_station_simulation(websocket: WebSocket):
    """
    Веб-сокет, отправляющий клиенту обновления состояния симуляции.
    Клиент получает данные каждые 0.1 секунды.
    """
    await websocket.accept()
    try:
        while True:
            if simulation_instance is not None:
                data = simulation_instance.get_state()
                await websocket.send_json(data)
                if data.get("total") == data.get("served") + data.get("lost"): 
                    break
            await asyncio.sleep(0.1)
    except Exception as e:
        print("WebSocket connection closed", e)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)