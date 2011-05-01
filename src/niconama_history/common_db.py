#-*- coding:utf-8
from datetime import datetime
import calendar
import re
import sqlite3

class CommonDb(object):
    """
    共通DB管理クラスです。
    """
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
        共通DBをクローズします。
        """
        self.connect.close()

    def insertComment(self, commentList):
        """
        コメントを共通DBに代入します。

        :param list commentList: コメントタプル(communityId, liveId, userId, name, message, option, date)のリスト
        """
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
        """
        全期間のコメントを取得します。

        :returns: Rowクラスのリスト
        """
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

        return [(datetime(9999,12,31), map(lambda comment: Comment(*comment), self.connect.execute(sql)))]

    def selectYears(self):
        """
        年毎のコメントを取得します。

        :returns: Commentクラスのリスト
        """
        terms = self._selectTerm(u'%Y')
        return self._selectDates(terms)

    def selectMonthes(self):
        """
        月毎のコメントを取得します。

        :returns: Commentクラスのリスト
        """
        terms = self._selectTerm(u'%Y-%m')
        return self._selectDates(terms)

    def selectDays(self):
        """
        日毎のコメントを取得します。

        :returns: Commentクラスのリスト
        """
        terms = self._selectTerm(u'%Y-%m-%d')
        return self._selectDates(terms)

    def _selectTerm(self, termFormat):
        """
        指定された期間毎のリストを返します。

        :returns: 日付を表したテキストのリスト
        """
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
        """
        指定した期間のコメントを取得します。

        :returns: Commentクラスのリスト
        """
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

        return map(lambda (term,): (self._termToDate(term), map(lambda comment: Comment(*comment), self.connect.execute(sql.format(term)))), terms)

    def _termToDate(self, term):
        """
        期間を表した文字列を日付型に変換します。

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

class Comment(object):
    """
    コメントを格納するクラスです。
    """
    def __init__(self, communityId, liveId, userId, name, message, option, datetime):
        self.communityId = communityId
        self.liveId = liveId
        self.userId = userId
        self.name = name
        self.message = message
        self.option = option
        self.datetime = datetime

    def __eq__(self, other):
        sameCommunityId = self.communityId == other.communityId
        sameLiveId = self.liveId == other.liveId
        sameUserId = self.userId == other.userId
        sameName = self.name == other.name
        sameMessage = self.message == other.message
        sameOption = self.option == other.option
        sameDatetime = self.datetime == other.datetime
        return sameCommunityId and sameLiveId and sameUserId and sameName and sameMessage and sameOption and sameDatetime

if __name__ == '__main__':
    import doctest
    doctest.testmod()