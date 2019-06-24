import unittest
import psycopg2

from Classes.chapter import Chapter
from Repositories.chapter_repository import Chapter_repository


class Chapter_repository_test(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.connection=psycopg2.connect(user="postgres",
                                    password="Aquapark4",
                                    host="localhost",
                                    port="5432",
                                    database="test")
        self.chapter_repository=Chapter_repository(self.connection)
        self.cursor = self.connection.cursor()
        self.cursor.execute("insert into projekt.book values(1, 1,'Johny Knoxville', 'Ja', now()) ;")
        self.cursor.execute("insert into projekt.book_chapter values(1, 1,now(),1 ) ;")
        self.cursor.execute("insert into projekt.chapter values(1, 'Som bozi',now()) ;")

    def test_get_all(self):
        result=self.chapter_repository.get_all()
        self.assertGreater(len(result), 0)

    def test_get_one_by_id_valid(self):
        chapters=self.chapter_repository.get_one_by_id(1)
        self.assertEqual(chapters.id, 1)
        self.assertEqual(chapters.chapter_name, 'Som bozi')

    def test_get_one_by_id_id_none(self):
        result=self.chapter_repository.get_one_by_id(None)
        self.assertEqual(result, None)

    def test_get_one_by_id_id_negative(self):
        result=self.chapter_repository.get_one_by_id(-1)
        self.assertEqual(result, None)

    def test_get_one_by_id_id_not_valid(self):
        result=self.chapter_repository.get_one_by_id(50)
        self.assertEqual(result, None)

    def test_rows_count_chapter(self):
        count=self.chapter_repository.rows_count_chapter()
        self.assertGreater(len(count), 0)

    def test_add_new_chapter_valid(self):
        chapter=Chapter()
        chapter.chapter_name='First chapter'
        self.chapter_repository.add_new_chapter(chapter,1)
        result=self.chapter_repository.get_one_by_id(2)
        self.assertEqual(result.chapter_name, 'First chapter')

    def test_add_new_chapter_none_user_id_none(self):
        chapters=self.chapter_repository.add_new_chapter(None,None)
        self.assertEqual(chapters, None)

    def test_add_new_chapter_one_parameter_none(self):
        chapter=Chapter()
        chapter.chapter_name= None
        chapter_test=self.chapter_repository.add_new_chapter(chapter,1)
        self.assertEqual(chapter_test, None)
        result=self.chapter_repository.get_one_by_id(chapter.id)
        self.assertEqual(result, None)

    def test_chapter_delete_valid(self):
        chapter=Chapter()
        chapter.chapter_name='Second chapter'
        self.chapter_repository.add_new_chapter(chapter,1)
        self.chapter_repository.chapter_delete(3)

    def test_chapter_delete_none_parameter(self):
        result=self.chapter_repository.chapter_delete(None)
        self.assertEqual(result, None)