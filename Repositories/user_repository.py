from Classes.user import User


class User_repository:
    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()

    def get_all(self):
        self.cursor.execute("SELECT * from projekt.user ;")
        records_user = self.cursor.fetchall()
        user_list = []
        for user in records_user:
            now_user = User()
            now_user.id = user[0]
            now_user.name = user[1]
            now_user.surename = user[2]
            now_user.login = user[3]
            now_user.password = user[4]
            now_user.lastlogin = user[5]
            now_user.lastlogintime = user[6]
            user_list.append(now_user)
        return user_list

    def get_one_by_id(self, id):
        self.cursor.execute("SELECT * from projekt.user where id=%d ;" % id)
        records_user = self.cursor.fetchone()
        now_user = User()
        now_user.id = records_user[0]
        now_user.name = records_user[1]
        now_user.surename = records_user[2]
        now_user.login = records_user[3]
        now_user.password = records_user[4]
        now_user.lastlogin = records_user[5]
        now_user.lastlogintime = records_user[6]
        return now_user

    def update(self, user):
        if user.id != None:
            self.cursor.execute(
                "UPDATE projekt.user set name=%s, surename=%s, login =%s, password=%s, where id=%d ;" % user.name,
                user.surename, user.login, user.password)
            self.connection.commit()

    def user_select(self, login_result, pass_result):
        user_select_query= "SELECT * from projekt.user where login=%s and password=%s"
        parameters=(str(login_result), str(pass_result))
        self.cursor.execute(user_select_query,parameters )
        selected_user = self.cursor.fetchone()
        if selected_user != None:
            now_user = User()
            now_user.id = selected_user[0]
            now_user.name = selected_user[1]
            now_user.surename = selected_user[2]
            now_user.login = selected_user[3]
            now_user.password = selected_user[4]
            now_user.lastlogin = selected_user[5]
            now_user.lastlogintime = selected_user[6]
            return now_user
        else:
            return None

    def user_delete(self, user_id):
        postgres_delete_query = "DELETE FROM projekt.user WHERE id = %s ;" % user_id
        self.cursor.execute(postgres_delete_query)
        self.connection.commit()

    def add_new_user(self, user):
        postgres_add_query = " INSERT INTO projekt.user (id, name, surename, login, password) VALUES (%d,%s,%s,%s,%s)"
        record_to_add = (user.id, user.name, user.surename, user.login, user.password)
        self.cursor.execute(postgres_add_query, record_to_add)
        self.connection.commit()




# ss

