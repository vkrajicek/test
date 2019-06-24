import unittest
import psycopg2

from Classes.subject import Subject
from Repositories.subject_repository import Subject_repository


class Subject_repository_test(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.connection=psycopg2.connect(user="postgres",
                                    password="Aquapark4",
                                    host="localhost",
                                    port="5432",
                                    database="test")
        self.subject_repository=Subject_repository(self.connection)
        self.subject = self.connection.cursor()
        self.subject.execute("insert into projekt.subject values(1,'Czech Language', 'Iveta Krajickova', 'Annual results', now()) ;")
        self.subject.execute("insert into projekt.user values (1,'Vito', 'Krajicek', 'Vito', 123, now(), now()) ;")

    def test_get_all_valid(self):
        result=self.subject_repository.get_all()
        self.assertGreater(len(result), 0)

    # def test_get_all_not_valid(self):
    #     result=self.subject_repository.get_all()
    #     self.assertEqual(len(result), 0)

    def test_get_one_by_id_valid(self):
        subject=self.subject_repository.get_one_by_id(1)
        self.assertEqual(subject.id, 1)
        self.assertEqual(subject.subject, 'Czech Language')
        self.assertEqual(subject.teacher, 'Iveta Krajickova')
        self.assertEqual(subject.method_of_course_completion, 'Annual results')

    def test_get_one_by_id_id_none(self):
        result=self.subject_repository.get_one_by_id(None)
        self.assertEqual(result, None)

    def test_get_one_by_id_id_negative(self):
        result=self.subject_repository.get_one_by_id(-1)
        self.assertEqual(result, None)

    def test_get_one_by_id_id_not_valid(self):
        result=self.subject_repository.get_one_by_id(50)
        self.assertEqual(result, None)

    def test_rows_count_chapter_valid(self):
        count=self.subject_repository.rows_count_subject()
        self.assertGreater(count, 0)

    # def test_rows_count_chapter_not_valid(self):
    #     count=self.subject_repository.rows_count_subject()
    #     self.assertEqual(count, 0)

    def test_add_new_subject_valid(self):
        subject=Subject()
        subject.id = 2
        subject.subject = 'Drawing'
        subject.teacher = 'Johny English'
        subject.method_of_course_completion = 'Annual results'
        self.subject_repository.add_new_subject(subject, 2, 15, 2)
        result=self.subject_repository.get_one_by_id(2)
        self.assertEqual(result.subject, 'Drawing')

    def test_add_new_subject_parameter_not_valid(self):
        subject=Subject()
        subject.id = 3
        subject.subject = 'physical education'
        subject.teacher =  None
        subject.method_of_course_completion = 'Annual results'
        self.subject_repository.add_new_subject(subject, 2, 14, 1)
        result=self.subject_repository.get_one_by_id(3)
        self.assertEqual(result, None)

    def test_add_new_subject_subject_parameter_not_valid(self):
        subject=Subject()
        subject.id = 3
        subject.subject = 'physical education'
        subject.teacher =  None
        subject.method_of_course_completion = 'Annual results'
        self.subject_repository.add_new_subject(subject, None, 14, 1)
        result=self.subject_repository.get_one_by_id(3)
        self.assertEqual(result, None)

    def test_subject_delete_valid(self):
        subject=Subject()
        subject.id = 4
        subject.subject = 'physical education 2'
        subject.teacher =  'John Brutal'
        subject.method_of_course_completion = 'Annual results'
        self.subject_repository.add_new_subject(subject, 2, 14, 1)
        self.subject_repository.subject_delete(4)

    def test_subject_delete_none_parameter(self):
        result=self.subject_repository.subject_delete(None)
        self.assertEqual(result, None)


