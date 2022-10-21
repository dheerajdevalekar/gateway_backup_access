from datetime import datetime
from loguru import logger
from requests import get
from fastapi import APIRouter, HTTPException
from os import listdir, getcwd, getenv

router = APIRouter()
path_ = None
cloud_push_server_ip = "localhost"
cloud_push_port_num = 5001
panel_number_url = f"http://localhost:5001/gateway_detail"
is_created_new_file = True
cloud_push_previous_log_count = None

try:
    path_ = getenv(key="dmesg_folder_path")
    if path_ is None:
        path_ = f"{getcwd()}/dmesg_logs"
except Exception as error:
    print(str(error))


def get_inside_folders(folder_path: str):
    log_folder = None
    try:
        log_folder = listdir(folder_path)
    except Exception as e:
        print(str(e))
    finally:
        return log_folder


@router.get('/ls_dmsg_folder', tags=['DMESG'])
def get_list_of_de_msg_folder():
    try:
        count = 0
        folders_list = []
        ls_folder = get_inside_folders(folder_path=path_)
        if ls_folder is not None:
            for folders in ls_folder:
                folders_list.append(folders)
                count = count + 1
        list_all_folders = list(enumerate(folders_list, 1))
        return {
            "all_dates": list_all_folders,
            "num_all_keys": count
        }
    except Exception as e:
        return HTTPException(status_code=500, detail=f'{e}')


@router.get('/dmsg_logs', tags=['DMESG'])
def get_de_msg(user_file_name: str):
    try:
        count = 0
        all_logs = []
        ret_dict = {"all_logs": [], "count": 0}
        folder_contains = get_inside_folders(folder_path=path_)
        # TODO: This is for Display all file contains
        if user_file_name == "all":
            for files_ in folder_contains:
                file_path_ = f"{getcwd()}/dmesg_logs/{files_}"
                if file_path_ is not None:
                    log_file_txt = open(file_path_, "r")
                    log_lines = log_file_txt.readlines()
                    log_file_txt.close()
                    for each_line in log_lines:
                        all_logs.append(each_line)
                        count = count + 1
        # TODO: This is for Display file contains with specific file name
        else:
            if folder_contains is not None:
                for files in folder_contains:
                    if files == user_file_name:
                        file_path_ = f"{getcwd()}/dmesg_logs/{files}"
                        if file_path_ is not None:
                            log_file_txt = open(file_path_, "r")
                            log_lines = log_file_txt.readlines()
                            log_file_txt.close()
                            for each_line in log_lines:
                                all_logs.append(each_line)
                                count = count + 1
        ret_dict.update({"all_logs": all_logs, "count": count})
        raise HTTPException(status_code=200, detail=ret_dict)
    except HTTPException:
        raise
    except Exception as e:
        return HTTPException(status_code=500, detail=f'{e}')


def get_panel_number():
    panel_number = None
    try:
        res = get(panel_number_url)
        if res.status_code == 200:
            res_dict = res.json()
            panel_number = res_dict.get("a_panel_no")
        else:
            panel_number = get_mac_addr()
            logger.error(f"Panel Number NOT Found: {panel_number}")
    except Exception as e:
        panel_number = get_mac_addr()
        logger.error(f"{e}")
    finally:
        return panel_number


def get_mac_addr():
    try:
        return "MACCC"
    except Exception as e:
        logger.error(f"{e}")


@router.get('/dmsg_logs_send_cloud', tags=['DMESG on cloud'])
def send_dmesg_to_cloud():
    global is_created_new_file, cloud_push_previous_log_count
    try:
        is_panel_number = False
        dmesg_list = {}
        panel_number = get_panel_number()
        if is_panel_number:
            is_panel_number = True
        is_panel_number= False
        folder_contains = get_inside_folders(folder_path=path_)
        last_file_path = f"{getcwd()}/dmesg_logs/{max(folder_contains)}"
        last_log_file_txt = open(last_file_path, "r")
        log_lines = last_log_file_txt.readlines()
        last_log_file_txt.close()
        if cloud_push_previous_log_count is None:
            cloud_push_previous_log_count = len(log_lines)
            dmesg_list = {"panel_number": panel_number, "time_": datetime.now(), "total_dmesg_count": {len(log_lines)},
                          "is_created_new_file": is_created_new_file, "new_dmesg_count": len(log_lines), "dmesg_list": log_lines}
        else:
            if len(log_lines) > cloud_push_previous_log_count:
                updated_log_lines = log_lines[(cloud_push_previous_log_count - len(log_lines)):]
                dmesg_list = {"panel_number": panel_number, "time_": datetime.now(),
                              "total_dmesg_count": {len(log_lines)},
                              "is_created_new_file": is_created_new_file,
                              "new_dmesg_count": len(updated_log_lines),
                              "dmesg_list": updated_log_lines}
                cloud_push_previous_log_count = cloud_push_previous_log_count + len(updated_log_lines)
        if is_created_new_file:
            is_created_new_file = False
        return dmesg_list
    except HTTPException:
        raise
    except Exception as e:
        return HTTPException(status_code=500, detail=f'{e}')
