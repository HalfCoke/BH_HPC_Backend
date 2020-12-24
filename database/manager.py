import pymysql

from config import DB_CONFIG


# 数据库管理，链接数据库并获取数据
class SQLManager(object):
    def __init__(self, db):
        self.conn = None
        self.db = db
        self.cursor = None
        self.connect()

    def connect(self):
        self.conn = pymysql.connect(
            host=DB_CONFIG["host"],
            port=DB_CONFIG["port"],
            user=DB_CONFIG["user"],
            passwd=DB_CONFIG["passwd"],
            charset=DB_CONFIG["charset"],
            db=self.db,
        )
        self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)

    # 查询多条数据
    def get_list(self, sql, args=None):
        self.cursor.execute(sql, args)
        result = self.cursor.fetchall()
        return result

    # 查询单条数据
    def get_one(self, sql, args=None):
        self.cursor.execute(sql, args)
        result = self.cursor.fetchone()
        return result

    # 执行命令
    def execute(self, sql):
        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except:
            self.conn.rollback()

    # 关闭数据库cursor和连接
    def close(self):
        self.cursor.close()
        self.conn.close()

    # 进入with语句自动执行
    def __enter__(self):
        return self

    # 退出with语句块自动执行
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
