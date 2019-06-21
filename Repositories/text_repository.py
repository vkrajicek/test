from Classes.text import Text


class Text_repository:
    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()

    def get_all(self):
        self.cursor.execute("SELECT * from projekt.projekt_text ;")
        records_text = self.cursor.fetchall()
        text_list = []
        for tekst in records_text:
            now_text = Text()
            now_text.id = tekst[0]
            now_text.user_id = tekst[1]
            now_text.veta = tekst[2]
            now_text.edited_date = tekst[3]
            text_list.append(now_text)
        return text_list

    def get_all_by_user_id(self,user_id):
        self.cursor.execute("SELECT * from projekt.projekt_text  where user_id=%d;" % user_id)
        records_text = self.cursor.fetchall()
        text_list = []
        for tekst in records_text:
            now_text = Text()
            now_text.id = tekst[0]
            now_text.user_id = tekst[1]
            now_text.veta = tekst[2]
            now_text.edited_date = tekst[3]
            text_list.append(now_text)
        return text_list

    def rows_count(self):
        self.cursor.execute("SELECT count(*) from projekt.projekt_text ;")
        rows_count_1 = self.cursor.fetchall()
        rows_count_2 = rows_count_1[0]
        return rows_count_2

    def id_veta_selected(self, user_id):
        postgres_select_query = "SELECT id, veta from projekt.projekt_text where user_id = %s "
        record_to_select = (str(user_id))
        self.cursor.execute(postgres_select_query, record_to_select)
        selected_texts = self.cursor.fetchall()
        return selected_texts

    def add_new_text(self, rows_count_2, result_user_add_id, result_new_text_for_new_user):
        postgres_insert_query_new_user = "INSERT INTO projekt.projekt_text (id,user_id, veta) VALUES (%s, %s, %s)"
        record_to_insert_new_user = (int(rows_count_2[0]) + 1, int(result_user_add_id), result_new_text_for_new_user)
        self.cursor.execute(postgres_insert_query_new_user, record_to_insert_new_user)
        self.connection.commit()

    def update(self, result_change_text, dict_key):
        postgres_insert_query = "UPDATE projekt.projekt_text set veta =%s where id= %s "
        record_to_insert = (result_change_text, str(dict_key))
        self.cursor.execute(postgres_insert_query, record_to_insert)
        self.connection.commit()
    #
    # def add_new_text_for_you(self, rows_count_2, user_id, result_new_text):
    #     postgres_insert_query = "INSERT INTO projekt.projekt_text (id,user_id, veta) VALUES (%s, %s, %s)"
    #     record_to_insert = (int(rows_count_2[0]) + 1, str(user_id), result_new_text)
    #     self.cursor.execute(postgres_insert_query, record_to_insert)
    #     self.connection.commit()


# ss