#-*- coding:utf-8
from datetime import datetime
import calendar
import re
import sqlite3

class CommonDb(object):

    def __enter__(self):
        """
        メモリ上に共通DBを構築します。
        """

        connect = sqlite3.connect(':memory:')

        createDbSql = """
            CREATE TABLE comment (
                community_id TEXT,
                user_id TEXT,
                name TEXT,
                message TEXT,
                option TEXT,
                datetime TEXT
            );
        """
        connect.execute(createDbSql)
        self.connect = connect
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        データベースをクローズします。
        """
        self.connect.close()

    def insertComment(self, commentList):
        sqlBase = u"""
            INSERT INTO comment(
                community_id
                ,user_id
                ,name
                ,message
                ,option
                ,datetime
            ) VALUES
                (?, ?, ?, ?, ?, ?)
            ;
        """

        for communityId, userId, name, message, option, datetime in commentList:
            self.connect.execute(sqlBase, (communityId, userId, name, message, option, datetime))

        self.connect.execute('CREATE INDEX datetime_index ON comment (datetime);')
        self.connect.commit()

        print '共通DBの構築が完了しました。'

    def selectAll(self):
        sql = """
            SELECT
                community_id
                ,user_id
                ,name
                ,message
                ,option
                ,datetime
            FROM
                comment
            ;
        """

        return [(datetime(9999,12,31), map(lambda comment: Row(*comment), self.connect.execute(sql)))]

    def selectYears(self):
        terms = self._selectTerm('%Y')
        return self._selectDates(terms)

    def selectMonthes(self):
        terms = self._selectTerm('%Y-%m')
        return self._selectDates(terms)

    def selectDays(self):
        terms = self._selectTerm('%Y-%m-%d')
        return self._selectDates(terms)

    def _selectTerm(self, termFormat):
        sql = """
            SELECT
                strftime('{0}', datetime) AS date
            FROM
                comment
            GROUP BY
                strftime('{0}', datetime)
            ORDER BY
                date
            ;
        """.format(termFormat)

        return self.connect.execute(sql).fetchall()

    def _selectDates(self, terms):
        def termToDate(term):
            if re.match('\d{4}$', term):
                return datetime.strptime(term + '-12-31', '%Y-%m-%d')
            elif re.match('\d{4}-\d{2}$', term):
                (year, month) = term.split('-')
                dayCount = calendar.monthrange(int(year), int(month))[1]
                return datetime(int(year), int(month), dayCount)
            else:
                return datetime.strptime(term, '%Y-%m-%d')

        sql = """
            SELECT
                community_id
                ,user_id
                ,name
                ,message
                ,option
                ,datetime
            FROM
                comment
            WHERE
                datetime LIKE '{0}%'
            ;
        """

        return map(lambda (term,): (termToDate(term), map(lambda comment: Row(*comment), self.connect.execute(sql.format(term)))), terms)

class Row(object):

    def __init__(self, communityId, userId, name, message, option, datetime):
        self.communityId = communityId
        self.userId = userId
        self.name = name
        self.message = message
        self.option = option
        self.datetime = datetime

if __name__ == '__main__':
    import doctest
    doctest.testmod()