from application.models import Base, engine


def create_tables():
    try:
        Base.metadata.create_all(engine)
        print('[INFO] Tables created successfully')
    except Exception as e:
        print(f'[ERROR] Failed to create tables: {e}')



if __name__ == "__main__":
    create_tables()