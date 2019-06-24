class User:
    def __init__(self):
        self.login = ''
        self.id = 0
        self.name = ''
        self.surename = ''
        self.password = ''
        self.lastlogin = ''
        self.lastlogintime = ''

    def __str__(self):
        return self.login + ' ' + str(
            self.id) + ' ' + self.name + ' ' + self.surename + ' ' + self.password + ' ' + self.lastlogin.__str__() + ' ' + self.lastlogintime.__str__()

# ss
