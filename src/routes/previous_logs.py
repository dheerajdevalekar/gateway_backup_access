from fastapi import APIRouter, HTTPException
from os import environ, listdir

router = APIRouter()


log_path = None
try:
    log_path = environ["LOG_PATH"]
except:
    log_path = f"/home/pi/iam-gateway/logs"


def get_inside_folders(folder_path: str):
    try:
        log_folder = listdir(folder_path)
        if len(log_folder) > 0:
            return log_folder
        else:
            return None
    except:
        return None


@router.get('/ls_prev_date', tags=['logs'])
def get_list_of_prev_date():
    try:
        prev_date_list = []
        log_folder = get_inside_folders(folder_path=log_path)
        if log_folder is not None:
            for folders in log_folder:
                prev_date_list.append(folders)
        return prev_date_list
    except Exception as e:
        raise e


@router.get('/ls_prev_log', tags=['logs'])
def get_list_of_previous_logs(
        usr_date: str
):
    try:
        all_logs = []
        counter = 0
        log_folder = get_inside_folders(folder_path=log_path)
        if log_folder is not None:
            if usr_date in log_folder:
                log_fetch_path = f"{log_path}/{usr_date}"
                logs_file_folders = get_inside_folders(folder_path=log_fetch_path)
                for folder in logs_file_folders:
                    actual_log_file_path = f"{log_fetch_path}/{folder}/log.log"
                    log_file_txt = open(actual_log_file_path, "r")
                    log_lines = log_file_txt.readlines()
                    log_file_txt.close()
                    for each_line in log_lines:
                        all_logs.append(each_line)
                        counter = counter + 1
            return {
                    "all_logs": all_logs,
                    "log_length": counter,
                    "date": usr_date
                   }
    except Exception as e:
        raise e
