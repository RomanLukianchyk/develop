import psycopg2
from config import host, user, password, db_name


def create_tables():
    connection = None
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        connection.autocommit = True

        with connection.cursor() as cursor:
            cursor.execute(open("create_tables.sql", "r").read())
            print('[INFO] Tables created successfully')

    except Exception as ex:
        print("[INFO] Error while working with PostgreSQL", ex)

    finally:
        if connection:
            connection.close()
            print("[INFO] PostgreSQL connection closed")


if __name__ == "__main__":
    create_tables()
