class User:
    def __init__(self, user_number, user_id, user_pw, user_nickname):
        self.user_number = user_number
        self.user_id = user_id
        self.user_pw = user_pw
        self.user_nickname = user_nickname

    def __str__(self):
        return f"{self.__repr__()}"

    def __repr__(self):
        return f"{self.__dict__}"

    def __eq__(self, other):
        if isinstance(other, User) and \
                self.user_number == other.user_number and \
                self.user_id == other.user_id and \
                self.user_pw == other.user_pw and \
                self.user_nickname == other.user_nickname:
            return True
        return False

    def __lt__(self, other):
        return self.user_nickname < other.user_nickname
