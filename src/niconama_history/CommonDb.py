#-*- coding:utf-8
from datetime import datetime
import calendar
import re
import sqlite3

class CommonDb(object):
    def __enter__(self):
        connect = sqlite3.connect(':memory:')

        createDbSql = u'''
            CREATE TABLE comment (
                community_id TEXT,
                user_id TEXT,
                name TEXT,
                message TEXT,
                option TEXT,
                datetime TEXT
            );
        '''
        connect.execute(createDbSql)
        self.connect = connect
        return self

    def __exit__(self, exc_type, exc_value, traceback):
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

    def selectYears(self):
        return self._selectTerm('%Y')

    def selectMonthes(self):
        return self._selectTerm('%Y-%m')

    def selectDays(self):
        return self._selectTerm('%Y-%m-%d')

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

        terms = self.connect.execute(sql)

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

        return map(lambda (term,): (self._termToDate(term), map(lambda comment: Row(comment), self.connect.execute(sql.format(term)))), terms)

    def _termToDate(self, term):
        if re.match('\d{4}$', term):
            return datetime.strptime(term + '-12-31', '%Y-%m-%d')
        elif re.match('\d{4}-\d{2}$', term):
            (year, month) = term.split('-')
            dayCount = calendar.monthrange(int(year), int(month))[1]
            return datetime(int(year), int(month), dayCount)
        else:
            return datetime.strptime(term, '%Y-%m-%d')

class Row(object):

    def __init__(self, row):
        self.communityId = row[0]
        self.userId = row[1]
        self.name = row[2]
        self.message = row[3]
        self.option = row[4]
        self.datetime = row[5]

if __name__ == '__main__':
    import doctest
    doctest.testmod()