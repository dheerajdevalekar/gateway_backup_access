from loguru import logger
from fastapi import APIRouter, HTTPException
from src.access_db import db_dict, db_conn, db_tables_name, query_with_limit, user_query_output, write_db_with_api, refresh

router = APIRouter()
db_path = None


@router.get(path='/tables', tags=['Online SQLite Browser'])
def view_table_names():
    try:
        raise HTTPException(status_code=200, detail=db_tables_name)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"{e}")
        raise HTTPException(status_code=401, detail=e)


@router.get(path='/table_data', tags=['Online SQLite Browser'])
def get_total_table_data(table_name: str, limit: int = 100):
    try:
        data = query_with_limit(table_name=table_name, limit=limit)
        if data.get('operation_status') is True:
            raise HTTPException(status_code=200, detail=data)
        else:
            raise HTTPException(status_code=400, detail=data)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"{e}")
        raise HTTPException(status_code=401, detail=e)


@router.post(path='/db_path', tags=['Online SQLite Browser'])
def set_db_path(user_db_path: str):
    from src.access_db import db_path
    global db_path
    is_refresh = False
    exception = {"status_code": 0, "detail": None}
    try:
        response = write_db_with_api(path=user_db_path)
        if response.get("result"):
            is_refresh = True
            exception.update({"status_code": 200, "detail": f'{response.get("detail")}'})
            raise HTTPException(status_code=exception.get("status_code"), detail=f'{exception.get("detail")} | Refresh-Status: {is_refresh}')
    except HTTPException:
        if is_refresh:
            refresh()
            raise
        else:
            raise
    except Exception as e:
        logger.error(f"{e}")
        raise HTTPException(status_code=401, detail=e)


@router.get(path='/query/output', tags=['Online SQLite Browser'])
def ls_user_query(user_query: str):
    try:
        data = user_query_output(query=user_query)
        if data.get('operation_status') is True:
            raise HTTPException(status_code=200, detail=data)
        else:
            raise HTTPException(status_code=400, detail=data)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"{e}")
        raise HTTPException(status_code=401, detail=e)