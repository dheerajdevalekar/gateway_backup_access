import sqlite3
from loguru import logger
from time import sleep
from os import getcwd
from json import loads, dumps
from datetime import datetime
db_dict = {}
db_conn = None
db_tables_name = []

db_path = None

try:
    config_file_ = open(f"{getcwd()}/config.json", "r+")
    config_data = loads(config_file_.read())
    db_path = config_data.get('db_path')
    logger.info(f"DB Path Set From config File, path: {db_path}")
    config_file_.close()
    pass
except:
    logger.critical(f"Database PATH is not SET")


def write_db_with_api(path: str):
    config_file = None
    operation_data = {"result": False, "detail": None}
    try:
        config_file = open(f"{getcwd()}/config.json", "w")
        config_file.flush()
        config_file.write(dumps({"db_path": path}))
        operation_data.update({"result": True, "detail": f"Database path will update from {db_path} to {path}"})
    except Exception as e:
        operation_data.update({"result": False, "detail": f"{e}"})
    finally:
        if config_file is not None:
            config_file.close()
        return operation_data


def refresh():
    restart_file = None
    restart_flag = False
    logger.warning(f"Database PATH is SET, now trying to REFRESH......!!!!!!")
    try:
        restart_file = open(f"{getcwd()}/restart.py", "w")
        restart_file.flush()
        restart_file.write(f"Gateway_Refresh_Time = {str(datetime.now().date())}-{str(datetime.now().time().replace(microsecond=0)).replace(':', '-')}\n")
        restart_flag = True
        return restart_flag
    except:
        restart_flag = False
    finally:
        if restart_file is not None:
            restart_file.close()
        return restart_flag


def get_all_table_names():
    global db_tables_name
    try:
        db_cur = db_conn.cursor()
        raw_table_names = db_cur.execute(f'''select * from sqlite_master''').fetchall()
        for tables in raw_table_names:
            db_tables_name.append(tables[1])
        if len(db_tables_name) > 0:
            logger.info(f"Added {len(db_tables_name)} Table Name")
        else:
            logger.warning(f"Failed to Add Table Name")
        db_cur.close()
    except Exception as e:
        logger.error(f"{e}")


def query_with_limit(table_name, limit):
    ret_data = {"operation_status": False, "msg": None, "table_columns": None, "query_ret_data": None}
    db_cur = None
    try:
        if table_name in db_tables_name:
            cols_name = []
            db_cur = db_conn.cursor()
            cols_data = db_cur.execute(f'''SELECT * FROM {table_name}''').description
            for cols in cols_data:
                cols_name.append(cols[0])
            data = db_cur.execute(f'''SELECT * FROM {table_name} limit {limit}''').fetchall()
            ret_data.update({"operation_status": True, "msg": "Table Found", "table_columns": cols_name, "query_ret_data": data})
        else:
            ret_data.update({"operation_status": False, "msg": "No Table Found", "table_columns": None, "query_ret_data": None})
    except Exception as e:
        db_conn.rollback()
        logger.error(f"{e} | Trying to Rollback")
    finally:
        if db_cur is not None:
            db_cur.close()
        return ret_data


def user_query_output(query: str):
    ret_data = {"operation_status": False, "msg": None, "table_columns": None, "query_ret_data": None}
    db_cur = None
    try:
        db_cur = db_conn.cursor()
        result = db_cur.execute(f'{query}').fetchall()
        ret_data.update({"operation_status": True, "msg": "Operation Successfully", "table_columns": [], "query_ret_data": result})
    except Exception as e:
        db_conn.rollback()
        logger.error(f"{e} | Trying to Rollback")
    finally:
        if db_cur is not None:
            db_cur.close()
        return ret_data


try:
    if db_path is not None:
        # Create a SQL connection to our SQLite database
        db_conn = sqlite3.connect(f"{db_path}", check_same_thread=False)
        # db_cur = db_conn.cursor()
        if db_conn is not None:
            logger.info(f"Database connection Successfully Created")
            get_all_table_names()
        else:
            logger.warning(f"Database NOT Connected")
    else:
        sleep(1)
except Exception as error:
    if db_conn is not None:
        db_conn.close()
    logger.error(f"{error}")
