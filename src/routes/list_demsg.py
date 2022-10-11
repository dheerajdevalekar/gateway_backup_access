from fastapi import APIRouter, HTTPException
from os import listdir, getcwd, getenv

router = APIRouter()
path_ = None

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
