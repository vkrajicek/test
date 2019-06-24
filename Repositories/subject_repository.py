from Classes.subject import Subject

class Subject_repository:
    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()
    # selected all data from subject table
    def get_all(self):
        self.cursor.execute("SELECT * from projekt.subject ;")
        records_subject = self.cursor.fetchall()
        if records_subject == None:
            return None
        subject_list = []
        for subject in records_subject:
            new_subject = Subject()
            new_subject.id = subject[0]
            new_subject.subject = subject[1]
            new_subject.teacher = subject[2]
            new_subject.method_of_course_completion = subject[3]
            new_subject.edited_date = subject[4]
            subject_list.append(new_subject)
        return subject_list
    # selected one row of data from subject table according to id
    def get_one_by_id(self, id):
        if id == None or id < 0:
            return None
        self.cursor.execute("SELECT * from projekt.subject where id=%d ;" % id)
        records_subject = self.cursor.fetchone()
        if records_subject == None:
            return None
        new_subject = Subject()
        new_subject.id = records_subject[0]
        new_subject.subject = records_subject[1]
        new_subject.teacher = records_subject[2]
        new_subject.method_of_course_completion = records_subject[3]
        new_subject.edited_date = records_subject[4]
        return new_subject
  # find the biggest id from subject table for latter use
    def rows_count_subject(self):
        self.cursor.execute("SELECT max(id) from projekt.subject ;")
        rows_count_subject_1 = self.cursor.fetchall()
        rows_count_subject_2 = rows_count_subject_1[0]
        if rows_count_subject_2[0]==None:
            return 0
        return rows_count_subject_2[0]
    # added new subject into subject and user_subject tables
    def add_new_subject(self, subject, user_id, attendance_actual, grade):
        if subject == None or subject.subject == None or subject.teacher == None or subject.method_of_course_completion == None or user_id == None or attendance_actual == None or grade == None:
            return None
        count = self.rows_count_subject()
        postgres_insert_query_new_subject = "INSERT INTO projekt.subject (id, subject, teacher, method_of_course_completion, edited_date) VALUES (%s, %s, %s, %s, now())"
        record_to_insert_new_subject = (int(count) + 1, subject.subject, subject.teacher, subject.method_of_course_completion)
        subject.id=int(count) + 1
        self.cursor.execute(postgres_insert_query_new_subject, record_to_insert_new_subject)
        self.connection.commit()
        self.cursor.execute("SELECT max(id) from projekt.user_subject")
        user_subject_id_count = self.cursor.fetchone()
        if user_subject_id_count[0]== None:
            user_subject_id_count=0
        else:
            user_subject_id_count=user_subject_id_count[0]
        postgres_insert_query_new_subject_in_user_subject = "INSERT INTO projekt.user_subject (id, user_id, subject_id, attendance_actual, grade, edited_date) VALUES (%s, %s, %s, %s, %s, now())"
        record_to_insert_new_subject_in_user_subject = (user_subject_id_count+1, int(user_id), subject.id, int(attendance_actual), int(grade))
        self.cursor.execute(postgres_insert_query_new_subject_in_user_subject, record_to_insert_new_subject_in_user_subject)
        self.connection.commit()
    # deleted one subject from subject and user_subject tables
    def subject_delete(self, subject_id):
        if subject_id==None:
            return None
        postgres_subject_delete_query = "DELETE FROM projekt.subject WHERE id = %s ;" % subject_id
        self.cursor.execute(postgres_subject_delete_query)
        postgres_user_subject_delete_query = ("DELETE from projekt.user_subject where subject_id=%d" % subject_id)
        self.cursor.execute(postgres_user_subject_delete_query)
        self.connection.commit()