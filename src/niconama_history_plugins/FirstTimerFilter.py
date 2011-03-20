#-*- coding:utf-8
'''
Created on 2011/03/20

@author: madguy
'''
from niconama_history.PluginBase import PluginBase

class commentFilter(PluginBase):

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
        self.regularList = db.connect.execute(sql).fetchall()

    @property
    def name(self):
        return 'FirstTimer'

    def analyzeDay(self, rows):
        for row in rows:
            ragulars = filter(lambda (userId, name): userId == row.userId, self.regularList)
            if len(ragulars) == 0:
                return

            for regular in self.regularList:
                self.regularList.remove(regular)
            return map(lambda (userId, name): '{0}が初登場！'.format(name), self.regularList)

if __name__ == '__main__':
    pass
