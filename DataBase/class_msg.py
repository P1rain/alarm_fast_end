class Message:
    def __init__(self, user_id, user_nickname, send_msg, send_time):
        self.user_id = user_id
        self.user_nickname = user_nickname
        self.send_msg = send_msg
        self.send_time = send_time

    def __str__(self):
        return f"{self.__repr__()}"

    def __repr__(self):
        return f"{self.__dict__}"

    def __eq__(self, other):
        if isinstance(other, Message) and \
                self.user_id == other.user_id and \
                self.user_nickname == other.user_nickname and \
                self.send_msg == other.send_msg and \
                self.send_time == other.send_time:
            return True
        return False

    def __lt__(self, other):
        return self.user_nickname < other.user_nickname
