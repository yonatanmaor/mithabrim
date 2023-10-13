from dataclasses import asdict

from sqlalchemy import text

from common import db_utils
from entities.needs_and_initiatives import Organization


def select_from_needs_and_initiatives():
    query = "SELECT * FROM needs_and_initiatives"
    results = db_utils.execute_query(query)
    return results


def insert_organzation(entity: Organization):
    db_utils.generic_insert(rows=[asdict(entity)], table_name='organizations')


def insert_needs_and_initiative_test():
    query = "INSERT INTO mehubarim.needs_and_initiatives (org_name) VALUES (:org_name);"

    try:
        params = {'org_name': 'abcd'}
        connection = db_utils.create_db_connection()
        connection.execute(text(query), params)
        # result = db_utils.execute_query(query, params=params, expect_affected_rows=True)
        # return result
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    # results = select_from_needs_and_initiatives()
    insert_needs_and_initiative_test()
    # print(results)