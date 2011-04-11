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
        connect = sqlite3.connect(u':memory:')
        connect.text_factory = sqlite3.OptimizedUnicode

        createDbSql = u"""
            CREATE TABLE comment (
                community_id TEXT,
                live_id TEXT,
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
                ,live_id
                ,user_id
                ,name
                ,message
                ,option
                ,datetime
            ) VALUES
                (?, ?, ?, ?, ?, ?, ?)
            ;
        """

        for comment in commentList:
            self.connect.execute(sqlBase, comment)

        self.connect.execute(u'CREATE INDEX datetime_index ON comment (datetime);')
        self.connect.commit()

    def selectAll(self):
        sql = u"""
            SELECT
                community_id
                ,live_id
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
        terms = self._selectTerm(u'%Y')
        return self._selectDates(terms)

    def selectMonthes(self):
        terms = self._selectTerm(u'%Y-%m')
        return self._selectDates(terms)

    def selectDays(self):
        terms = self._selectTerm(u'%Y-%m-%d')
        return self._selectDates(terms)

    def _selectTerm(self, termFormat):
        sql = u"""
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
        sql = u"""
            SELECT
                community_id
                ,live_id
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

        return map(lambda (term,): (self._termToDate(term), map(lambda comment: Row(*comment), self.connect.execute(sql.format(term)))), terms)

    def _termToDate(self, term):
        """
        >>> instance = CommonDb()
        >>> instance._termToDate('2000')
        datetime.datetime(2000, 12, 31, 0, 0)
        >>> instance._termToDate('2000-01')
        datetime.datetime(2000, 1, 31, 0, 0)
        >>> instance._termToDate('2000-01-01')
        datetime.datetime(2000, 1, 1, 0, 0)
        """
        if re.match(u'\d{4}$', term):
            return datetime.strptime(u'{0}-12-31'.format(term), u'%Y-%m-%d')
        elif re.match(u'\d{4}-\d{2}$', term):
            (year, month) = term.split('-')
            dayCount = calendar.monthrange(int(year), int(month))[1]
            return datetime(int(year), int(month), dayCount)
        else:
            return datetime.strptime(term, u'%Y-%m-%d')

class Row(object):
    def __init__(self, communityId, liveId, userId, name, message, option, datetime):
        self.communityId = communityId
        self.liveId = liveId
        self.userId = userId
        self.name = name
        self.message = message
        self.option = option
        self.datetime = datetime

if __name__ == '__main__':
    import doctest
    doctest.testmod()