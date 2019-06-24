import unittest
import psycopg2

from Repositories.chapter_repository import Chapter_repository


class Chapter_repository_test(unittest.TestCase):

    def setUp(self):
        self.connection = psycopg2.connect(user="postgres",
                                           password="Aquapark4",
                                           host="localhost",
                                           port="5432",
                                           database="test")
        self.chapter_repository = Chapter_repository(self.connection)

    def test_chapter_repository(self):
        chapters = self.chapter_repository.get_all()
        self.assertEqual(len(chapters), 0)

    # def tearDown(self):
    #

