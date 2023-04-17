class Worker:
    """Базовый класс работника"""

    def __init__(self, role_id, name, surname, email, phone, login, password, experience):
        self.role_id = role_id
        self.name = name
        self.surname = surname
        self.email = email
        self.phone = phone
        self.login = login
        self.password = password
        self.experience = experience

