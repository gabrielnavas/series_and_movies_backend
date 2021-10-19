from datetime import datetime


class UserValidationModel:
    def __init__(self, first_name, last_name, email, password, password_confirmation):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.password_confirmation = password_confirmation


class UserModel:
    def __init__(self, id: int, first_name: str, last_name: str, email: str, password: str, created_at: datetime):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.created_at = created_at
