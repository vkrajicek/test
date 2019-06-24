from Classes.book import Book
from Classes.chapter import Chapter
from Repositories.chapter_repository import Chapter_repository


class Book_repository:
    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()
    # get all data from book table
    def get_all(self):
        self.cursor.execute("SELECT * from projekt.book ;")
        records_book = self.cursor.fetchall()
        if records_book != None:
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
        else:
            return None
    # get all data from bok table accoring to user_id
    def get_all_by_user_id(self, user_id):
        if user_id == None:
            return None
        self.cursor.execute("SELECT * from projekt.book  where user_id=%d;" % user_id)
        records_book = self.cursor.fetchall()
        if len(records_book) == 0:
            return None
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
    # getcone row of data from book table according to id
    def get_one_by_id(self, id):
        self.cursor.execute("SELECT * from projekt.book where id=%d ;" % id)
        records_book = self.cursor.fetchone()
        if records_book != None:
            new_book = Book()
            new_book.id = records_book[0]
            new_book.user_id = records_book[1]
            new_book.name_of_the_book = records_book[2]
            new_book.author = records_book[3]
            new_book.edited_date = records_book[4]
            self.cursor.execute("SELECT chapter_id from projekt.book_chapter where book_id=%d ;" % id)
            chapters_ids = self.cursor.fetchall()
            if len(chapters_ids) >0:
                chapters_ids_list=[]
                for i in chapters_ids:
                    chapters_ids_list.append(int(i[0]))
                select_query="SELECT chapter_name from projekt.chapter where id in %s ;" % chapters_ids_list
                select_query=select_query.replace("[", "(")
                select_query=select_query.replace("]", ")")
                self.cursor.execute(select_query)
                chapters=self.cursor.fetchall()
                if len(chapters) >0:
                    chapters_list=[]
                    for i in chapters:
                        chapter=Chapter()
                        chapter.chapter_name=i[0]
                        chapters_list.append(chapter)
                    new_book.chapters=chapters_list
                    return new_book
                else:
                    return new_book
            else:
                return new_book
        else:
            return None
    # find the biggest id from book table for latter use
    def rows_count_book(self):
        self.cursor.execute("SELECT max(id) from projekt.book ;")
        rows_count_book_1 = self.cursor.fetchall()
        rows_count_book_2 = rows_count_book_1[0]
        if rows_count_book_2[0]==None:
            return 0
        return rows_count_book_2[0]
    # added new book into book, chapter and book_chapter tables
    def add_new_book(self, book):
        count=self.rows_count_book()
        if book == None or book.id == None or book.user_id == None or book.name_of_the_book == None or book.author == None:
            return None
        insert_query_new_book = "INSERT INTO projekt.book (id,user_id, name_of_the_book, \"Author\", edited_date) VALUES (%s, %s, %s, %s, now())"
        record_to_insert_new_book = (int(count) + 1, int(book.user_id), book.name_of_the_book, book.author)
        book.id=int(count) + 1
        self.cursor.execute(insert_query_new_book, record_to_insert_new_book)
        self.connection.commit()
        chapter_repository = Chapter_repository(self.connection)
        chapter_ids_list=[]
        for i in book.chapters:
            if i.chapter_name == None:
                continue
            chapter_id=chapter_repository.rows_count_chapter()
            postgres_insert_query_new_chapter = "INSERT INTO projekt.chapter (id, chapter_name, edited_date) VALUES (%s, %s, now())"
            record_to_insert_new_chapter = (int(chapter_id) + 1, i.chapter_name)
            self.cursor.execute(postgres_insert_query_new_chapter, record_to_insert_new_chapter)
            self.connection.commit()
            chapter_ids_list.append(int(chapter_id) + 1)
        self.cursor.execute("SELECT max(id) from projekt.book_chapter")
        book_chapters_id_count=self.cursor.fetchone()
        book_chaper_id=int(book_chapters_id_count[0])
        for i in chapter_ids_list:
            book_chaper_id=book_chaper_id+1
            postgres_insert_query_new_book_and_chapters= "INSERT INTO projekt.book_chapter (id, book_id, chapter_id, edited_date) VALUES (%s, %s, %s, now())"
            record_to_insert_new_book_and_chapters=(book_chaper_id, int(book.id), int(i))
            self.cursor.execute(postgres_insert_query_new_book_and_chapters, record_to_insert_new_book_and_chapters)
            self.connection.commit()
        return book
    # deleted one book from book_chapter, chapter and book tables
    def book_delete(self, book_id):
        if book_id==None:
            return None
        self.cursor.execute("SELECT chapter_id from projekt.book_chapter where book_id=%d ;" % book_id)
        chapters_id=self.cursor.fetchall()
        chapters_ids_list = []
        for i in chapters_id:
            chapters_ids_list.append(i[0])
        postgres_book_chapter_delete_query = ("DELETE from projekt.book_chapter where book_id=%d" % book_id)
        self.cursor.execute(postgres_book_chapter_delete_query)
        postgres_chapter_delete_query = ("DELETE from projekt.chapter where id = %d;" % chapters_ids_list[0])
        self.cursor.execute(postgres_chapter_delete_query)
        postgres_delete_query = "DELETE FROM projekt.book WHERE id = %s" % book_id
        self.cursor.execute(postgres_delete_query)
        self.connection.commit()
