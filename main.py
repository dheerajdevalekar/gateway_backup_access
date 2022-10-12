from loguru import logger
from os import getcwd, system, path
from datetime import datetime, time
from uvicorn import run
from fastapi import FastAPI
from src.routes.list_demsg import router as ls_dmesg
from src.routes.previous_logs import router as prev_logs
from src.routes.online_sqlite_browser import router as online_sqlite_browser
from _thread import start_new_thread

app = FastAPI(title=f"Gateway Backup Solution")

app.include_router(ls_dmesg)
app.include_router(prev_logs)
app.include_router(online_sqlite_browser)


@app.on_event("startup")
async def init_process():
    try:
        logger.info(f"Gateway Backup Solution STARTS with PORT: 5008")
        start_new_thread(main, ())
    except Exception as e:
        logger.error(f"{e}")


def main():
    try:
        path_ = f"{getcwd()}/dmesg_logs"
        curr_time = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")  # This strftime is used to Filter out the Microseconds from Main Time
        cmd = f"dmesg -w -H > {path_}/{curr_time}.txt"
        if path.exists(path_) is True:
            logger.info(f"{path_} Folder Already Exist")
            system(cmd)
        else:
            system(f"mkdir {path_}")
            logger.info(f"{path_} Folder Created")
            system(cmd)
    except Exception as e:
        logger.error(f"{e}")


if __name__ == '__main__':
    run("main:app", host="0.0.0.0", port=5008, reload=True)
