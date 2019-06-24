from Classes.chapter import Chapter


class Chapter_repository:
    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()

    def get_all(self):
        self.cursor.execute("SELECT * from projekt.chapter ;")
        records_chapter = self.cursor.fetchall()
        if records_chapter != None:
            chapter_list = []
            for chapter in records_chapter:
                now_chapter = Chapter()
                now_chapter.id = chapter[0]
                now_chapter.chapter_name = chapter[1]
                now_chapter.edited_date = chapter[2]
                chapter_list.append(now_chapter)
            return chapter_list
        else:
            return None

    def get_one_by_id(self, id):
        if id == None or id < 0:
            return None
        self.cursor.execute("SELECT * from projekt.chapter where id=%d ;" % id)
        records_chapter = self.cursor.fetchone()
        if records_chapter == None:
            return None
        now_chapter = Chapter()
        now_chapter.id = records_chapter[0]
        now_chapter.chapter_name = records_chapter[1]
        now_chapter.edited_date = records_chapter[2]
        return now_chapter

    def rows_count_chapter(self):
        self.cursor.execute("SELECT max(id) from projekt.chapter ;")
        rows_count_chapter_1 = self.cursor.fetchall()
        rows_count_chapter_2 = rows_count_chapter_1[0]
        if rows_count_chapter_2[0]==None:
            return 0
        return rows_count_chapter_2[0]

    def add_new_chapter(self, chapter, book_id):
        count = self.rows_count_chapter()
        if chapter == None or chapter.chapter_name == None or chapter.id == None or book_id == None:
            return None
        postgres_insert_query_new_chapter = "INSERT INTO projekt.chapter (id, chapter_name, edited_date) VALUES (%s, %s, now())"
        record_to_insert_new_chapter = (int(count) + 1, chapter.chapter_name)
        self.cursor.execute(postgres_insert_query_new_chapter, record_to_insert_new_chapter)
        self.cursor.execute("SELECT max(id) from projekt.book_chapter")
        book_chapters_id_count = self.cursor.fetchone()
        book_chaper_id=int(book_chapters_id_count[0])

        postgres_insert_query_new_chapter_in_book_chapter = "INSERT INTO projekt.book_chapter (id, book_id, edited_date, chapter_id) VALUES (%s, %s, now(), %s)"
        record_to_insert_new_chapter_in_book_chapter = (book_chaper_id + 1, int(book_id), int(count) + 1)
        self.cursor.execute(postgres_insert_query_new_chapter_in_book_chapter, record_to_insert_new_chapter_in_book_chapter)
        self.connection.commit()

    def chapter_delete(self, chapter_id):
        if chapter_id==None:
            return None
        postgres_delete_query = "DELETE FROM projekt.chapter WHERE id = %s ;" % chapter_id
        self.cursor.execute(postgres_delete_query)
        postgres_book_chapter_delete_query = ("DELETE from projekt.book_chapter where chapter_id=%d" % chapter_id)
        self.cursor.execute(postgres_book_chapter_delete_query)
        self.connection.commit()