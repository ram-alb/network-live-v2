import os

import cx_Oracle
from network_live.atoll.sql_commands import atoll_selects, network_live_inserts


def execute_sql(sql_type, sql_command, sql_params=None):
    """
    Execute SQL commands on an Oracle database.

    Args:
        sql_type (str): The type of SQL command to execute ('delete', 'insert', or 'select').
        sql_command (str): The SQL command to be executed.
        sql_params (list, optional): Parameters for the SQL command, required for 'insert' type.

    Returns:
        list or None: If 'select' type, returns a list of tuples representing the query result.
            If 'delete' or 'insert' type, returns None.
    """
    atoll_dsn = cx_Oracle.makedsn(
        os.getenv('ATOLL_HOST'),
        os.getenv('ATOLL_PORT'),
        service_name=os.getenv('SERVICE_NAME'),
    )
    with cx_Oracle.connect(
        user=os.getenv('ATOLL_LOGIN'),
        password=os.getenv('ATOLL_PASSWORD'),
        dsn=atoll_dsn,
    ) as connection:
        cursor = connection.cursor()
        if sql_type == 'delete':
            cursor.execute(sql_command)
            connection.commit()
        elif sql_type == 'insert':
            cursor.executemany(sql_command, sql_params)
            connection.commit()
        elif sql_type == 'select':
            cursor.execute(sql_command)
            return cursor.fetchall()


def get_physical_params(technology):
    """
    Retrieve physical parameters of cells for a given technology.

    Args:
        technology (str): The technology for which physical parameters are to be retrieved.

    Returns:
        dict: A dictionary containing physical parameters for each cell.
    """
    atoll_data = execute_sql('select', atoll_selects[technology])
    physical_params = {}
    for cell in atoll_data:
        (
            cell_name,
            azimut,
            height,
            longitude,
            latitude,
        ) = cell
        physical_params[cell_name] = {
            'azimut': azimut,
            'height': height,
            'longitude': longitude,
            'latitude': latitude,
        }
    return physical_params


def update_network_live(cells, oss, technology):
    """
    Update the Network Live for a specific technology and Operational Support System (OSS).

    This function performs a two-step operation:
    1. Deletes existing records in the Network Live table for the specified technology and OSS.
    2. Inserts new records into the  Network Live table for the specified technology and OSS.

    Args:
        cells (list): List of cells to be inserted into the Network Live table.
        oss (str): Operational Support System identifier.
        technology (str): The technology for which the Netwrok Live data is to be updated

    Returns:
        str: A success or failure message indicating the result of the update operation.
    """
    network_live_tables = {
        'LTE': 'ltecells2',
        'WCDMA': 'wcdmacells2',
        'GSM': 'gsmcells2',
        'NR': 'nrcells',
    }

    delete_sql = "DELETE FROM {table} WHERE oss='{oss}'".format(
        table=network_live_tables[technology],
        oss=oss,
    )

    execute_sql('delete', delete_sql)
    try:
        execute_sql('insert', network_live_inserts[technology], cells)
    except cx_Oracle.Error:
        return f'{technology} {oss} Fail'
    return f'{technology} {oss} Success'
