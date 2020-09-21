import psycopg2.extras
from DBUtils.PooledDB import PooledDB
import threading
import sys


class DBOperator:
    _instance_lock = threading.Lock()

    def __init__(self):
        self.init_pool()

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            with DBOperator._instance_lock:
                if not hasattr(cls, '_instance'):
                    DBOperator._instance = object.__new__(cls)
                return DBOperator._instance

    def get_pool_conn(self):
        if not self._pool:
            self.init_pool()
        return self._pool.connection()

    def init_pool(self):
        try:
            pool = PooledDB(
                creator=psycopg2,
                maxconnections=6,
                mincached=1,
                maxcached=4,
                blocking=True,
                maxusage=None,
                setsession=[],
                host='47.98.184.202',
                port='5432',
                user='postgres',
                password='retail',
                database='retail')
            self._pool = pool
            print("succeed")
        except Exception as e:
            print(e)
            self.close_pool()

    def close_pool(self):
        if self._pool != None:
            self._pool.close()

    def SelectSql(self, sql):
        try:
            conn = self.get_pool_conn()
            cursor = conn.cursor()
            cursor.execute(sql)
            result = cursor.fetchall()
        except Exception as e:
            print('execute sql {0} is error'.format(sql))
            sys.exit('ERROR: load data from database error caused {0}'.format(str(e)))
        finally:
            cursor.close()
            conn.close()
        return result

    def InsertSql(self, sql, *args):
        try:
            conn = self.get_pool_conn()
            cursor = conn.cursor()
            cursor.execute(sql, args)
            result = True
        except Exception as e:
            print('ERROR: execute  {0} causes error'.format(sql))
            sys.exit('ERROR: update data from database error caused {0}'.format(str(e)))
        finally:
            cursor.close()
            conn.commit()
            conn.close()
        return result

    def UpdateSql(self, sql, *args):
        try:
            conn = self.get_pool_conn()
            cursor = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)
            cursor.execute(sql, args)
            result = True
        except Exception as e:
            print('ERROR: execute  {0} causes error'.format(sql))
            sys.exit('ERROR: update data from database error caused {0}'.format(str(e)))
        finally:
            cursor.close()
            conn.commit()
            conn.close()
        return result