#-*- coding:utf-8

from collections import defaultdict
from niconama_history.plugin_base import PluginBase

class CommentFilter(PluginBase):
    """
    月毎の最も発言したリスナーを抽出するプラグインです。
    """
    def analyzeMonth(self, date, rows):
        userDict = defaultdict(int)

        for row in filter(lambda row: (row.name is not None) and (len(row.name) > 0), rows):
            userDict[(row.userId, row.name)] += 1

        userName = max(userDict, key = lambda x: userDict.get(x))[1]
        message = u'一番発言したのは{0}さんでした。'.format(userName)
        return message

if __name__ == '__main__':
    pass
