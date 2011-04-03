#-*- coding:utf-8
'''
Created on 2011/03/20

@author: madguy
'''
from niconama_history.PluginBase import PluginBase

class CommentFilter(PluginBase):
    """
    常連さんの出現を抽出するプラグインです。
    """

    def __init__(self, db):
        PluginBase.__init__(self)
        sql = """
            SELECT
                user_id
                ,name
            FROM
                comment
            WHERE
                name IS NOT NULL
            GROUP BY
                user_id
                ,name
            HAVING
                count(user_id) > {}
            ;
        """.format(1000)
        self.regularSet = set(db.connect.execute(sql).fetchall())

    @property
    def name(self):
        return 'FirstTimer'

    def analyzeDay(self, rows):
        messages = []
        for row in rows:
            ragulars = filter(lambda (userId, name): userId == row.userId, self.regularSet)
            if len(ragulars) > 0:
                self.regularSet -= set(ragulars)
                messages.extend(map(lambda (userId, name): '{0}が初登場！'.format(name), ragulars))

        return messages

if __name__ == '__main__':
    pass
