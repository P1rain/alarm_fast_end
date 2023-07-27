class Alarm:
    def __init__(self, alarm_id, user_id, alarm_time, alarm_date, alarm_day_of_the_week, alarm_song):
        self.alarm_id = alarm_id
        self.user_id = user_id
        self.alarm_time = alarm_time
        self.alarm_date = alarm_date
        self.alarm_day_of_the_week = alarm_day_of_the_week
        self.alarm_song = alarm_song

    def __str__(self):
        return f"{self.__repr__()}"

    def __repr__(self):
        return f"{self.__dict__}"

    def __eq__(self, other):
        if isinstance(other, Alarm) and \
                self.alarm_id == other.alarm_id and \
                self.user_id == other.user_id and \
                self.alarm_time == other.alarm_time and \
                self.alarm_date == other.alarm_date and \
                self.alarm_day_of_the_week == other.alarm_day_of_the_week and \
                self.alarm_song == other.alarm_song:
            return True
        return False
