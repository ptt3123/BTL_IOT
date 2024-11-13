import asyncio, json
import paho.mqtt.client as mqtt
from contextlib import asynccontextmanager
from datetime import datetime
from fastapi import FastAPI, WebSocket, Request, Query
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from crud import *


ws: list[WebSocket] = []
cnt = 0
data_hw = {"type": "hw", "fan": "off", "led": "off", "con": "off"}

def on_connect(mqttclient, userdata, flags, rc):
    print("Kết nối thành công với mã: " + str(rc))
    mqttclient.subscribe("psensor")
    mqttclient.subscribe("pfan")
    mqttclient.subscribe("pled")
    mqttclient.subscribe("pcon")

def on_message(mqttclient, userdata, msg):
    data: dict = json.loads(msg.payload.decode())
    global data_hw
    if msg.topic == "psensor":
        global cnt
        cnt += 1
        if cnt == 5:
            # create_data(data)
            cnt = 0

        data.update({"tim": datetime.now().strftime("%H:%M:%S")})

    else:
        create_action(data)
        data_hw.update({data.get("hw"): data.get("act")})
        data = data_hw

    asyncio.run_coroutine_threadsafe(message_queue.put(data), loop)



client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect('192.168.1.8', 1883)
client.loop_start()


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    client.loop_stop()
    client.disconnect()


app = FastAPI(lifespan=lifespan)
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")
message_queue = asyncio.Queue()
loop = asyncio.get_event_loop()


@app.get("/home", response_class=HTMLResponse)
async def home_get(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


@app.get("/bai5", response_class=HTMLResponse)
async def home_get(request: Request):
    return templates.TemplateResponse("bai5.html", {"request": request})


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    ws.append(websocket)
    global data_hw
    global client
    await websocket.send_text(json.dumps(data_hw))
    while True:
        try:
            data = await asyncio.wait_for(websocket.receive_text(), timeout=1.0)
            data = json.loads(data)
            hw = data.get("hw")
            if data_hw.get(hw) == "off":
                client.publish(f"s{hw}", "on")
            else:
                client.publish(f"s{hw}", "off")

        except asyncio.TimeoutError:
            pass

        data = await message_queue.get()
        await websocket.send_text(json.dumps(data))


@app.get("/database", response_class=HTMLResponse)
async def database_get(request: Request):

    return templates.TemplateResponse(
        "database.html",
        {"request": request}
    )


@app.get("/api/database")
async def get_data(txt: str = Query(default=""),
                   item: str = Query(default=""), order = Query(default=""),
                   pagesize: int = Query(default=20), page: int = Query(default=1)):

    txt = txt.replace("T", " ")
    lst, total_items = read_data(txt, pagesize, page, item, order)
    return {"data": lst, "total": total_items}


@app.get("/actionHistory", response_class=HTMLResponse)
async def action_history_get(request: Request):

    return templates.TemplateResponse(
        "actionHistory.html",
        {"request": request}
    )


@app.get("/api/actionHistory")
async def get_action_history(txt: str = Query(default=""),
                    item: str = Query(default=""), order = Query(default=""),
                   pagesize: int = Query(default=20), page: int = Query(default=1)):

    txt = txt.replace("T", " ")
    lst, total_items = read_action(txt, pagesize, page, item, order)
    return {"data": lst, "total": total_items}


@app.get("/portfolio", response_class=HTMLResponse)
async def portfolio_get(request: Request):
    return templates.TemplateResponse("portfolio.html", {"request": request})