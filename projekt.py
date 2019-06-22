import psycopg2


from Repositories.text_repository import Text_repository
from Repositories.user_repository import User_repository

connection = psycopg2.connect(user="postgres",
                              password="Aquapark4",
                              host="localhost",
                              port="5432",
                              database="postgres")
cursor = connection.cursor()

user_repository = User_repository(connection)
user_list = user_repository.get_all()

text_repository = Text_repository(connection)
rows_count_2 = text_repository.rows_count()

print('Welcome to the text database')

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

selected_texts = text_repository.id_veta_selected(selected_user.id)

selected_texts_dictionary = {}
for vet in selected_texts:
    selected_texts_dictionary.update({vet[0]: vet[1]})

for i in range(4):
    if selected_user.login == 'Vito':
        result_user_change = input(
            ' Hi Vito, you are admin so you can add or delete users, do you want it? type yes or no: ')
        if result_user_change == 'no':
            break
        if result_user_change == 'yes':
            result_user_del = input('Do you want to delete an user? type yes or no: ')

            if result_user_del == 'yes':
                result_user_delete = input('Type login of the user you want to delete: ')
                user_repository.user_delete(result_user_delete)

            result_user_in = input('Do you want to add an user? type yes or no: ')
            if result_user_in == 'no':
                break
            if result_user_in == 'yes':
                result_user_add_id = input('Type id of the user you want to add: ')
                result_user_add_name = input('Type name of the user you want to add: ')
                result_user_add_surename = input('Type surename of the user you want to add: ')
                result_user_add_login = input('Type login of the user you want to add: ')
                result_user_add_password = input('Type password of the user you want to add: ')

                user_repository.add_new_user(result_user_add_id, result_user_add_name, result_user_add_surename, result_user_add_login, result_user_add_password)

                result_new_text_for_new_user = input('Type new text for the new user here: ')

                text_repository.add_new_text(rows_count_2, result_user_add_id, result_new_text_for_new_user)

                break

print('Here are your texts: ')
for key, value in selected_texts_dictionary.items():
    print(value + ' on position ' + str(key))

for i in range(1, 4):
    print('If you want to change your texts press 1')
    print('if you want to continue, press 2')
    press = input('Please type a number: ')

    if press == '1':
        result_position = input(' Press the number of position of the text you want to change: ')
        dict_value = ''
        dict_key = 0
        for key, value in selected_texts_dictionary.items():
            if key == int(result_position):
                dict_value += value
                dict_key += key
        result_change_text = input('Change your text from -' + ' ' + str(dict_value) + ' ' + '-to: ')

        text_repository.update(result_change_text, dict_key)
        break

    if press == '2':
        break
    else:
        print('You press wrong command and you have only ' + ' ' + str(int(3 - i)) + ' ' + ' attempts')

for i in range(4):
    print('Do you want to add another text to you? ')
    press = input('Please type yes or no: ')
    if press == 'yes':
        result_new_text = input('Type your new text here: ')
        text_repository.add_new_text(rows_count_2, selected_user.id, result_new_text)
        break
    if press == 'no':
        break
    else:
        print('You press wrong command and you have only ' + ' ' + str(int(3 - i)) + ' ' + ' attempts')

print('Thank you ' + selected_user.name + ' ' + 'for using text_maker 9000')
print('Have a nice day')

cursor.close()
connection.close()
