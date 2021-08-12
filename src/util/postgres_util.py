from contextlib import contextmanager

import psycopg2.pool

from config import config
from src.util.log_util import logger

POOL = psycopg2.pool.SimpleConnectionPool(
    minconn=10,
    maxconn=20,
    host=config.PG_HOST,
    port=int(config.PG_PORT),
    database=config.PG_DBNAME,
    user=config.PG_USER,
    password=config.PG_PASSWORD)


@contextmanager
def get_conn():
    conn = POOL.getconn()
    try:
        yield conn
        conn.commit()
    except Exception as e:
        logger.error(e)
        conn.rollback()
    finally:
        POOL.putconn(conn)


@contextmanager
def get_cursor():
    with get_conn() as conn:
        yield conn.cursor()
