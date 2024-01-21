from flask import Flask, jsonify
from flask_restful import Api
from application.create_tables import create_tables
from application.generate_testdata import generate_test_data
from application.orm import Repository
from application.models import engine
from sqlalchemy.orm import sessionmaker
from application.requests import Groups, StudentsInCourse, NewStudent, DeleteStudent, AddStudentToCourse, RemoveStudentFromCourse

app = Flask(__name__)
api = Api(app)

Session = sessionmaker(bind=engine)
session = Session()
repository = Repository(session)


@app.route('/create-tables', methods=['POST'])
def handle_create_tables():
    create_tables()
    return jsonify({"message": "Tables created successfully"})


@app.route('/create-testdata', methods=['POST'])
def handle_create_testdata():
    generate_test_data()
    return jsonify({"message": "Test data created successfully"})


api.add_resource(Groups, "/groups/<int:max_students>", resource_class_args=(repository, session), methods=['GET'])
api.add_resource(StudentsInCourse, "/students-in-course", "/students-in-course/<string:course_name>", resource_class_args=(session,))
api.add_resource(NewStudent, "/new-student/<string:first_name>/<string:last_name>/<int:group_id>", resource_class_args=(session,), methods=['POST'])
api.add_resource(DeleteStudent, "/delete-student/<int:student_id>", resource_class_args=(session,), methods=['DELETE'])
api.add_resource(AddStudentToCourse, "/add-student-to-course/<int:student_id>/<int:course_id>", resource_class_args=(session,), methods=['POST'])
api.add_resource(RemoveStudentFromCourse, "/remove-student-from-course/<int:student_id>/<int:course_id>", resource_class_args=(session,), methods=['DELETE'])
