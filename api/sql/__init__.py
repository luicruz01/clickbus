from flask import g, Flask, current_app
import os
from api.sql.postgres import PostgresConn

# Please keep it short, even if all classes have lazy db connections (they must!).
CONNECTIONS = {
    'test': (PostgresConn, "dbname='postgres' user='postgres' host='127.0.0.1' password='pg1234' options='-c statement_timeout=2500'")
}

env_value = os.environ.get('LOCAL_DOCKER',False)
if env_value:
    CONNECTIONS['tracking'] =  CONNECTIONS['test']

app = Flask(__name__)


class SQLConnection(object):
    """ Keep reference to the conn object
    """

    def __new__(cls, conn_key):
        """
            Opens a new database connection if there is none yet for the current application context.
            :return: Postgres Database connection
        """
        with app.app_context():
            if not hasattr(g, 'postgres_db'):
                g.postgres_db = {}
            if conn_key not in g.postgres_db:
                g.postgres_db[conn_key] = CONNECTIONS[conn_key][0](CONNECTIONS[conn_key][1], conn_key)
            return g.postgres_db[conn_key]


def close_db(error=None):
    """Closes the database again at the end of the request."""
    with app.app_context():
        if hasattr(g, 'postgres_db'):
            for k, v in g.postgres_db.iteritems():
                g.postgres_db[v].close()
