#-*- coding:utf-8
from BeautifulSoup.BeautifulSoup import BeautifulSoup
from ConfigParser import SafeConfigParser
from argparse import ArgumentError
import datetime
import os.path
import re
import sqlite3
import time

configFileName = u'niconama_history.conf'

def createInstance(type):
    """
    ファクトリメソッドです。引数によって適切なコメントビューワのインスタンスを返します。

    :param unicode type: パラメータ文字列。nwhois, ncv, ankoが指定できます。
    :returns: コメントビューアパーサのインスタンス
    """
    instance = dict(nwhois=Nwhois, ncv=NCV, anko=GissiriAnko).get(type)
    if instance == None:
        raise ArgumentError(u'適切なコメントビューアを選択できません。')

    return instance()

class CommentViewer(object):
    """
    コメントビューアパーサの基底クラスです。
    """
    def __init__(self):
        """
        コンストラクタです。
        コンフィグファイルを読み込みます。
        コンフィグファイルが存在しない場合、生成します。
        """
        if os.path.exists(configFileName) == False:
            self._initializeConfig()

        self.config = SafeConfigParser()
        self.config.read(configFileName)

    def _initializeConfig(self):
        """
        コンフィグファイルを生成します。
        """
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
    """
    Nwhoisのパーサクラスです。
    """
    def saveConfig(self, options):
        """
        nwhoisのコンフィグを上書きします。

        :param object options: オプション
        """
        if options.path:
            self.config.set(options.type, u'Comment', options.path)

    def loadComment(self, communityId):
        """
        sqliteログからコメントを抽出します。
        コメントログのパスはコンフィグファイルから読み込みます。

        :param string communityId: コミュニティID(coXXX)
        :returns: チャットのタプル(communityId, liveId, userId, name, message, option, date)
        """
        sqlFilePath = re.sub(ur'{(\w+?)}', lambda match: os.environ[match.group(1)], self.config.get(u'nwhois', u'Comment'))
        return self._loadComment(communityId, sqlFilePath)

    def _loadComment(self, community, sqlFilePath):
        if os.path.exists(sqlFilePath) == False:
            raise AttributeError(u'データベースファイルが存在しません。')

        sql = u"""
            SELECT
                chat.cid AS community_id
                ,lid AS live_id
                ,uid AS user_id
                ,name
                ,message
                ,CASE WHEN mail <> '' THEN mail ELSE null END AS optoin
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
            ORDER BY
                chat.no
            ;
        """.format(community)

        conn = sqlite3.connect(sqlFilePath)
        chatList = conn.execute(sql).fetchall()

        return chatList

class NCV(CommentViewer):
    """
    NiconamaCommentViewer用のパーサクラスです。
    """
    def saveConfig(self, options):
        """
        ncvのコンフィグを上書きします。

        :param object options: オプション
        """
        if options.path:
            self.config.set(options.type, u'Comment', options.path)
        if options.user:
            self.config.set(options.type, u'UserSetting', options.userSetting)

    def loadComment(self, communityId):
        """
        ログフォルダからコメントファイルを探索して抽出します。
        コメントログのパスはコンフィグファイルから読み込みます。

        :param string communityId: コミュニティID(coXXX)
        :returns: チャットのタプル(communityId, liveId, userId, name, message, option, date)
        """
        userSettingFilePath = re.sub(ur'{(\w+?)}', lambda match: os.environ[match.group(1)], self.config.get(u'ncv', u'UserSetting'))
        commentLogFolder = re.sub(ur'{(\w+?)}', lambda match: os.environ[match.group(1)], self.config.get(u'ncv', u'Comment'))
        return self._loadComment(communityId, userSettingFilePath, commentLogFolder)

    def _loadComment(self, communityId, userSettingFilePath, commentLogFolder):
        nameDict = self._loadUserSetting(communityId, userSettingFilePath)
        commentLogFileList = filter(lambda file: re.match(ur'ncvLog_lv\d+-{0}\.xml$'.format(communityId), file) , os.listdir(commentLogFolder))

        chatList = []
        for commentFile in commentLogFileList:
            parser = BeautifulSoup(open(os.path.join(commentLogFolder, commentFile), u'r'))
            liveId = u'lv' + parser.find(u'livenum').renderContents().decode(u'utf-8')
            chatTagList = parser.find(u'livecommentdataarray').findAll(u'chat', recursive=False)
            for chatTag in chatTagList:
                userId = chatTag.get(u'user_id')
                if chatTag.get(u'user_id') == u'':
                    continue

                name = nameDict.get(userId)
                message = chatTag.renderContents().decode(u'utf-8')
                option = chatTag.get(u'mail')
                unixtime = time.localtime(int(chatTag.get(u'date')))
                date = (datetime.datetime(*unixtime[:-3]).strftime(u'%Y-%m-%d %H:%M:%S') if unixtime else None).decode(u'utf-8')
                chatList.append((communityId, liveId, userId, name, message, option, date))

        return chatList

    def _loadUserSetting(self, communityId, userSettingFilePath):
        parser = BeautifulSoup(open(userSettingFilePath, u'r'))
        nameTagList = parser.findAll(u'user', attrs={ u'community': communityId, u'name': True })
        return dict(map(lambda tag: (tag.renderContents(), tag.get(u'name')), nameTagList))

class GissiriAnko(CommentViewer):
    """
    ギッシリアンコちゃん用のパーサクラスです。
    """
    def saveConfig(self, options):
        """
        ギッシリアンコちゃんのコンフィグを上書きします。

        :param object options: オプション
        """
        if options.path:
            self.config.set(options.type, u'Comment', options.path)

    def loadComment(self, communityId):
        """
        ログフォルダからコメントファイルを探索して抽出します。
        コメントログのパスはコンフィグファイルから読み込みます。

        :param string communityId: コミュニティID(coXXX)
        :returns: チャットのタプル(communityId, liveId, userId, name, message, option, date)
        """
        logFolderPath = re.sub(ur'{(\w+?)}', lambda match: os.environ[match.group(1)], self.config.get(u'anko', u'Comment')).decode('utf-8')
        return self._loadComment(communityId, logFolderPath)

    def _loadComment(self, communityId, logFolderPath):
        liveInfoFilePathList = map(lambda name: os.path.join(logFolderPath, name), filter(lambda file: re.match(ur'nico\d{8}_\d+_ticket\.xml$', file) , os.listdir(logFolderPath)))
        communityCommentFileList = map(lambda filePath: (filePath, filePath.replace(u'ticket.xml', u'xml.txt')), liveInfoFilePathList)

        chatList = []
        for communityCommentFile in communityCommentFileList:
            chatList.extend(self._parseComment(communityId, *communityCommentFile))

        return chatList

    def _parseComment(self, communityId, liveInfoFilePath, commentFilePath):
        chatList = []
        if not (os.path.exists(liveInfoFilePath) and os.path.exists(commentFilePath)):
            return chatList

        infoParser = BeautifulSoup(open(liveInfoFilePath, u'r'))
        if not infoParser.find(u'communityid').renderContents() == communityId:
            return chatList

        commentParser = BeautifulSoup(open(commentFilePath, u'r'))
        chatTagList = commentParser.findAll(u'chat', attrs={u'msgkind': u'message_msg'})
        for chatTag in chatTagList:
            communityId = communityId.decode(u'utf-8')
            liveId = infoParser.find(u'liveid').renderContents().decode()
            userId = chatTag.get(u'user').decode(u'utf-8')
            name = chatTag.get(u'nickname').decode(u'utf-8')
            message = chatTag.renderContents().decode(u'utf-8')
            option = chatTag.get(u'mail').decode(u'utf-8') if chatTag.get(u'mail') != '' else None
            date = re.sub(
                ur'(\d{4})/(\d{1,2})/(\d{1,2})\s(\d{1,2}):(\d{1,2}):(\d{1,2})',
                lambda match: u'{0:04d}-{1:02d}-{2:02d} {3:02d}:{4:02d}:{5:02d}'.format(int(match.group(1)), int(match.group(2)), int(match.group(3)), int(match.group(4)), int(match.group(5)), int(match.group(6))),
                chatTag.get(u'date')
            ).decode(u'utf-8')
            chatList.append((communityId, liveId, userId, name, message, option, date))

        return chatList

if __name__ == '__main__':
    createInstance(u'nwhois')
