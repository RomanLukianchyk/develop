import psycopg2
from faker import Faker
import random
import string
from config import host, user, password, db_name

fake = Faker()


def generate_group_name():
    numbers = random.randint(10, 99)
    letters = ''.join(random.choices(string.ascii_letters, k=2))
    return f'{letters}-{numbers}'


def generate_test_data():
    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name
    )

    try:
        with connection.cursor() as cursor:

            groups = [(generate_group_name(),) for _ in range(10)]
            cursor.executemany("INSERT INTO GroupModel (name) VALUES (%s) RETURNING id", groups)
            group_ids = [row[0] for row in cursor.fetchall()]

            courses_data = [
                ("Mathematics",),
                ("Biology",),
                ("Physics",),
                ("Chemistry",),
                ("History",),
                ("Literature",),
                ("Computer Science",),
                ("Art",),
                ("Economics",),
                ("Music",),
            ]
            cursor.executemany("INSERT INTO CourseModel (name) VALUES (%s) RETURNING id", courses_data)
            course_ids = [row[0] for row in cursor.fetchall()]

            first_names = [fake.first_name() for _ in range(20)]
            last_names = [fake.last_name() for _ in range(20)]
            students_data = []

            for _ in range(200):
                group_id = random.choice(group_ids)
                first_name = random.choice(first_names)
                last_name = random.choice(last_names)
                cursor.execute(
                    "INSERT INTO StudentModel (group_id, first_name, last_name) VALUES (%s, %s, %s) RETURNING id",
                    (group_id, first_name, last_name)
                )
                student_id = cursor.fetchone()[0] if cursor.rowcount > 0 else None
                students_data.append(student_id)

            student_course_data = []
            for student_id in students_data:
                num_courses = random.randint(1, 3)
                selected_courses = random.sample(course_ids, num_courses)
                for course_id in selected_courses:
                    student_course_data.append((student_id, course_id))

            for data in student_course_data:
                cursor.execute(
                    "INSERT INTO StudentCourseRelation (student_id, course_id) VALUES (%s, %s)",
                    data
                )

        connection.commit()

    except Exception as ex:
        print("[INFO] Error while working with PostgreSQL", ex)

    finally:
        connection.close()
        print("[INFO] PostgreSQL connection closed")


if __name__ == "__main__":
    generate_test_data()
