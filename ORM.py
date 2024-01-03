from sqlalchemy.orm import sessionmaker
from models import GroupModel, CourseModel, StudentModel, engine
from sqlalchemy import func
Session = sessionmaker(bind=engine)
session = Session()



def count_students_in_groups(max_students=20):
    return (
        session.query(GroupModel.name, func.count(StudentModel.id).label('student_count'))
        .outerjoin(GroupModel.students)
        .group_by(GroupModel.id, GroupModel.name)
        .having(func.count(StudentModel.id) <= max_students)
        .all()
    )

def find_students_in_course(course_name=''):
    return (
        session.query(StudentModel)
        .join(StudentModel.courses)
        .filter(CourseModel.name == course_name)
        .all()
    )


def add_new_student(group_id, first_name, last_name):
    new_student = StudentModel(group_id=group_id, first_name=first_name, last_name=last_name)
    session.add(new_student)
    session.commit()
    print("[INFO] New student added successfully")


def delete_student_by_id(student_id):
    student_to_delete = session.query(StudentModel).get(student_id)
    if student_to_delete:
        session.delete(student_to_delete)
        session.commit()
        print("[INFO] Student deleted successfully")
    else:
        print("[INFO] Student not found")


def add_student_to_course(student_id, course_id):
    student_to_add = session.query(StudentModel).get(student_id)
    course_to_add = session.query(CourseModel).get(course_id)

    if student_to_add and course_to_add:
        if course_to_add not in student_to_add.courses:
            student_to_add.courses.append(course_to_add)
            session.commit()
            print("[INFO] Student added to the course successfully")
        else:
            print("[INFO] Student is already in the course")
    else:
        print("[INFO] Student or course not found")


def remove_student_from_course(student_id, course_id):
    student_to_remove = session.query(StudentModel).get(student_id)
    course_to_remove = session.query(CourseModel).get(course_id)

    if student_to_remove and course_to_remove:
        if course_to_remove in student_to_remove.courses:
            student_to_remove.courses.remove(course_to_remove)
            session.commit()
            print("[INFO] Student removed from the course successfully")
        else:
            print("[INFO] Student is not enrolled in the specified course")
    else:
        print("[INFO] Student or course not found")


# try:
#     print(count_students_in_groups())
#
# except Exception as ex:
#     print("[INFO] Error while working with PostgreSQL", ex)
#     session.rollback()
#
# finally:
#     session.close()
