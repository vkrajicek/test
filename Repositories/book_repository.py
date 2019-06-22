from Classes.book import Book
from Classes.chapter import Chapter
from Repositories.chapter_repository import Chapter_repository


class Book_repository:
    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()

    def get_all(self):
        self.cursor.execute("SELECT * from projekt.book ;")
        records_book = self.cursor.fetchall()
        book_list = []
        for book in records_book:
            now_book = Book()
            now_book.id = book[0]
            now_book.user_id = book[1]
            now_book.name_of_the_book = book[2]
            now_book.author = book[3]
            now_book.edited_date = book[4]
            book_list.append(now_book)
        return book_list

    def get_all_by_user_id(self,user_id):
        self.cursor.execute("SELECT * from projekt.book  where user_id=%d;" % user_id)
        records_book = self.cursor.fetchall()
        book_list = []
        for book in records_book:
            now_book = Book()
            now_book.id = book[0]
            now_book.user_id = book[1]
            now_book.name_of_the_book = book[2]
            now_book.author = book[3]
            now_book.edited_date = book[4]
            book_list.append(now_book)
        return book_list

    def get_one_by_id(self, id):
        self.cursor.execute("SELECT * from projekt.book where id=%d ;" % id)
        records_book = self.cursor.fetchone()
        new_book = Book()
        new_book.id = records_book[0]
        new_book.chapter_name = records_book[1]
        new_book.edited_date = records_book[3]
        self.cursor.execute("SELECT chapter_id from projekt.book_chapter where book_id=%d ;" % id)
        chapters_ids = self.cursor.fetchall()
        self.cursor.execute("SELECT chapter_name from projekt.chapter where id in %d ;", (chapters_ids,))
        chapters=self.cursor.fetchall()
        chapters_list=[]
        for i in chapters:
            chapter=Chapter()
            chapter.chapter_name=i[0]
            chapters_list.append(chapter)
        new_book.chapters=chapters_list
        return new_book

    def rows_count_book(self):
        self.cursor.execute("SELECT count(*) from projekt.book ;")
        rows_count_book_1 = self.cursor.fetchall()
        rows_count_book_2 = rows_count_book_1[0]
        return rows_count_book_2

    def add_new_book(self, book, user_id):
        count=self.rows_count_book()
        postgres_insert_query_new_book = "INSERT INTO projekt.book (id,user_id, name_of_the_book, author) VALUES (%d, %d, %s, %s)"
        record_to_insert_new_book = (count[0] + 1, user_id, book.name_of_the_book, book.author)
        self.cursor.execute(postgres_insert_query_new_book, record_to_insert_new_book)
        chapter_repository=Chapter_repository(self.connection)
        self.connection.commit()
        chaper_ids_list=[]
        for i in book.chapters:
            chapter_id=chapter_repository.rows_count_chapter()
            postgres_insert_query_new_chapter = "INSERT INTO projekt.chapter (id, chapter_name, edited_date) VALUES (%d, %s, now()"
            record_to_insert_new_chapter = (chapter_id + 1, i.chapter_name)
            self.cursor.execute(postgres_insert_query_new_chapter, record_to_insert_new_chapter)
            self.connection.commit()
            chaper_ids_list.append(chapter_id + 1)
        self.cursor.execute("SELECT count(*) from projekt.book_chapter")
        book_chapters_id_count=self.cursor.fetchone()
        for i in chaper_ids_list:
            postgres_insert_query_new_book_and_chapters= "INSERT INTO projekt.book_chapter (id, book_id, edited_date, chapter_id) VALUES (%d, %d, now(), %d"
            record_to_insert_new_book_and_chapters=(book_chapters_id_count +1, book.id, i)
            self.cursor.execute(postgres_insert_query_new_book_and_chapters, record_to_insert_new_book_and_chapters)
            self.connection.commit()

    def book_delete(self, book_id):
        self.cursor.execute("SELECT chapter_id from projekt.book_chapter where book_id=%d ;" % book_id)
        chapters_id=self.cursor.fetchall()
        chapters_ids_list = []
        for i in chapters_id:
            chapters_ids_list.append(i[0])
        postgres_book_chapter_delete_query = ("DELETE from projekt.book_chapter where book_id=%d" % book_id)
        self.cursor.execute(postgres_book_chapter_delete_query)
        postgres_chapter_delete_query = ("DELETE from projekt.chapter where id in %d;", (chapters_ids_list, ))
        self.cursor.execute(postgres_chapter_delete_query)
        postgres_delete_query = "DELETE FROM projekt.book WHERE id = %s" % book_id
        self.cursor.execute(postgres_delete_query)
        self.connection.commit()

