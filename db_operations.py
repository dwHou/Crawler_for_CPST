import pymysql


class DatabaseOperation(object):
    def __init__(self, site, username, password, database_name):
        """

        :param site: such as root@localhost, localhost is the site
        :param username: the username of whom own the database
        :param password: password used to login the database
        :param database_name: the name of the database
        """
        self.site = site
        self.username = username
        self.password = password
        self.database_name = database_name

    def __operation__(self, _name_):
        """

        :type _name_: str
        :param _name_: the type of operation
        :return: none
        """
        db = pymysql.connect(self.site, self.username, self.password, self.database_name)
        cursor = db.cursor()

        try:
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()
            print('>>> ' + _name_ + ' operation occur some errors!')

        db.close()

    def query(self, sql):
        """

        :type sql: str
        :param sql: sql operation clause
        :return: list
        """
        db = pymysql.connect(self.site, self. username, self.password, self.database_name)
        cursor = db.cursor()

        try:
            cursor.execute(sql)
            results = cursor.fetchall()

            for row in results:
                print(row)
        except:
            print('>>> Insertion operation has some errors!')

        db.close()

    def update(self, sql):
        """

        :type sql: str
        :param sql: update operation
        :return:
        """
        self.__operation__(_name_='UPDATE')

    def insertion(self, sql):
        """

        :type sql: str
        :param sql: insertion operation
        :return: none
        """
        self.__operation__(_name_='INSERTION')

    def deletion(self, sql):
        """

        :type sql: str
        :param sql: deletion operation
        :return: none
        """
        self.__operation__(_name_='DELETION')


test_operation = DatabaseOperation(site='localhost', username='root', password='961727', database_name='crawler')
test_operation.query('select * from test_use')
test_operation.insertion()
test_operation.update()


