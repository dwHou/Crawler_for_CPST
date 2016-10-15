import MySQLdb


class DatabaseOperation(object):
    def __init__(self, host, user, passwd, db):
        """

        :param host: such as root@localhost, localhost is the site
        :param user: the username of whom own the database
        :param passwd: password used to login the database
        :param db: the name of the database
        """
        self.conn = MySQLdb.connect(host=host, user=user, passwd=passwd, db=db)

    def __del__(self):
        """Close database automatic

        :return: none
        """
        try:
            self.conn.close()
        except:
            print('>> ERORRS OCCUR WHEN CLOSE CONNECTION!')

    def __operation__(self, _name_, sql):
        """Agrefunction which be used in some operations

        :type _name_: str
        :param _name_: the type of operation
        :return: none
        """
        cursor = self.conn.cursor()

        try:
            cursor.execute(sql)
            self.conn.commit()
        except:
            self.conn.rollback()
            print('>>> ' + _name_ + ' operation occur some errors!')

    def close_db(self):
        """Close database manual

        :return: none
        """
        self.conn.close()

    def create_table(self, sql):
        cursor = self.conn.cursor()

        try:
            cursor.execute(sql)
            print('>>> CREATE NEW TABLE')
        except:
            print('>>> CANNOT CREATE A NEW TABLE, SOME EROORS OCCUR!')

    def query(self, sql):
        """Query some data and return as a list type

        :type sql: str
        :param sql: sql operation clause
        :return: list
        """
        cursor = self.conn.cursor()

        try:
            cursor.execute(sql)
            results = cursor.fetchall()

            for row in results:
                print(row)
        except:
            print('>>> Insertion operation has some errors!')

    def update(self, sql):
        """Update operation

        :type sql: str
        :param sql: update operation
        :return:
        """
        self.__operation__(_name_='UPDATE', sql=sql)

    def insertion(self, sql):
        """Insertion operation

        :type sql: str
        :param sql: insertion operation
        :return: none
        """
        self.__operation__(_name_='INSERTION', sql=sql)

    def deletion(self, sql):
        """Deletion operation

        :type sql: str
        :param sql: deletion operation
        :return: none
        """
        self.__operation__(_name_='DELETION', sql=sql)

    def insert_file(self, sql, file_obj):
        """This function is particular for insert file object into a certain table

        :type sql: str
        :param sql: operation clause

        :type file_obj: bytes
        :param file_obj: file object, normal binary
        :return: none
        """
        cursor = self.conn.cursor()
        cursor.execute(sql, [MySQLdb.Binary(file_obj)])
        cursor.commit()

    def get_file(self, sql):
        """Function used to get a file object from database

        :type sql: str
        :param sql:
        :return: bytes
        """
        cursor = self.conn.cursor()
        cursor.execute(sql)
        file = cursor.fetchone()[0]
        return file

    def drop_table(self, sql):
        """Drop down table

        :type sql: str
        :param sql: drop clause
        :return: none
        """
        cursor = self.conn.cursor()
        try:
            cursor.execute(sql)
        except:
            print('>>> DROP TABLE OPERATION OCCURS ERRORS')

        # self.conn.commit()


test_operation = DatabaseOperation(host='localhost', user='root', passwd='961727', db='crawler')
test_operation.closedb()
