from Classes.chapter import Chapter


class Chapter_repository:
    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()

    def get_all(self):
        self.cursor.execute("SELECT * from projekt.chapter ;")
        records_chapter = self.cursor.fetchall()
        chapter_list = []
        for chapter in records_chapter:
            now_chapter = Chapter()
            now_chapter.id = chapter[0]
            now_chapter.chapter_name = chapter[1]
            now_chapter.edited_date = chapter[3]
            chapter_list.append(now_chapter)
        return chapter_list

    def get_one_by_id(self, id):
        self.cursor.execute("SELECT * from projekt.chapter where id=%d ;" % id)
        records_chapter = self.cursor.fetchone()
        now_chapter = Chapter()
        now_chapter.id = records_chapter[0]
        now_chapter.chapter_name = records_chapter[1]
        now_chapter.edited_date = records_chapter[3]
        return now_chapter

    def rows_count_chapter(self):
        self.cursor.execute("SELECT count(*) from projekt.chapter ;")
        rows_count_chapter_1 = self.cursor.fetchall()
        rows_count_chapter_2 = rows_count_chapter_1[0]
        return int(rows_count_chapter_2)

    def chapter_delete(self, chapter_id):
        postgres_delete_query = "DELETE FROM projekt.chapter WHERE id = %s ;" % chapter_id
        self.cursor.execute(postgres_delete_query)
        postgres_book_chapter_delete_query = ("DELETE from projekt.book_chapter where chapter_id=%d" % chapter_id)
        self.cursor.execute(postgres_book_chapter_delete_query)
        self.connection.commit()

    # def add_new_chapter(self, rows_count_chapter_2, result_new_chapter):
    #     postgres_insert_query_new_chapter = "INSERT INTO projekt.chapter (id, chapter_name) VALUES (%s, %s)"
    #     record_to_insert_new_chapter = (int(rows_count_chapter_2[0]) + 1, result_new_chapter)
    #     self.cursor.execute(postgres_insert_query_new_chapter, record_to_insert_new_chapter)
    #     self.connection.commit()