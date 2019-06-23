import psycopg2

from Classes.subject import Subject
from Classes.user import User

from Repositories.book_repository import Book_repository
from Repositories.subject_repository import Subject_repository
from Repositories.user_repository import User_repository
from Repositories.chapter_repository import Chapter_repository

connection = psycopg2.connect(user="postgres",
                              password="Aquapark4",
                              host="localhost",
                              port="5432",
                              database="postgres")
cursor = connection.cursor()

user_repository = User_repository(connection)
user_list = user_repository.get_all()

book_repository = Book_repository(connection)
chapter_repository = Chapter_repository(connection)
subject_repository = Subject_repository(connection)


print('Welcome to the database')

print('Please, write your login and then password')

log_user = None
for i in range(3):
    login_result = input('Login: ')
    pass_result = input('Password: ')

    selected_user = user_repository.user_select(login_result, pass_result)
    if selected_user==None:
        print('You press wrong command and you have only ' + ' ' + str(int(2 - i)) + ' ' + ' attempts')
        continue

    print('Welcome ' + selected_user.name)
    log_user = selected_user
    user = selected_user
    break

if log_user==None:
    exit(0)


# selected_texts = book_repository.id_book_selected(selected_user.id)

# selected_texts_dictionary = {}
# for vet in selected_texts:
#     selected_texts_dictionary.update({vet[0]: vet[1]})

for i in range(4):
    if selected_user.login == 'Vito':
        result_user_change = input(
            ' Hi Vito, you are admin so you can add or delete users, do you want it? type yes or no: ')
        if result_user_change == 'no':
            break
        if result_user_change == 'yes':
            result_user_del = input('Do you want to delete an user? type yes or no: ')

            if result_user_del == 'yes':
                result_user_delete = input('Type id of the user you want to delete: ')
                user_repository.user_delete(result_user_delete)

            result_user_in = input('Do you want to add an user? type yes or no: ')
            if result_user_in == 'no':
                break
            if result_user_in == 'yes':
                user = User()
                user.id = input('Type id of the user you want to add: ')
                user.name =input('Type name of the user you want to add: ')
                user.surename =input('Type surename of the user you want to add: ')
                user.login =input('Type login of the user you want to add: ')
                user.password =input('Type password of the user you want to add: ')
                user_repository.add_new_user(user)

                result_new_book_for_new_user = input('Type new book for the new user here: ')
                result_new_author_for_new_book = input('Type author for the book: ')

                book_repository.add_new_book(user.id, result_new_book_for_new_user, result_new_author_for_new_book)

                break

books=book_repository.get_all_by_user_id(log_user.id)
print('Here is your book: ')
print(books[0].name_of_the_book)

# subject=Subject()
# subject.id=5
# subject.subject='Matika'
# subject.teacher='pancelka'
# subject.method_of_course_completion='Final exam'
# subject_repository.add_new_subject(subject, selected_user.id)




#
# for i in range(1, 4):
#     print('If you want to change your texts press 1')
#     print('if you want to continue, press 2')
#     press = input('Please type a number: ')
#
#     if press == '1':
#         result_position = input(' Press the number of position of the text you want to change: ')
#         dict_value = ''
#         dict_key = 0
#         for key, value in selected_texts_dictionary.items():
#             if key == int(result_position):
#                 dict_value += value
#                 dict_key += key
#         result_change_text = input('Change your text from -' + ' ' + str(dict_value) + ' ' + '-to: ')
#
#         book_repository.update(result_change_text, dict_key)
#         break
#
#     if press == '2':
#         break
#     else:
#         print('You press wrong command and you have only ' + ' ' + str(int(3 - i)) + ' ' + ' attempts')
#
# for i in range(4):
#     print('Do you want to add another text to you? ')
#     press = input('Please type yes or no: ')
#     if press == 'yes':
#         result_new_text = input('Type your new text here: ')
#         book_repository.add_new_book(rows_count_book, selected_user.id, result_new_text)
#         break
#     if press == 'no':
#         break
#     else:
#         print('You press wrong command and you have only ' + ' ' + str(int(3 - i)) + ' ' + ' attempts')

print('Thank you ' + selected_user.name + ' ' + 'for using text_maker 9000')
print('Have a nice day')

cursor.close()
connection.close()
