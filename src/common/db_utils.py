import pymysql
import yaml


class DatabaseConfig:
    def __init__(self, config_file):
        self.config_file = config_file
        with open(self.config_file, 'r') as file:
            config_data = yaml.safe_load(file)
            self.username = config_data.get('username')
            self.password = config_data.get('password')
            self.host = config_data.get('host')
            self.database = config_data.get('database')


def create_db_connection():
    """
    Assumes a config file exists in ../../../config/db_config.yaml (mithabrim/config/db_config.yaml)
    Create a database connection and return the connection object.
    Args:
        username (str): MySQL username.
        password (str): MySQL password.
        host (str): MySQL host.
        database (str): MySQL database name.
    Returns:
        sqlalchemy.engine.base.Connection: A database connection.
    """
    config_file_path = "../../config/db_config.yaml"
    db_config = DatabaseConfig(config_file_path)
    db = pymysql.connect(
        host=db_config.host,
        user=db_config.username,
        password=db_config.password,
        db=db_config.database
    )
    return db


def _format_val(val):
    if isinstance(val, UUID):
        return str(val)
    if isinstance(val, list):
        return [_format_val(x) for x in val]
    if isinstance(val, dict):
        return {k: _format_val(v) for k, v in val.items()}
    if isinstance(val, bytes):
        return val.decode("utf-8")
    return val


def execute_query(query, *args):
    args = [_format_val(arg) for arg in args]
    """ construct query with %s where the parameters are"""
    db = create_db_connection()
    try:
        cursor = db.cursor(cursor=pymysql.cursors.DictCursor)
        cursor.execute(query, args)
        results = cursor.fetchall()
        db.commit()
        return [_format_val(result) for result in results]
    except Exception as e:
        print(e)
        raise e
    finally:
        db.close()


def generic_insert(rows, table_name, raise_errors=True, ignore=False):
    if isinstance(rows, dict):
        rows = [rows]
    db = create_db_connection()
    try:
        cursor = db.cursor()
        sql = "{prefix} INTO {table_name} ({keys}) Values".format(
            prefix='INSERT IGNORE' if ignore else 'INSERT',
            table_name=table_name,
            keys=",".join(rows[0].keys()))
        values = []
        for row in rows:
            values.extend(row.values())
            values_placeholder = ",".join(["%s" for value in row.values()])
            sql += " ({values_placeholder}),".format(values_placeholder=values_placeholder)
        sql = sql[:-1]
        cursor.execute(sql, values)
        db.commit()
        return cursor.lastrowid
    except Exception as e:
        print(e)
        if raise_errors:
            raise e
    finally:
        db.close()