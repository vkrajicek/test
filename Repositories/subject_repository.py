from Classes.subject import Subject

class Subject_repository:
    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()

    def get_all(self):
        self.cursor.execute("SELECT * from projekt.subject ;")
        records_subject = self.cursor.fetchall()
        subject_list = []
        for subject in records_subject:
            new_subject = Subject()
            new_subject.id = subject[0]
            new_subject.chapter_name = subject[1]
            new_subject.edited_date = subject[3]
            subject_list.append(new_subject)
        return subject_list

    def get_one_by_id(self, id):
        self.cursor.execute("SELECT * from projekt.subject where id=%d ;" % id)
        records_subject = self.cursor.fetchone()
        now_subject = Subject()
        now_subject.id = records_subject[0]
        now_subject.chapter_name = records_subject[1]
        now_subject.edited_date = records_subject[3]
        return now_subject

    def rows_count_subject(self):
        self.cursor.execute("SELECT count(*) from projekt.subject ;")
        rows_count_subject_1 = self.cursor.fetchall()
        rows_count_subject_2 = rows_count_subject_1[0]
        return rows_count_subject_2

    def add_new_subject(self, subject, user_id, attendance_actual, grade):
        count = self.rows_count_subject()
        postgres_insert_query_new_subject = "INSERT INTO projekt.subject (id, subject, teacher, method_of_course_completion, edited_date) VALUES (%d, %s, %s, %s, now())"
        record_to_insert_new_subject = (count[0] + 1, subject.subject, subject.teacher, subject.method_of_course_completion)
        self.cursor.execute(postgres_insert_query_new_subject, record_to_insert_new_subject)
        self.connection.commit()
        self.cursor.execute("SELECT count(*) from projekt.user_subject")
        user_subject_id_count = self.cursor.fetchone()
        postgres_insert_query_new_subject_in_user_subject = "INSERT INTO projekt.user_subject (id, user_id, subject_id, attendance_actual, grade, edited_date) VALUES (%d, %d, %d, %d, %d, now())"
        record_to_insert_new_subject_in_user_subject = (user_subject_id_count,user_id, count[0] + 1, attendance_actual, grade )
        self.cursor.execute(postgres_insert_query_new_subject_in_user_subject, record_to_insert_new_subject_in_user_subject)
        self.connection.commit()

    def subject_delete(self, subject_id):
        postgres_subject_delete_query = "DELETE FROM projekt.subject WHERE subject = %s ;" % subject_id
        self.cursor.execute(postgres_subject_delete_query)
        postgres_user_subject_delete_query = ("DELETE from projekt.user_subject where subject_id=%d" % subject_id)
        self.cursor.execute(postgres_user_subject_delete_query)
        self.connection.commit()