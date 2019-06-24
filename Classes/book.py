class Book:
    def __init__(self):
        self.id = 0
        self.user_id = 0
        self.name_of_the_book = ''
        self.author = ''
        self.edited_date = ''
        self.chapters = []

    def __str__(self):
        return str(self.id) + ' ' + str(
            self.user_id) + ' ' + self.name_of_the_book + ' ' + self.author + ' ' + self.edited_date.__str__()
