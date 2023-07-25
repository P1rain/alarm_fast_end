import psycopg2 as pg

from DataBase.class_user import User
# from DataBase.class_alarm import Alarm


class DB:
    _instance = None

    def __new__(cls, test_option=None):
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self, test_option=None):
        self.conn = None
        self.test_option = test_option

    def start_conn(self):
        if self.test_option is True:
            self.conn = pg.connect(host="10.10.20.115", dbname="db_alarm", user="kdt115", password="1234", port="5432")
        # else:
        #     self.conn = pg.connect("main_db.db")
        return self.conn.cursor()

    def end_conn(self):
        if self.conn is not None:
            self.conn.close()
            self.conn = None

    def commit_db(self):
        if self.conn is not None:
            self.conn.commit()
        else:
            raise f'connot commit datatbase! {self.__name__}'

    def create_tables(self):
        c = self.start_conn()
        # 대충 테이블 만드는 내용
        c.execute("""
        DROP TABLE IF EXISTS alarm_data;
        CREATE TABLE alarm_data (
            "alarm_id"	INTEGER,
            "user_number"	INTEGER,
            "alarm_name"	TEXT,
            "alarm_time"	TEXT,
            "alarm_date"	TEXT,
            "alarm_day_of_the_weak"	TEXT,
            "alarm_song"	TEXT,
            PRIMARY KEY("alarm_id")
        );
        DROP TABLE IF EXISTS user_list;
        CREATE TABLE user_list(
            "user_number"	INTEGER,
            "user_id"	varchar(12),
            "user_pw"	varchar(15),
            "user_nickname"	varchar(15),
            PRIMARY KEY("user_number")
        );
        """)
        self.commit_db()
        self.end_conn()

    # 회원가입 정보 tb에 집넣기
    def insert_user(self, user_object: User):
        c = self.start_conn()
        user_number = user_object.user_number
        user_id = user_object.user_id
        user_pw = user_object.user_pw
        user_nickname = user_object.user_nickname
        c.execute(f"select * from user_list where user_number = '{user_number}'")
        users_id = c.fetchone()
        if users_id is None:
            c.execute(
                f"insert into user_list values ('{user_number}', '{user_id}', '{user_pw}', '{user_nickname}')")
            self.commit_db()
            # 정렬 안함
            c.execute("select * from user")
            inserted_user = c.fetchone()
            inserted_user_obj = User(*inserted_user)
            self.end_conn()
            return inserted_user_obj
        else:
            updated_user_obj = self.update_user(user_object)
            return updated_user_obj

    # user테이블 업데이트
    def update_user(self, user_object: User):
        c = self.start_conn()
        user_id = user_object.user_id
        user_pw = user_object.user_pw
        user_name = user_object.user_nickname
        c.execute(f"update user_list set user_id='{user_id}', user_pw = '{user_pw}', user_name='{user_name}')")
        self.commit_db()
        c.execute(f"select * from user_list where user_id = '{user_id}'")
        updated_user = c.fetchone()
        updated_user_obj = User(*updated_user)
        self.end_conn()
        return updated_user_obj

    # 로그인 기능
    def user_log_in(self, login_id, login_pw):
        c = self.start_conn()
        c.execute(f"select * from user_list where user_id = '{login_id}' and user_pw = '{login_pw}'")
        exist_user = c.fetchone()
        self.end_conn()
        if exist_user is not None:
            print('로그인 성공')
            login_user_obj = User(*exist_user)
            return login_user_obj
        else:
            print('아이디 혹은 비밀번호를 잘못 입력했습니다.')
            return False

    # 아이디 중복체크
    def check_join_id(self, inserted_id):
        c = self.start_conn()
        c.execute(f"select * from user_list where user_id = '{inserted_id}'")
        username_id = c.fetchone()
        if username_id is None:
            return True
        else:
            return False

    # 회원가입 요청
    def user_sign_up(self, user_id, user_pw, user_nickname):
        useable_id = self.check_join_id(user_id)
        if useable_id is False:
            return False
        c = self.start_conn()
        c.execute('select * from user_list order by user_number desc limit 1')
        last_user_row = c.fetchone()
        if last_user_row is None:
            user_number = 1
        else:
            user_number = last_user_row[0] + 1
        sign_up_user_obj = User(user_number, user_id, user_pw, user_nickname)
        self.end_conn()
        sing_up_obj = self.insert_user(sign_up_user_obj)
        return sing_up_obj

    # 알림 설정
    # def alarm_setting(self, user_object: Alarm):
    #     user_id = user_object.user_id
    #     alarm_name = user_object.alarm_name
    #     alarm_time = user_object.alarm_time
    #     alarm_date = user_object.alarm_date
    #     alarm_day_of_the_week = user_object.alarm_day_of_the_week
    #     alarm_song = user_object.alarm_song
    #     c = self.start_conn()


    # 알람 수정

    # 알람 취소

    # 알람 노래설정

    # 알람 노래 수정

    # 알람 기간 설정

    # 알람 기간 수정

    # 알람 시간 수정
