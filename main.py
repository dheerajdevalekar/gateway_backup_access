from loguru import logger
from os import getcwd, system, path
from datetime import datetime


def main():
    try:
        path_ = f"{getcwd()}/dmsg_logs"
        curr_time = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")  # This strftime is used to Filter out the Microseconds from Main Time
        cmd = f"dmesg -w > {path_}/{curr_time}.txt"
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
    main()
