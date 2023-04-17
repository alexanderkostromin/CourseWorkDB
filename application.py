class Application:
    """Базовый класс заявки"""

    def __init__(self, client_id, status_id, reply_type_id, urgency_id, service_id, application_data, date):
        self.client_id = client_id
        self.status_id = status_id
        self.reply_type_id = reply_type_id
        self.urgency_id = urgency_id
        self.service_id = service_id
        self.application_data = application_data
        self.date = date

