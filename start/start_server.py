import sys

from DataBase.class_DB import DB
# from CODE.class_server import Server

if __name__ == '__main__':
    db_conn = DB(test_option=True)
    # db_conn.create_tables()
    # server = Server(db_conn)
    # server.start()
    db_conn.user_log_in('qwer', 'qwer')
