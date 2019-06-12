class Text:
    def __init__(self):
        self.id=0
        self.user_id=0
        self.veta=''
        self.edited_date=''

    def __str__(self):
        return str(self.id) + ' ' + str(self.user_id) + ' ' + self.veta + ' ' + self.edited_date.__str__()
