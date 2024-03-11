from flask import jsonify, request
from flask_restful import Resource
from application.models import CourseModel, StudentModel, GroupModel

class Groups(Resource):
    def __init__(self, repository, session):
        self.repository = repository
        self.session = session

    def get(self, max_students=20):
        groups = self.repository.count_students_in_groups(max_students)
        return jsonify([{"name": group.name, "student_count": group.student_count} for group in groups])




class StudentsInCourse(Resource):
    def __init__(self, session):
        self.session = session

    def get(self, course_name=''):
        students = (
            self.session.query(StudentModel)
            .join(StudentModel.courses)
            .filter(CourseModel.name == course_name)
            .all()
        )
        return [{"id": student.id, "first_name": student.first_name, "last_name": student.last_name} for student in students]


class NewStudent(Resource):
    def __init__(self, session):
        self.session = session

    def post(self, first_name, last_name, group_id):
        try:
            group_id = int(group_id)
            new_student = StudentModel(group_id=group_id, first_name=first_name, last_name=last_name)
            self.session.add(new_student)
            self.session.commit()

            return {"message": f"New student added successfully: Student id {new_student.id}"}

        except ValueError:
            return {"message": "Invalid group_id format"}, 400

class AddStudentToCourse(Resource):
    def __init__(self, session):
        self.session = session

    def post(self, student_id, course_id):
        try:
            student_id = int(student_id)
            course_id = int(course_id)

            student_to_add = self.session.query(StudentModel).get(student_id)
            course_to_add = self.session.query(CourseModel).get(course_id)

            if student_to_add and course_to_add:
                if course_to_add not in student_to_add.courses:
                    student_to_add.courses.append(course_to_add)
                    self.session.commit()
                    return {"message": "Student added to the course successfully"}
                else:
                    return {"message": "Student is already in the course"}
            else:
                return {"message": "Student or course not found"}

        except ValueError:
            return {"message": "Invalid student_id or course_id format"}, 400

class DeleteStudent(Resource):
    def __init__(self, session):
        self.session = session

    def delete(self, student_id):
        try:
            student_id = int(student_id)

            student_to_delete = self.session.query(StudentModel).get(student_id)

            if student_to_delete:
                self.session.delete(student_to_delete)
                self.session.commit()
                return {"message": "Student deleted successfully"}
            else:
                return {"message": "Student not found"}

        except ValueError:
            return {"message": "Invalid student_id format"}, 400

class RemoveStudentFromCourse(Resource):
    def __init__(self, session):
        self.session = session

    def delete(self, student_id, course_id):
        try:
            student_id = int(student_id)
            course_id = int(course_id)

            student_to_remove = self.session.query(StudentModel).get(student_id)
            course_to_remove = self.session.query(CourseModel).get(course_id)

            if student_to_remove and course_to_remove:
                if course_to_remove in student_to_remove.courses:
                    student_to_remove.courses.remove(course_to_remove)
                    self.session.commit()
                    return {"message": "Student removed from the course successfully"}
                else:
                    return {"message": "Student is not enrolled in the specified course"}
            else:
                return {"message": "Student or course not found"}

        except ValueError:
            return {"message": "Invalid student_id or course_id format"}, 400

