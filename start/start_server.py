import sys

from DataBase.class_DB import DB
from CODE.class_server import Server
from CODE.class_message_search import TimeSetting

if __name__ == '__main__':
    db_conn = DB(test_option=True)
    time_set = TimeSetting(db_conn)
    # db_conn.create_tables()
    server = Server(db_conn, time_set)
    # day, time = Server(db_conn).alarm_time_data("9월 29일 9시")
    # print(day)
    # print(time)
    # Server(db_conn).alarm_test("qwer")
    server.start()
