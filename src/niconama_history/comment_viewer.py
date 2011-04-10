#-*- coding:utf-8
from ConfigParser import SafeConfigParser
from argparse import ArgumentError
from niconama_history.BeautifulSoup import BeautifulSoup
import datetime
import os.path
import re
import sqlite3
import time

configFileName = u'niconama_history.conf'

def createInstance(type):
    """
    ファクトリメソッドです。引数によって適切なコメントビューワのインスタンスを返します。
    """
    instance = dict(nwhois=Nwhois, ncv=NCV, anko=GissiriAnko).get(type)
    if instance == None:
        raise ArgumentError(u'適切なコメントビューアを選択できません。')

    return instance()

class CommentViewer(object):
    def __init__(self):
        if os.path.exists(configFileName) == False:
            self._initializeConfig()

        self.config = SafeConfigParser()
        self.config.read(configFileName)

    def _initializeConfig(self):
        config = r"""[nwhois]
Comment={LOCALAPPDATA}\nwhois\data\database\log3.sqlite

[ncv]
Comment={APPDATA}\posite-c\NiconamaCommentViewer\CommentLog\
UserSetting={APPDATA}\posite-c\\NiconamaCommentViewer\UserSetting.xml

[anko]
Comment={USERPROFILE}\Documents\ギッシリアンコちゃん\log\
""".encode('utf-8')

        with open(configFileName, u'w') as handle:
            handle.write(config)

class Nwhois(CommentViewer):
    def saveConfig(self, options):
        if options.path:
            self.config.set(options.type, u'Comment', options.path)

    def loadComment(self, community):
        self.sqlFile = re.sub(ur'{(\w+?)}', lambda match: os.environ[match.group(1)], self.config.get(u'nwhois', u'Comment'))

        if os.path.exists(self.sqlFile) == False:
            raise AttributeError(u'データベースファイルが存在しません。')

        sql = u"""
            SELECT
                chat.cid AS community_id
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

class NCV(CommentViewer):
    def saveConfig(self, options):
        if options.path:
            self.config.set(options.type, u'Comment', options.path)
        if options.user:
            self.config.set(options.type, u'UserSetting', options.userSetting)

    def loadComment(self, communityId):
        def loadUserSetting(communityId):
            userFile = re.sub(ur'{(\w+?)}', lambda match: os.environ[match.group(1)], self.config.get(u'ncv', u'UserSetting'))
            parser = BeautifulSoup(open(userFile, u'r'))
            nameTagList = parser.findAll(u'user', attrs = { u'community': communityId, u'name': True } )
            return dict(map(lambda tag: (tag.renderContents(), tag.get(u'name')), nameTagList))

        nameDict = loadUserSetting(communityId)
        commentLogFolder = re.sub(ur'{(\w+?)}', lambda match: os.environ[match.group(1)], self.config.get(u'ncv', u'Comment'))
        commentLogFileList = filter(lambda file: re.match(ur'ncvLog_lv\d+-{0}\.xml$'.format(communityId), file) , os.listdir(commentLogFolder))

        chatList = []
        for commentFile in commentLogFileList:
            parser = BeautifulSoup(open(os.path.join(commentLogFolder, commentFile), u'r'))
            chatTagList =  parser.find(u'livecommentdataarray').findAll(u'chat', recursive=False)
            for chatTag in chatTagList:
                userId = chatTag.get(u'user_id')
                if chatTag.get(u'user_id') == u'':
                    continue

                communityId = communityId
                name = nameDict.get(userId)
                message = chatTag.renderContents().decode(u'utf-8')
                option = chatTag.get(u'mail')
                unixtime = time.localtime(int(chatTag.get(u'date')))
                date = (datetime.datetime(*unixtime[:-3]).strftime(u'%Y-%m-%d %H:%M:%S') if unixtime else None).decode(u'utf-8')
                chatList.append((communityId, userId, name, message, option, date))

        return chatList

class GissiriAnko(CommentViewer):
    def saveConfig(self, options):
        if options.path:
            self.config.set(options.type, 'Comment', options.path)

    def loadComment(self, communityId):
        def communityFilter(filePath):
            parser = BeautifulSoup(open(os.path.join(filePath), 'r'))
            return parser.find('communityid').renderContents() == communityId

        logFolderPath = re.sub('{(\\w+?)}', lambda match: os.environ[match.group(1)], self.config.get('anko', 'Comment')).decode('utf-8')
        liveInfoFilePathList = filter(lambda file: re.match(r'nico\d{8}_\d+_ticket\.xml$', file) , os.listdir(logFolderPath))
        communityCommentFilePathList = map(lambda filePath: filePath.replace('ticket.xml', 'xml.txt'), filter(communityFilter, map(lambda name: os.path.join(logFolderPath, name), liveInfoFilePathList)))

        chatList = []
        for commentFile in communityCommentFilePathList:
            parser = BeautifulSoup(open(os.path.join(logFolderPath, commentFile), 'r'))
            chatTagList = parser.findAll(u'chat', attrs={'msgkind': 'message_msg'})
            for chatTag in chatTagList:
                communityId = communityId.decode('utf-8')
                userId = chatTag.get(u'user').decode('utf-8')
                name = chatTag.get(u'nickname').decode('utf-8')
                message = chatTag.renderContents().decode('utf-8')
                option = chatTag.get(u'mail').decode('utf-8')
                date = chatTag.get(u'date').replace('/', '-').decode('utf-8')
                chatList.append((communityId, userId, name, message, option, date))

        return chatList

if __name__ == '__main__':
    createInstance(u'nwhois')