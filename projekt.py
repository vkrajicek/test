import psycopg2

from Classes.book import Book
from Classes.chapter import Chapter
from Classes.subject import Subject
from Classes.user import User
from Repositories.book_repository import Book_repository
from Repositories.chapter_repository import Chapter_repository
from Repositories.subject_repository import Subject_repository
from Repositories.user_repository import User_repository

connection = psycopg2.connect(user="postgres",
                              password="Aquapark4",
                              host="localhost",
                              port="5432",
                              database="postgres")
cursor = connection.cursor()

user_repository = User_repository(connection)
book_repository = Book_repository(connection)
chapter_repository = Chapter_repository(connection)
subject_repository = Subject_repository(connection)

user_list = user_repository.get_all()

print('Welcome to the database')

print('Please, write your login and then password')

loged_user = None
for i in range(3):
    login_result = input('Login: ')
    pass_result = input('Password: ')

    selected_user = user_repository.user_select(login_result, pass_result)
    if selected_user == None:
        print('You press wrong command and you have only ' + ' ' + str(int(2 - i)) + ' ' + ' attempts')
        continue

    print('Welcome ' + selected_user.name)
    loged_user = selected_user
    break

if loged_user == None:
    exit(0)

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
                result = user_repository.user_delete(result_user_delete)

            result_user_in = input('Do you want to add an user? type yes or no: ')
            if result_user_in == 'no':
                break
            if result_user_in == 'yes':
                user = User()
                book = Book()
                user.id = input('Type id of the user you want to add: ')
                user.name = input('Type name of the user you want to add: ')
                user.surename = input('Type surename of the user you want to add: ')
                user.login = input('Type login of the user you want to add: ')
                user.password = input('Type password of the user you want to add: ')
                user_repository.add_new_user(user)

                book.name_of_the_book = input('Type new book for the new user here: ')
                book.author = input('Type author for the book: ')

                book_repository.add_new_book(book)

                break

for i in range(4):
    if selected_user.login == 'Vito':
        print('Do you want to delete one of the subjects? ')
        press = input('Please type yes or no: ')
        if press == 'yes':
            subject_id = input('Type here the id of the subject: ')
            subject_repository.subject_delete(subject_id)
            break
        if press == 'no':
            break
    else:
        break

books = book_repository.get_all_by_user_id(loged_user.id)
if len(books) < 2:
    print('Here is your book: ')
else:
    print('Here are your books')
for i in books:
    print(i.name_of_the_book + ' by author: ' + i.author + ' at a position: ' + str(i.id))

for i in range(4):
    print('Do you want to add another book to you? ')
    press = input('Please type yes or no: ')
    if press == 'yes':
        book = Book()
        book.name_of_the_book = input('Type name your new book here: ')
        book.author = input('Type the author here: ')
        chapter_count = input('Type number of chapters of this book: ')
        for i in range(1, int(chapter_count) + 1):
            chapter = Chapter()
            chapter.chapter_name = input('Type chapter number' + str(i) + ' here:')
            book.chapters.append(chapter)
        book.user_id = loged_user.id
        book_repository.add_new_book(book)
        break
    if press == 'no':
        break
    else:
        print('You press wrong command and you have only ' + ' ' + str(int(3 - i)) + ' ' + ' attempts')

for i in range(1, 4):
    print('Do you want to delete some of your books?')
    press = input('Please type yes or no: ')

    if press == 'yes':
        if len(books) < 2:
            print('Here is again your book: ')
        else:
            print('Here are again your books')
        for i in books:
            print(i.name_of_the_book + ' by author: ' + i.author + ' at a position: ' + str(i.id))
        result_position = input(' Press the number of position of the book you want to delete: ')
        book_repository.book_delete(int(result_position))
        break
    if press == 'no':
        break
    else:
        print('You press wrong command and you have only ' + ' ' + str(int(3 - i)) + ' ' + ' attempts')

cursor.execute("SELECT * from projekt.user_subject where user_id=%d;" % loged_user.id)
records_subject = cursor.fetchall()
user_id_in_user_subjects = []
subject_id_in_user_subject = []
for i in records_subject:
    user_id_in_user_subjects.append(i[loged_user.id])
    subject_id_in_user_subject.append((i[2]))

print('Here are yours subjects and teachers')
for i in subject_id_in_user_subject:
    subjects = subject_repository.get_one_by_id(i)
    print(subjects.subject + ' : ' + subjects.teacher)

for i in range(4):
    print('Do you want to add another subject to you? ')
    press = input('Please type yes or no: ')
    if press == 'yes':
        subject = Subject()
        subject.subject = input('Type here name of the subject: ')
        subject.teacher = input('Type here teacher of the subject: ')
        subject.method_of_course_completion = input(
            ' Type here if you can complete it by Final exam or Annual results: ')
        attendance_actual = input('Type here your attendace from 1 to 15: ')
        grade = input(' Type here your grade from 1 to 5: ')
        subject_repository.add_new_subject(subject, loged_user.id, attendance_actual, grade)
        break
    if press == 'no':
        break
    else:
        print('You press wrong command and you have only ' + ' ' + str(int(3 - i)) + ' ' + ' attempts')

print('Thank you ' + selected_user.name + ' ' + 'for using something_maker 9000')
print('Have a nice day')

cursor.close()
connection.close()
