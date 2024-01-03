from flask import Flask, request
from flask_restful import Resource, Api

from ORM import count_students_in_groups
from models import Base, engine, GroupModel, CourseModel, StudentModel, student_course_relation
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)
api = Api(app)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


class Groups(Resource):
    def get(self):
        max_students = request.args.get('max_students', default=1, type=int)
        groups = count_students_in_groups(max_students)
        return [{"name": group.name, "student_count": group.student_count} for group in groups]



class StudentsInCourse(Resource):
    def get(self, course_name=''):
        students = (
            session.query(StudentModel)
            .join(StudentModel.courses)
            .filter(CourseModel.name == course_name)
            .all()
        )
        return [{"id": student.id, "first_name": student.first_name, "last_name": student.last_name} for student in students]


class NewStudent(Resource):
    def get(self):
        group_id = request.args.get('group_id')
        first_name = request.args.get('first_name')
        last_name = request.args.get('last_name')

        if group_id is None or first_name is None or last_name is None:
            return {"message": "All parameters (group_id, first_name, last_name) are required"}, 400

        try:
            group_id = int(group_id)

            new_student = StudentModel(group_id=group_id, first_name=first_name, last_name=last_name)
            session.add(new_student)
            session.commit()

            return {"message": "New student added successfully"}

        except ValueError:
            return {"message": "Invalid group_id format"}, 400


class AddStudentToCourse(Resource):
    def post(self, student_id, course_id):
        try:
            student_id = int(student_id)
            course_id = int(course_id)

            student_to_add = session.query(StudentModel).get(student_id)
            course_to_add = session.query(CourseModel).get(course_id)

            if student_to_add and course_to_add:
                if course_to_add not in student_to_add.courses:
                    student_to_add.courses.append(course_to_add)
                    session.commit()
                    return {"message": "Student added to the course successfully"}
                else:
                    return {"message": "Student is already in the course"}
            else:
                return {"message": "Student or course not found"}

        except ValueError:
            return {"message": "Invalid student_id or course_id format"}, 400



class DeleteStudent(Resource):
    def delete(self, student_id):
        try:
            student_id = int(student_id)

            student_to_delete = session.query(StudentModel).get(student_id)

            if student_to_delete:
                session.delete(student_to_delete)
                session.commit()
                return {"message": "Student deleted successfully"}
            else:
                return {"message": "Student not found"}

        except ValueError:
            return {"message": "Invalid student_id format"}, 400

class RemoveStudentFromCourse(Resource):
    def delete(self, student_id, course_id):
        try:
            student_id = int(student_id)
            course_id = int(course_id)

            student_to_remove = session.query(StudentModel).get(student_id)
            course_to_remove = session.query(CourseModel).get(course_id)

            if student_to_remove and course_to_remove:
                if course_to_remove in student_to_remove.courses:
                    student_to_remove.courses.remove(course_to_remove)
                    session.commit()
                    return {"message": "Student removed from the course successfully"}
                else:
                    return {"message": "Student is not enrolled in the specified course"}
            else:
                return {"message": "Student or course not found"}

        except ValueError:
            return {"message": "Invalid student_id or course_id format"}, 400


api.add_resource(Groups, "/groups")
api.add_resource(StudentsInCourse, "/students-in-course", "/students-in-course/<string:course_name>")
api.add_resource(NewStudent, "/new-student")
api.add_resource(DeleteStudent, "/delete-student/<int:student_id>", methods=['DELETE'])
api.add_resource(AddStudentToCourse, "/add-student-to-course/<int:student_id>/<int:course_id>", methods=['POST'])
api.add_resource(RemoveStudentFromCourse, "/remove-student-from-course/<int:student_id>/<int:course_id>", methods=['DELETE'])



if __name__ == "__main__":
    app.run(debug=True)
