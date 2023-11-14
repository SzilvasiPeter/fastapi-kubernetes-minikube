import logging
from pathlib import Path

from fastapi import FastAPI

log_path = Path("/var/log/fastapi_app")
filename = str(log_path / "my.log") if log_path.exists() else "my.log"
logging.basicConfig(
    filename=filename,
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
app = FastAPI()


@app.get("/")
def read_root():
    logging.info("Inside the `read_root` function.")
    return {"Hello": "World"}


@app.get("/item/{item_id}")
def read_item(item_id: int):
    item_message = "This is the item message."
    logging.info(f"The item_id is the following: {item_id}")
    return {"item_id": item_id, "item_message": item_message}


@app.get("/generate_log/{iteration}")
def generate_log(iteration: int):
    for i in range(iteration):
        logging.info(f"Generate logs {i}")
    return {"Log generation is done."}
