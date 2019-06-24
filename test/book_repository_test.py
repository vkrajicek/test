import unittest
import psycopg2

from Classes.book import Book
from Classes.chapter import Chapter
from Repositories.book_repository import Book_repository


class Book_repository_test(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.connection=psycopg2.connect(user="postgres",
                                    password="Aquapark4",
                                    host="localhost",
                                    port="5432",
                                    database="test")
        self.book_repository=Book_repository(self.connection)
        self.cursor = self.connection.cursor()
        self.cursor.execute("insert into projekt.book values(1, 1,'Johny Knoxville', 'Ja', now()) ;")
        self.cursor.execute("insert into projekt.book_chapter values(1, 1,now(),1 ) ;")
        self.cursor.execute("insert into projekt.chapter values(1, 'Som bozi',now()) ;")
        self.cursor.execute("insert into projekt.book values(2, 2,'tomas matonoha', 'ferdinant', now()) ;")
        self.cursor.execute("insert into projekt.book values(3, 3,'cook book', 'Margita', now()) ;")
        self.cursor.execute("insert into projekt.book_chapter values(3, 3,now(),3 ) ;")
        self.cursor.execute("insert into projekt.chapter values(2, 'Meat',now()) ;")

        self.connection.commit()

    def test_get_all(self):
        result=self.book_repository.get_all()
        self.assertGreater(len(result), 0)

    # def test_get_all_not_valid(self):
    #     result=self.book_repository.get_all()
    #     self.assertEqual(len(result), 0)

    def test_get_all_by_user_id_valid(self):
        result = self.book_repository.get_all_by_user_id(1)
        self.assertGreater(len(result), 0)

    def test_get_all_by_user_id_negative(self):
        result = self.book_repository.get_all_by_user_id(-1)
        self.assertEqual(result, None)

    def test_get_all_by_user_id_none(self):
        result = self.book_repository.get_all_by_user_id(None)
        self.assertEqual(result, None)

    def test_get_one_by_id_no_chapters(self):
        books=self.book_repository.get_one_by_id(2)
        self.assertEqual(books.name_of_the_book, 'tomas matonoha')
        self.assertEqual(books.author, 'ferdinant')
        self.assertEqual(books.id, 2)
        self.assertEqual(books.user_id, 2)
        self.assertEqual(len(books.chapters), 0)

    def test_get_one_by_id_valid(self):
        books=self.book_repository.get_one_by_id(1)
        self.assertEqual(books.name_of_the_book, 'Johny Knoxville')
        self.assertEqual(books.author, 'Ja')
        self.assertEqual(books.id, 1)
        self.assertEqual(books.user_id, 1)
        self.assertEqual(len(books.chapters), 1)

    def test_get_one_by_id_negative(self):
        result=self.book_repository.get_one_by_id(-1)
        self.assertEqual(result, None)

    def test_rows_count_book(self):
        count=self.book_repository.rows_count_book()
        self.assertGreater(count, 0)

    # def test_rows_count_book_not_valid(self):
    #     count=self.book_repository.rows_count_book()
    #     self.assertEqual(count, 0)

    def test_add_new_book_valid(self):
        book=Book()
        book.id=4
        book.user_id=4
        book.name_of_the_book='Python for beginners'
        book.author='Jaroslav Sochan'
        chapter_1=Chapter()
        chapter_1.chapter_name='First chapter'
        chapter_2=Chapter()
        chapter_2.chapter_name='Second chapter'
        book.chapters.append(chapter_1)
        book.chapters.append(chapter_2)
        result_book=self.book_repository.add_new_book(book)
        result=self.book_repository.get_one_by_id(result_book.id)
        self.assertNotEqual(result, None)
        self.assertEqual(result.id, book.id)
        self.assertEqual(result.user_id, book.user_id)
        self.assertEqual(result.name_of_the_book, book.name_of_the_book)
        self.assertEqual(len(result.chapters), len(book.chapters))

    def test_add_new_book_none(self):
        result=self.book_repository.add_new_book(None)
        self.assertEqual(result, None)

    def test_add_new_book_one_book_parameter_none(self):
        book=Book()
        book.id=5
        book.user_id=None
        book.name_of_the_book='Python for someone'
        book.author='Bc. Jaroslav Sochan'
        book_test=self.book_repository.add_new_book(book)
        self.assertEqual(book_test, None)

    def test_add_new_book_one_chapter_parameter_none(self):
        book=Book()
        book.id=5
        book.user_id=5
        book.name_of_the_book='Python for adults'
        book.author='ing. Jaroslav Sochan'
        chapter_1=Chapter()
        chapter_1.chapter_name='First chapter'
        chapter_2=Chapter()
        chapter_2.chapter_name=None
        book.chapters.append(chapter_1)
        book.chapters.append(chapter_2)
        book_test=self.book_repository.add_new_book(book)
        self.assertNotEqual(book_test, None)
        result=self.book_repository.get_one_by_id(book_test.id)
        self.assertNotEqual(result, None)
        self.assertEqual(result.id, book.id)
        self.assertEqual(result.user_id, book.user_id)
        self.assertEqual(result.name_of_the_book, book.name_of_the_book)
        self.assertEqual(len(result.chapters), 1)

    def test_book_delete_valid(self):
        book=Book()
        book.id=6
        book.user_id=6
        book.name_of_the_book='Mr. Fantastic'
        book.author='Reed Richards'
        chapter_1=Chapter()
        chapter_1.chapter_name='First chapter'
        chapter_2=Chapter()
        chapter_2.chapter_name='Second chapter'
        book.chapters.append(chapter_1)
        book.chapters.append(chapter_2)
        self.book_repository.add_new_book(book)

        self.book_repository.book_delete(6)
        books=self.book_repository.get_one_by_id(6)
        self.assertEqual(books, None)

    def test_book_delete_none_parameter(self):
        result=self.book_repository.book_delete(None)
        self.assertEqual(result, None)
