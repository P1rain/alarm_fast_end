import sys

from DataBase.class_DB import DB
from CODE.class_server import Server

if __name__ == '__main__':
    db_conn = DB(test_option=True)
    # db_conn.create_tables()
    server = Server(db_conn)
    # day, time = Server(db_conn).alarm_time_data("9월 29일 9시")
    # print(day)
    # print(time)
    server.start()
