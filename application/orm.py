from sqlalchemy import func
from sqlalchemy.orm import Session
from application.models import GroupModel, CourseModel, StudentModel


class Repository:
    def __init__(self, session: Session):
        self.session = session

    def count_students_in_groups(self, max_students=20):
        return (
            self.session.query(GroupModel.name, func.count(StudentModel.id).label('student_count'))
            .outerjoin(GroupModel.students)
            .group_by(GroupModel.id, GroupModel.name)
            .having(func.count(StudentModel.id) <= max_students)
            .all()
        )
    def find_students_in_course(self, course_name=''):
        return (
            self.session.query(StudentModel)
            .join(StudentModel.courses)
            .filter(CourseModel.name == course_name)
            .all()
        )

    def add_new_student(self, group_id, first_name, last_name):
        new_student = StudentModel(group_id=group_id, first_name=first_name, last_name=last_name)
        self.session.add(new_student)
        self.session.commit()
        print("[INFO] New student added successfully")

    def delete_student_by_id(self, student_id):
        student_to_delete = self.session.query(StudentModel).get(student_id)
        if student_to_delete:
            self.session.delete(student_to_delete)
            self.session.commit()
            print("[INFO] Student deleted successfully")
        else:
            print("[INFO] Student not found")

    def add_student_to_course(self, student_id, course_id):
        student_to_add = self.session.query(StudentModel).get(student_id)
        course_to_add = self.session.query(CourseModel).get(course_id)

        if student_to_add and course_to_add:
            if course_to_add not in student_to_add.courses:
                student_to_add.courses.append(course_to_add)
                self.session.commit()
                print("[INFO] Student added to the course successfully")
            else:
                print("[INFO] Student is already in the course")
        else:
            print("[INFO] Student or course not found")

    def remove_student_from_course(self, student_id, course_id):
        student_to_remove = self.session.query(StudentModel).get(student_id)
        course_to_remove = self.session.query(CourseModel).get(course_id)

        if student_to_remove and course_to_remove:
            if course_to_remove in student_to_remove.courses:
                student_to_remove.courses.remove(course_to_remove)
                self.session.commit()
                print("[INFO] Student removed from the course successfully")
            else:
                print("[INFO] Student is not enrolled in the specified course")
        else:
            print("[INFO] Student or course not found")
