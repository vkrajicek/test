class Subject:
    def __init__(self):
        self.id = 0
        self.subject = ''
        self.teacher = ''
        self.method_of_course_completion = ''
        self.edited_date = ''

    def __str__(self):
        return str(
            self.id) + ' ' + self.subject + ' ' + self.teacher + ' ' + self.method_of_course_completion + ' ' + self.edited_date.__str__()
