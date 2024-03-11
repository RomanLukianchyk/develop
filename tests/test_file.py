import unittest
from application.app import app
from application.orm import Repository
import requests
import json

BASE_URL = 'http://127.0.0.1:5000'


class TestGroupsEndpoint:

    @staticmethod
    def test_get_group_valid_id():
        response = requests.get(f'{BASE_URL}/groups/1')
        assert response.status_code == 200


    @staticmethod
    def test_get_group_invalid_id():
        response = requests.get(f'{BASE_URL}/groups/asda')
        assert response.status_code == 404


def test_new_student():
    response = requests.post(f'{BASE_URL}/new-student/Jon/Dhoe4/3')
    assert response.status_code == 200
    response = requests.post(f'{BASE_URL}/new-student/')
    assert response.status_code == 404

class TestDeleteStudentEndpoint:

    @staticmethod
    def test_delete_existing_student():
        response = requests.delete(f'{BASE_URL}/delete-student/201')
        assert response.status_code == 200

    @staticmethod
    def test_delete_nonexistent_student():
        response = requests.delete(f'{BASE_URL}/delete-student/99999')
        assert response.status_code == 200
        data = response.json()
        assert data == {'message': 'Student not found'}

    @staticmethod
    def test_delete_student_invalid_id():
        response = requests.delete(f'{BASE_URL}/delete-student/asd')
        assert response.status_code == 404
        try:
            data = response.json()
            assert data == {'message': 'Student not found'}
        except json.JSONDecodeError:
            pass



def test_add_student_to_course():
    responce = requests.post(f'{BASE_URL}/add-student-to-course/199/3')
    assert responce.status_code == 200

def test_remove_student_from_course():
    response = requests.delete(f'{BASE_URL}/remove-student-from-course/199/3')
    assert response.status_code == 200


class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def tearDown(self):
        pass

    def test_create_tables_endpoint(self):
        response = self.app.post('/create-tables')
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertIn('Tables created successfully', data['message'])

    def test_create_testdata_endpoint(self):
        response = self.app.post('/create-testdata')
        data = response.get_json()


        self.assertEqual(response.status_code, 200)
        self.assertIn('Test data created successfully', data['message'])



if __name__ == '__main__':
    unittest.main()