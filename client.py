class Client(object):
    """Базовый класс клиента"""

    def __init__(self, name, surname, email, phone, login, password):
        self.name = name
        self.surname = surname
        self.email = email
        self.phone = phone
        self.login = login
        self.password = password



