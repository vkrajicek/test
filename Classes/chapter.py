class Chapter:
    def __init__(self):
        self.id = 0
        self.chaper_name = ''
        self.edited_date = ''

    def __str__(self):
        return str(self.id) + ' ' + self.chaper_name + ' ' + self.edited_date.__str__()