import string
from sqlalchemy.orm import sessionmaker
from application.models import GroupModel, CourseModel, StudentModel, engine
from faker import Faker
import random

fake = Faker()

def generate_group_name():
    numbers = random.randint(10, 99)
    letters = ''.join(random.choices(string.ascii_letters, k=2))
    return f'{letters}-{numbers}'

def generate_test_data():
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        groups = [GroupModel(name=generate_group_name()) for _ in range(10)]
        session.add_all(groups)
        session.flush()

        courses = [CourseModel(name=name) for name in ["Mathematics", "Biology", "Physics", "Chemistry", "History",
                                                       "Literature", "Computer Science", "Art", "Economics", "Music"]]
        session.add_all(courses)
        session.flush()

        students = [StudentModel(
            group_id=random.choice(groups).id,
            first_name=fake.first_name(),
            last_name=fake.last_name()
        ) for _ in range(200)]
        session.add_all(students)
        session.flush()

        for student in students:
            num_courses = random.randint(1, 3)
            selected_courses = random.sample(courses, num_courses)
            student.courses.extend(selected_courses)

        session.commit()

    except Exception as ex:
        print("[INFO] Error while working with PostgreSQL", ex)

    finally:
        session.close()
        print("[INFO] PostgreSQL connection closed")


if __name__ == "__main__":
    generate_test_data()
