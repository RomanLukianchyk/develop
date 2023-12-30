from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from config import host, user, password, db_name

db_url = f"postgresql+psycopg2://{user}:{password}@{host}/{db_name}"
engine = create_engine(db_url, echo=True)
Session = sessionmaker(bind=engine)
session = Session()

try:
    # Проверка наличия пользователя Roman
    check_user_query = text("SELECT 1 FROM pg_roles WHERE rolname = 'Roman';")
    result = session.execute(check_user_query).scalar()

    if not result:
        # Создание пользователя Roman
        create_user_query = text("CREATE USER Roman WITH PASSWORD '12345';")
        session.execute(create_user_query)

        # Назначение роли суперпользователя
        grant_superuser_query = text("ALTER USER Roman WITH SUPERUSER;")
        session.execute(grant_superuser_query)

    # Предоставление привилегий
    grant_privileges_query = text("GRANT ALL PRIVILEGES ON DATABASE postgres TO Roman;")
    session.execute(grant_privileges_query)

    session.commit()

    print('[INFO] User created and privileges granted successfully')

except Exception as ex:
    print("[INFO] Error while working with PostgreSQL", ex)
    session.rollback()

finally:
    session.close()
    print("[INFO] PostgreSQL connection closed")
