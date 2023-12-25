import psycopg2
from config import host, user, password, db_name


def create_user_with_privileges():
    connection = None
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name,
        )

        connection.autocommit = True

        with connection.cursor() as cursor:
            cursor.execute("CREATE USER Roman WITH PASSWORD '12345';")
            print('[INFO] User created successfully')
            cursor.execute("GRANT ALL PRIVILEGES ON DATABASE postgres TO Roman")
            print('[INFO] Privileges granted successfully')

    except Exception as ex:
        print("[INFO] Error while working with PostgreSQL", ex)

    finally:
        if connection:
            connection.close()
            print("[INFO] PostgreSQL connection closed")


if __name__ == "__main__":
    create_user_with_privileges()
