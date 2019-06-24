import unittest
import psycopg2

from Classes.user import User
from Repositories.user_repository import User_repository


class User_repository_test(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.connection=psycopg2.connect(user="postgres",
                                    password="Aquapark4",
                                    host="localhost",
                                    port="5432",
                                    database="test")
        self.user_repository=User_repository(self.connection)
        self.user = self.connection.cursor()
        self.user.execute("insert into projekt.user values (1,'Vit', 'Krajicek', 'Vito', 123, now(), now()) ;")

    def test_get_all_valid(self):
        result=self.user_repository.get_all()
        self.assertGreater(len(result), 0)

    # def test_get_all_not_valid(self):
    #     result=self.user_repository.get_all()
    #     self.assertEqual(len(result), 0)

    def test_get_one_by_id_valid(self):
        user=self.user_repository.get_one_by_id(1)
        self.assertEqual(user.id, 1)
        self.assertEqual(user.name, 'Vit')
        self.assertEqual(user.surename, 'Krajicek')
        self.assertEqual(user.login, 'Vito')
        self.assertEqual(user.password, '123')

    def test_get_one_by_id_id_none(self):
        result=self.user_repository.get_one_by_id(None)
        self.assertEqual(result, None)

    def test_get_one_by_id_id_negative(self):
        result=self.user_repository.get_one_by_id(-1)
        self.assertEqual(result, None)

    def test_get_one_by_id_id_not_valid(self):
        result=self.user_repository.get_one_by_id(50)
        self.assertEqual(result, None)

    def test_update_valid(self):
        user=User()
        user.id = 1
        user.name = 'Tomas'
        user.surename = 'Krystof'
        user.login = 'Toso'
        user.password = 1234
        self.user_repository.update(user)
        self.assertEqual(user.id, 1)
        self.assertEqual(user.name, 'Tomas')
        self.assertEqual(user.surename, 'Krystof')
        self.assertEqual(user.login, 'Toso')
        self.assertEqual(user.password, 1234)

    def test_update_parameter_none(self):
        user=User()
        user.id = 1
        user.name = 'Tomas'
        user.surename = 'Krystof'
        user.login = 'Toso'
        user.password = None
        result=self.user_repository.update(user)
        self.assertEqual(result, None)

    def test_user_select_valid(self):
        login_result = 'Toso'
        pass_result = 1234
        user=self.user_repository.user_select(login_result, pass_result)
        self.assertEqual(user.name, 'Tomas')

    def test_user_select_parameter_none(self):
        login_result = None
        pass_result = 123
        result=self.user_repository.user_select(login_result, pass_result)
        self.assertEqual(result, None)

    def test_add_new_user_valid(self):
        user=User()
        user.id = 2
        user.name = 'Jaroslav'
        user.surename = 'Sochan'
        user.login = 'Jaro'
        user.password = 12345
        self.user_repository.add_new_user(user)
        self.assertEqual(user.id, 2)
        self.assertEqual(user.name, 'Jaroslav')
        self.assertEqual(user.surename, 'Sochan')
        self.assertEqual(user.login, 'Jaro')
        self.assertEqual(user.password, 12345)

    def test_add_new_user_parameter_none(self):
        user=User()
        user.id = 2
        user.name = None
        user.surename = 'Sochan'
        user.login = 'Jaro'
        user.password = 12345
        result=self.user_repository.add_new_user(user)
        self.assertEqual(result, None)

    def test_user_delete_valid(self):
        user=User()
        user.id = 3
        user.name = 'Johny'
        user.surename = 'Knoxville'
        user.login = 'John'
        user.password = 12345
        self.user_repository.add_new_user(user)
        self.user_repository.user_delete(3)

    def test_subject_delete_none_parameter(self):
        result=self.user_repository.user_delete(None)
        self.assertEqual(result, None)

