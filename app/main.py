import logging
from datetime import date, timedelta
from pathlib import Path

from fastapi import FastAPI

log_path = Path("/var/log/fastapi_app")
log_folder = log_path / "logs" if log_path.exists() else Path("logs")
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


@app.get("/generate_log/{num_logs}")
def generate_log(num_logs: int):
    for i in range(num_logs):
        logging.info(f"Generate logs {i}")
    return {"Log generation is done."}


@app.get("/generate_log_folders/{num_folders}")
def generate_log_folders(num_folders: int):
    logger = logging.getLogger()

    previous_handlers = logger.handlers.copy()
    logger.handlers.clear()

    create_file_handlers(num_folders, logger)
    for i in range(5000):
        logger.info(f"Hello, world {i}!")

    logger.handlers.clear()
    logger.handlers = previous_handlers

    return {"Log folder generation is done."}


def create_file_handlers(num_folders: int, logger: logging.Logger):
    """Create logging file handlers that log inside different folders

    Args:
        num_folders (int): Number of folders to create
        logger (Logger): Logger instance to which logging handlers are added
    """
    child_folder = log_folder
    today = date.today()
    for i in range(num_folders):
        child_folder = log_folder / str(today + timedelta(days=i))
        child_folder.mkdir(parents=True, exist_ok=True)

        filename = str(child_folder / "my.log")
        file_handler = logging.FileHandler(filename)
        logger.addHandler(file_handler)
