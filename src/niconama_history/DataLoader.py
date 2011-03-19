#-*- coding:utf-8
import sqlite3

def createInstance(keyword):
    if keyword == 'nwhois':
        return Nwhois()

class Nwhois:
    def __init__(self):
        self.sqlFile = 'log3.sqlite'

    def load(self, community):
        sql = u'''
            SELECT
                chat.cid AS chat_id
                ,uid AS user_id
                ,name
                ,message
                ,mail AS optoin
                ,datetime((date / 10000000) - 62135596800, 'unixepoch') AS insert_time
            FROM
                chat
            LEFT JOIN
                user
            ON
                chat.uid = user.id
            AND chat.cid = user.cid
            WHERE
                chat.cid = '{}'
            ;
        '''.format(community)

        conn = sqlite3.connect(self.sqlFile)
        chatList = conn.execute(sql).fetchall()

        return chatList

if __name__ == '__main__':
    createInstance('nwhois')