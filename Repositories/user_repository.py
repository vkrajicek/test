from Classes.user import User


class User_repository:
    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()

    # get all users from user table
    def get_all(self):
        self.cursor.execute("SELECT * from projekt.user ;")
        records_user = self.cursor.fetchall()
        if records_user == None:
            return None
        user_list = []
        for user in records_user:
            new_user = User()
            new_user.id = user[0]
            new_user.name = user[1]
            new_user.surename = user[2]
            new_user.login = user[3]
            new_user.password = user[4]
            new_user.lastlogin = user[5]
            new_user.lastlogintime = user[6]
            user_list.append(new_user)
        return user_list

    # ged one user from user table according to id
    def get_one_by_id(self, id):
        if id == None or id < 0:
            return None
        self.cursor.execute("SELECT * from projekt.user where id=%d ;" % id)
        records_user = self.cursor.fetchone()
        if records_user == None:
            return None
        new_user = User()
        new_user.id = records_user[0]
        new_user.name = records_user[1]
        new_user.surename = records_user[2]
        new_user.login = records_user[3]
        new_user.password = records_user[4]
        new_user.lastlogin = records_user[5]
        new_user.lastlogintime = records_user[6]
        return new_user

    # update one user in user table
    def update(self, user):
        if user.id == None or user == None or user.name == None or user.surename == None or user.login == None or user.password == None:
            return None
        user_update_query = "UPDATE projekt.user set name=%s, surename=%s, login =%s, password=%s where id=%s ;"
        parameters = (user.name, user.surename, user.login, user.password, int(user.id))
        self.cursor.execute(user_update_query, parameters)

    # selected user according to login and password
    def user_select(self, login_result, pass_result):
        if login_result == None or pass_result == None:
            return None
        user_select_query = "SELECT * from projekt.user where login=%s and password=%s"
        parameters = (str(login_result), str(pass_result))
        self.cursor.execute(user_select_query, parameters)
        selected_user = self.cursor.fetchone()
        if selected_user != None:
            new_user = User()
            new_user.id = selected_user[0]
            new_user.name = selected_user[1]
            new_user.surename = selected_user[2]
            new_user.login = selected_user[3]
            new_user.password = selected_user[4]
            new_user.lastlogin = selected_user[5]
            new_user.lastlogintime = selected_user[6]
            return new_user
        else:
            return None

    # add new user into user table
    def add_new_user(self, user):
        if user.id == None or user == None or user.name == None or user.surename == None or user.login == None or user.password == None:
            return None
        new_user_add_query = " INSERT INTO projekt.user (id, name, surename, login, password) VALUES (%s,%s,%s,%s,%s)"
        record_to_add = (int(user.id), user.name, user.surename, user.login, user.password)
        self.cursor.execute(new_user_add_query, record_to_add)
        self.connection.commit()

    # delete one user from user, user_subject and subject tables
    def user_delete(self, user_id):
        if user_id == None:
            return None
        user_delete_query = "DELETE FROM projekt.user WHERE id = %s ;" % user_id
        self.cursor.execute(user_delete_query)
        self.cursor.execute("SELECT subject_id from projekt.user_subject where user_id=%d ;" % user_id)
        subject_id = self.cursor.fetchall()
        if subject_id == []:
            return None
        subject_ids_list = []
        for i in subject_id:
            subject_ids_list.append(i[0])
        subject_delete_query = "DELETE FROM projekt.subject WHERE id = %s ;" % subject_ids_list[0]
        self.cursor.execute(subject_delete_query)
        user_subject_delete_query = ("DELETE from projekt.user_subject where user_id=%d" % user_id)
        self.cursor.execute(user_subject_delete_query)
        self.connection.commit()
