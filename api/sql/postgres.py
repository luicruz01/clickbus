import traceback
import sys

import psycopg2
import psycopg2.extras

from api.utils import setup_logger

logger = setup_logger('pg_connection')


class PostgresConn(object):

    def __init__(self, conn_str, conn_key):
        self.conn_str = conn_str
        self.conn = None
        self.conn_key = conn_key

    def __del__(self):
        if self.conn:
            self.conn.close()
            self.conn = None
    
    def close(self):
        if self.conn:
            self.conn.close()
            self.conn = None

    def __connect(self):
        return psycopg2.connect(self.conn_str)

    def execute(self, *args, **kwargs):
        query = kwargs.get('query', None) if len(args) < 1 else args[0]
        params = kwargs.get('params', False) if len(args) < 2 else args[1]
        commit = kwargs.get('commit', False)
        fetch = kwargs.get('fetch', True)
        returning = kwargs.get('returning', False)
        rollback = kwargs.get('rollback', False)
        cursor_dict = kwargs.get('cursor_dict', False)
        if self.conn is None:
            self.conn = self.__connect()
            # self.conn.rollback()
            # self.conn.commit()
        try:
            if cursor_dict:
                cur = self.conn.cursor(
                    cursor_factory=psycopg2.extras.RealDictCursor
                )
            else:
                cur = self.conn.cursor()

            if query:
                if params:
                    cur.execute(query, params)
                else:
                    cur.execute(query)
            if returning:
                self.conn.commit()
                return cur.fetchall()
            if commit:
                return self.conn.commit()
            if fetch:
                return cur.fetchall()
            if rollback:
                return self.conn.rollback()
        except Exception as ex:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            logger.error("%s:%s" %
                (str(ex), ''.join(
                    traceback.format_exception(exc_type, exc_value, exc_traceback)))
            )
            self.conn = None
            self.conn = self.__connect()
            if kwargs.get('retry', False):
                raise ex
            kwargs['retry'] = True
            self.execute(*args, **kwargs)

        return True
