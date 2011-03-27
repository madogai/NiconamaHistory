#-*- coding:utf-8
from ConfigParser import SafeConfigParser
from argparse import ArgumentError
import os.path
import re
import sqlite3

def createInstance(type):
    """ファクトリメソッドです。引数によって適切なコメントビューワのインスタンスを返します。
    """
    instance = dict(nwhois=Nwhois, ncv=NCV).get(type)
    if instance == None:
        raise ArgumentError('適切なコメントビューアを選択できません。')

    return instance()

def initializeConfig():
    config = """
[nwhois]
Comment={LOCALAPPDATA}\nwhois\data\database\log3.sqlite

[ncv]
Comment={APPDATA}\posite-c\NiconamaCommentViewer\CommentLog\
UserSetting={APPDATA}\posite-c\NiconamaCommentViewer\UserSetting.xml

[anko]
Comment={USERPROFILE}\Documents\ギッシリアンコちゃん\log
"""

    with open('config.ini', 'w') as handle:
        handle.write(config)

class AbstractCommentViewer(object):
    def __init__(self):
        self.config = SafeConfigParser()
        self.config.read('config.ini')

    def saveConfig(self, options):
        pass

    def loadComment(self, community):
        pass

class Nwhois(AbstractCommentViewer):
    def saveConfig(self, options):
        if options.path:
            self.config.set(options.type, 'Comment', options.path)

    def loadComment(self, community):
        """コメントデータをロードします。
        """
        self.sqlFile = re.sub('{(\\w+?)}', lambda match: os.environ[match.group(1)], self.config.get('nwhois', 'Comment'))

        if os.path.exists(self.sqlFile) == False:
            raise AttributeError('データベースファイルが存在しません。')

        sql = """
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
        """.format(community)

        conn = sqlite3.connect(self.sqlFile)
        chatList = conn.execute(sql).fetchall()

        return chatList

class NCV(AbstractCommentViewer):
    def saveConfig(self, options):
        if options.path:
            self.config.set(options.type, 'Comment', options.path)
        if options.userSetting:
            self.config.set(options.type, 'UserSetting', options.userSetting)

    def loadComment(self, community):
        """コメントデータをロードします。
        """
        pass

if __name__ == '__main__':
    createInstance('nwhois')